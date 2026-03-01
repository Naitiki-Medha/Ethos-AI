"""
Enhanced Compliance Engine with Context Validation Layer
Ensures 100% correct format and eliminates loopholes
Includes Human Review Gate for high-risk cases
Includes Omission Detection for missing compliance elements
"""

from typing import List, Optional
from core.context import ComplianceContext, ComplianceReport
from core.context_validator import ContextValidator, ContextEnricher, ContextValidationError
from core.engine import ComplianceEngine
from core.human_review_gate import HumanReviewGate, ReviewCase
from core.omission_detector import OmissionDetector
from utils.audit import AuditLogger


class EnhancedComplianceEngine:
    """
    Enhanced compliance engine with multi-layer validation and human review
    
    Architecture:
    1. Context Validation Layer (ensures correct format)
    2. Context Enrichment Layer (adds intelligence)
    3. Compliance Rule Layer (checks laws)
    4. Omission Detection Layer (checks what's missing)
    5. Human Review Gate (mandatory for high-risk cases)
    6. Audit Layer (logs everything)
    """

    def __init__(
        self,
        rules: List,
        enable_logging: bool = True,
        strict_validation: bool = True,
        enable_enrichment: bool = True,
        enable_human_review: bool = True,
        enable_omission_detection: bool = True,
    ):
        """
        Initialize enhanced engine

        Args:
            rules: List of compliance rules
            enable_logging: Enable audit logging
            strict_validation: Strict mode for validation (raises errors)
            enable_enrichment: Enable context enrichment
            enable_human_review: Enable human review gate
            enable_omission_detection: Enable omission detection
        """
        self.validator = ContextValidator(strict_mode=strict_validation)
        self.enricher = ContextEnricher() if enable_enrichment else None
        self.compliance_engine = ComplianceEngine(rules, enable_logging)
        self.omission_detector = OmissionDetector() if enable_omission_detection else None
        self.human_review_gate = HumanReviewGate() if enable_human_review else None
        self.logger = AuditLogger() if enable_logging else None

    def check(self, context: ComplianceContext) -> ComplianceReport:
        """
        Enhanced compliance check with validation, omission detection, and human review

        Args:
            context: Input compliance context

        Returns:
            ComplianceReport with validation info, omissions, and review status

        Process:
        1. Validate context format
        2. Enrich context with intelligence
        3. Run compliance rules
        4. Detect omissions (what's missing)
        5. Check if human review required
        6. Log everything
        """
        validation_warnings = []

        try:
            # LAYER 1: Validate and ensure correct format
            context, warnings = self.validator.validate_and_enrich(context)
            validation_warnings.extend(warnings)

            # LAYER 2: Enrich with intelligence (optional)
            if self.enricher:
                context = self.enricher.enrich(context)

            # LAYER 3: Run compliance rules
            report = self.compliance_engine.check(context)

            # LAYER 4: Detect omissions (what's missing)
            if self.omission_detector:
                omissions = self.omission_detector.detect_omissions(context, report)

                if omissions:
                    omission_summary = self.omission_detector.get_omission_summary()

                    # Add omissions to report
                    omission_msg = f"\n\n⚠️  OMISSIONS DETECTED ({omission_summary['total_omissions']})\n"
                    omission_msg += f"Critical: {omission_summary['by_severity']['critical']}, "
                    omission_msg += f"High: {omission_summary['by_severity']['high']}, "
                    omission_msg += f"Medium: {omission_summary['by_severity']['medium']}, "
                    omission_msg += f"Low: {omission_summary['by_severity']['low']}\n\n"

                    for omission in omissions[:3]:  # Show first 3
                        omission_msg += f"• {omission.description}\n"
                        omission_msg += f"  Required: {omission.required_element}\n"
                        omission_msg += f"  Legal: {omission.legal_reference}\n\n"

                    if len(omissions) > 3:
                        omission_msg += f"... and {len(omissions) - 3} more omissions"

                    report.message = (
                        f"{report.message}{omission_msg}"
                        if report.message
                        else omission_msg
                    )

                    # Add omission metadata
                    context.metadata["omissions_detected"] = True
                    context.metadata["omission_count"] = len(omissions)
                    context.metadata["omission_summary"] = omission_summary

                    # If critical omissions, mark as non-compliant
                    if self.omission_detector.has_critical_omissions():
                        report.is_compliant = False
                        if "CRITICAL_OMISSION" not in report.violations:
                            report.violations.append("CRITICAL_OMISSION")

            # LAYER 5: Human Review Gate (if enabled)
            if self.human_review_gate:
                requires_review, reason, priority = self.human_review_gate.requires_review(
                    context, report
                )

                if requires_review:
                    # Create review case
                    review_case = self.human_review_gate.create_review_case(
                        context, report, reason, priority
                    )

                    # Update report with review info
                    report.message = (
                        f"{report.message}\n\n⚠️  HUMAN REVIEW REQUIRED\n"
                        f"Case ID: {review_case.case_id}\n"
                        f"Priority: {priority.value.upper()}\n"
                        f"Reason: {reason}"
                        if report.message
                        else f"⚠️  HUMAN REVIEW REQUIRED\n"
                        f"Case ID: {review_case.case_id}\n"
                        f"Priority: {priority.value.upper()}\n"
                        f"Reason: {reason}"
                    )

                    # Add review metadata
                    context.metadata["requires_human_review"] = True
                    context.metadata["review_case_id"] = review_case.case_id
                    context.metadata["review_priority"] = priority.value

                    # For critical cases, override to non-compliant
                    if priority.value in ["critical", "high"]:
                        report.is_compliant = False
                        if "HUMAN_REVIEW_REQUIRED" not in report.violations:
                            report.violations.append("HUMAN_REVIEW_REQUIRED")

            # Add validation info to report
            if validation_warnings:
                report.message = (
                    f"{report.message}\n\nValidation Warnings: {'; '.join(validation_warnings)}"
                    if report.message
                    else f"Validation Warnings: {'; '.join(validation_warnings)}"
                )

            # LAYER 6: Enhanced audit logging
            if self.logger:
                self._log_enhanced(context, report, validation_warnings)

            return report

        except ContextValidationError as e:
            # Validation failed - return non-compliant report
            return ComplianceReport(
                is_compliant=False,
                violations=["CONTEXT_VALIDATION_ERROR"],
                message=f"Context validation failed: {str(e)}",
            )

    def submit_review_decision(
        self,
        case_id: str,
        reviewer_id: str,
        decision: bool,
        notes: Optional[str] = None,
    ) -> ReviewCase:
        """
        Submit human review decision

        Args:
            case_id: Review case ID
            reviewer_id: Reviewer's ID
            decision: True = approve, False = reject
            notes: Optional reviewer notes

        Returns:
            Updated ReviewCase
        """
        if not self.human_review_gate:
            raise ValueError("Human review gate is not enabled")

        return self.human_review_gate.submit_review(case_id, reviewer_id, decision, notes)

    def get_pending_reviews(self, priority=None):
        """Get pending review cases"""
        if not self.human_review_gate:
            return []
        return self.human_review_gate.get_pending_reviews(priority)

    def get_review_stats(self):
        """Get review statistics"""
        if not self.human_review_gate:
            return {}
        return self.human_review_gate.get_review_stats()

    def _log_enhanced(
        self,
        context: ComplianceContext,
        report: ComplianceReport,
        warnings: List[str],
    ):
        """Enhanced logging with validation info"""
        import json
        from datetime import datetime

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": context.user_id,
            "content_hash": context.metadata.get("content_hash", "unknown"),
            "content_type": context.content_type,
            "content_length": context.metadata.get("content_length", 0),
            "is_compliant": report.is_compliant,
            "violations": report.violations,
            "validation_warnings": warnings,
            "risk_score": context.metadata.get("risk_score", 0),
            "risk_level": context.metadata.get("risk_level", "unknown"),
            "detected_language": context.metadata.get("detected_language", "unknown"),
            "sentiment": context.metadata.get("sentiment", "unknown"),
            "categories": context.metadata.get("detected_categories", []),
            "suspicious_patterns": context.metadata.get(
                "suspicious_pattern_detected", False
            ),
            "requires_human_review": context.metadata.get(
                "requires_human_review", False
            ),
            "review_case_id": context.metadata.get("review_case_id", None),
            "review_priority": context.metadata.get("review_priority", None),
        }

        self.logger.logger.info(json.dumps(log_entry))

    def get_validation_stats(self) -> dict:
        """Get validation statistics"""
        stats = {
            "validator_mode": "strict" if self.validator.strict_mode else "lenient",
            "enrichment_enabled": self.enricher is not None,
            "logging_enabled": self.logger is not None,
            "omission_detection_enabled": self.omission_detector is not None,
            "human_review_enabled": self.human_review_gate is not None,
            "total_rules": len(self.compliance_engine.rules),
        }

        if self.human_review_gate:
            stats["review_stats"] = self.get_review_stats()

        return stats

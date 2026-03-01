"""
Synthetically Generated Information (SGI) Rules
Based on IT (Intermediary Guidelines) Amendment Rules 2026
"""

from rules.base import LegalRule
from core.context import ComplianceContext, ComplianceReport
from datetime import datetime


class SGILabelingRule(LegalRule):
    """
    Enforces mandatory labeling of AI-generated content as per
    IT Amendment Rules 2026 (notified 20th Feb 2026)
    """

    @property
    def rule_name(self) -> str:
        return "SGI_MANDATORY_LABELING"

    @property
    def legal_reference(self) -> str:
        return "IT (Intermediary Guidelines) Amendment Rules 2026"

    def validate(self, context: ComplianceContext) -> ComplianceReport:
        # Check if content is marked as AI-generated
        is_ai_generated = context.metadata.get("is_ai_generated", True)
        has_sgi_label = context.metadata.get("has_sgi_label", False)

        if is_ai_generated and not has_sgi_label:
            return ComplianceReport(
                is_compliant=False,
                violations=[self.rule_name],
                message="Violation: AI-generated content must have prominent SGI labeling (visible for 10% of content duration/area)",
            )

        return ComplianceReport(is_compliant=True)


class SGIConsentRule(LegalRule):
    """
    Requires user consent declaration before generating synthetic media
    """

    @property
    def rule_name(self) -> str:
        return "SGI_USER_CONSENT"

    @property
    def legal_reference(self) -> str:
        return "IT (Intermediary Guidelines) Amendment Rules 2026"

    def validate(self, context: ComplianceContext) -> ComplianceReport:
        # For content generation requests, verify consent
        generation_triggers = [
            "generate",
            "create",
            "make",
            "produce",
            "synthesize",
        ]

        content_lower = context.content.lower()
        is_generation_request = any(
            trigger in content_lower for trigger in generation_triggers
        )

        if is_generation_request:
            has_consent = context.metadata.get("user_consent_sgi", False)
            if not has_consent:
                return ComplianceReport(
                    is_compliant=False,
                    violations=[self.rule_name],
                    message="Violation: User must provide explicit consent before generating synthetic media",
                )

        return ComplianceReport(is_compliant=True)


class HarmfulSGIBlockingRule(LegalRule):
    """
    Blocks harmful synthetic content as mandated by IT Amendment Rules 2026
    Categories: CSAM, non-consensual deepfakes, fake events, explosive material
    """

    @property
    def rule_name(self) -> str:
        return "SGI_HARMFUL_CONTENT_BLOCKING"

    @property
    def legal_reference(self) -> str:
        return "IT (Intermediary Guidelines) Amendment Rules 2026"

    def validate(self, context: ComplianceContext) -> ComplianceReport:
        content_lower = context.content.lower()

        # Harmful content categories
        harmful_patterns = {
            "CSAM": ["child", "minor", "underage", "kid"],
            "Non-consensual": ["without consent", "non-consensual", "revenge"],
            "Misinformation": [
                "fake news",
                "false event",
                "fabricated",
                "hoax",
                "misleading",
            ],
            "Violence": ["explosive", "bomb", "weapon", "violence", "harm"],
            "Explicit": ["nude", "explicit", "pornographic", "sexual"],
        }

        detected_violations = []
        for category, keywords in harmful_patterns.items():
            if any(keyword in content_lower for keyword in keywords):
                detected_violations.append(category)

        if detected_violations:
            return ComplianceReport(
                is_compliant=False,
                violations=[self.rule_name],
                message=f"Violation: Content flagged for harmful categories: {', '.join(detected_violations)}. Automated blocking required.",
            )

        return ComplianceReport(is_compliant=True)

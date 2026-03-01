"""
India AI Governance Guidelines (Nov 2025) - Seven Sutras Implementation
"""

from rules.base import LegalRule
from core.context import ComplianceContext, ComplianceReport


class FairnessEquityRule(LegalRule):
    """
    Ensures fairness, equity, and non-discrimination in AI systems
    Sutra 4: Fairness & Equity
    """

    @property
    def rule_name(self) -> str:
        return "AI_GOVERNANCE_FAIRNESS"

    @property
    def legal_reference(self) -> str:
        return "India AI Governance Guidelines 2025, Sutra 4"

    def validate(self, context: ComplianceContext) -> ComplianceReport:
        # Check for discriminatory language or bias indicators
        content_lower = context.content.lower()

        discriminatory_terms = [
            "discriminate",
            "bias against",
            "exclude",
            "only for",
            "not for",
            "deny based on",
        ]

        protected_attributes = [
            "caste",
            "religion",
            "gender",
            "race",
            "disability",
            "age",
            "sexual orientation",
        ]

        # Check if content combines discriminatory intent with protected attributes
        has_discriminatory_term = any(
            term in content_lower for term in discriminatory_terms
        )
        mentions_protected_attr = any(
            attr in content_lower for attr in protected_attributes
        )

        if has_discriminatory_term and mentions_protected_attr:
            return ComplianceReport(
                is_compliant=False,
                violations=[self.rule_name],
                message="Violation: Content may lead to discriminatory outcomes based on protected attributes",
            )

        # Check if bias mitigation is flagged as needed
        bias_detected = context.metadata.get("bias_detected", False)
        if bias_detected:
            return ComplianceReport(
                is_compliant=False,
                violations=[self.rule_name],
                message="Violation: Algorithmic bias detected. Fairness and equity principles violated.",
            )

        return ComplianceReport(is_compliant=True)


class TransparencyExplainabilityRule(LegalRule):
    """
    Ensures AI systems are understandable and transparent
    Sutra 6: Understandable by Design
    """

    @property
    def rule_name(self) -> str:
        return "AI_GOVERNANCE_TRANSPARENCY"

    @property
    def legal_reference(self) -> str:
        return "India AI Governance Guidelines 2025, Sutra 6"

    def validate(self, context: ComplianceContext) -> ComplianceReport:
        # For automated decisions, check if explainability is provided
        is_automated_decision = context.metadata.get("automated_decision", False)
        has_explanation = context.metadata.get("has_explanation", False)

        if is_automated_decision and not has_explanation:
            return ComplianceReport(
                is_compliant=False,
                violations=[self.rule_name],
                message="Violation: Automated AI decisions must be explainable and transparent to users",
            )

        return ComplianceReport(is_compliant=True)


class SafetySecurityRule(LegalRule):
    """
    Ensures AI systems are safe, secure, and sustainable
    Sutra 7: Safety, Resilience & Sustainability
    """

    @property
    def rule_name(self) -> str:
        return "AI_GOVERNANCE_SAFETY"

    @property
    def legal_reference(self) -> str:
        return "India AI Governance Guidelines 2025, Sutra 7"

    def validate(self, context: ComplianceContext) -> ComplianceReport:
        content_lower = context.content.lower()

        # Safety risk indicators
        safety_risks = [
            "harm",
            "danger",
            "unsafe",
            "threat",
            "attack",
            "exploit",
            "vulnerability",
            "malicious",
        ]

        if any(risk in content_lower for risk in safety_risks):
            # Check if safety assessment was done
            safety_assessed = context.metadata.get("safety_assessed", False)
            if not safety_assessed:
                return ComplianceReport(
                    is_compliant=False,
                    violations=[self.rule_name],
                    message="Violation: Content with potential safety risks requires safety assessment",
                )

        return ComplianceReport(is_compliant=True)


class AccountabilityRule(LegalRule):
    """
    Ensures accountability mechanisms are in place
    Sutra 5: Accountability
    """

    @property
    def rule_name(self) -> str:
        return "AI_GOVERNANCE_ACCOUNTABILITY"

    @property
    def legal_reference(self) -> str:
        return "India AI Governance Guidelines 2025, Sutra 5"

    def validate(self, context: ComplianceContext) -> ComplianceReport:
        # Check if accountability mechanisms are in place
        has_audit_trail = context.metadata.get("has_audit_trail", True)
        has_responsible_party = context.metadata.get("has_responsible_party", True)

        if not has_audit_trail:
            return ComplianceReport(
                is_compliant=False,
                violations=[self.rule_name],
                message="Violation: AI system must maintain audit trails for accountability",
            )

        if not has_responsible_party:
            return ComplianceReport(
                is_compliant=False,
                violations=[self.rule_name],
                message="Violation: Clear accountability and responsible party must be identified",
            )

        return ComplianceReport(is_compliant=True)

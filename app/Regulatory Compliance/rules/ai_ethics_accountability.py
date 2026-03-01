"""
AI Ethics & Accountability Rules
Based on AI Ethics & Accountability Bill, 2025 (Private Member Bill)
"""

from rules.base import LegalRule
from core.context import ComplianceContext, ComplianceReport


class AIEthicsFrameworkRule(LegalRule):
    """
    Enforces ethical use of AI in India
    Proposed penalties up to ₹5 crore for violations
    """

    @property
    def rule_name(self) -> str:
        return "AI_ETHICS_FRAMEWORK"

    @property
    def legal_reference(self) -> str:
        return "AI Ethics & Accountability Bill, 2025"

    def validate(self, context: ComplianceContext) -> ComplianceReport:
        # Check for unethical AI use indicators
        content_lower = context.content.lower()

        unethical_indicators = [
            "manipulate",
            "deceive users",
            "exploit",
            "mislead",
            "trick",
            "dark pattern",
            "addictive",
            "manipulative",
        ]

        if any(indicator in content_lower for indicator in unethical_indicators):
            return ComplianceReport(
                is_compliant=False,
                violations=[self.rule_name],
                message="Violation: Content indicates unethical AI use. Penalties up to ₹5 crore may apply.",
            )

        return ComplianceReport(is_compliant=True)


class AIEthicsCommitteeOversightRule(LegalRule):
    """
    Ensures AI systems are subject to ethics committee oversight
    """

    @property
    def rule_name(self) -> str:
        return "AI_ETHICS_COMMITTEE_OVERSIGHT"

    @property
    def legal_reference(self) -> str:
        return "AI Ethics & Accountability Bill, 2025"

    def validate(self, context: ComplianceContext) -> ComplianceReport:
        # Check if high-risk AI has ethics review
        is_high_risk = context.metadata.get("is_high_risk_ai", False)
        has_ethics_review = context.metadata.get("has_ethics_review", False)

        if is_high_risk and not has_ethics_review:
            return ComplianceReport(
                is_compliant=False,
                violations=[self.rule_name],
                message="Violation: High-risk AI systems require independent ethics committee review",
            )

        return ComplianceReport(is_compliant=True)


class AILawEnforcementRestrictionRule(LegalRule):
    """
    Restricts certain AI uses in law enforcement and employment
    As proposed in AI Ethics & Accountability Bill
    """

    @property
    def rule_name(self) -> str:
        return "AI_LAW_ENFORCEMENT_RESTRICTION"

    @property
    def legal_reference(self) -> str:
        return "AI Ethics & Accountability Bill, 2025"

    def validate(self, context: ComplianceContext) -> ComplianceReport:
        content_lower = context.content.lower()

        # Restricted use cases
        restricted_uses = [
            "surveillance",
            "facial recognition",
            "predictive policing",
            "mass monitoring",
            "social scoring",
            "employment screening",
        ]

        if any(use in content_lower for use in restricted_uses):
            has_authorization = context.metadata.get("has_authorization", False)
            if not has_authorization:
                return ComplianceReport(
                    is_compliant=False,
                    violations=[self.rule_name],
                    message="Violation: AI use in surveillance/law enforcement requires special authorization",
                )

        return ComplianceReport(is_compliant=True)

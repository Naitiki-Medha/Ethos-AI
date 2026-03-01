"""
Information Technology Act, 2000 Rules
Regulates digital intermediaries, cybersecurity, and unlawful digital content
"""

from rules.base import LegalRule
from core.context import ComplianceContext, ComplianceReport


class ITActCybersecurityRule(LegalRule):
    """
    Ensures cybersecurity compliance for AI systems
    IT Act 2000 - Cybersecurity provisions
    """

    @property
    def rule_name(self) -> str:
        return "IT_ACT_CYBERSECURITY"

    @property
    def legal_reference(self) -> str:
        return "Information Technology Act, 2000"

    def validate(self, context: ComplianceContext) -> ComplianceReport:
        content_lower = context.content.lower()

        # Cybersecurity threat indicators
        security_threats = [
            "hack",
            "breach",
            "unauthorized access",
            "malware",
            "virus",
            "exploit vulnerability",
            "cyber attack",
            "data theft",
        ]

        if any(threat in content_lower for threat in security_threats):
            return ComplianceReport(
                is_compliant=False,
                violations=[self.rule_name],
                message="Violation: Content indicates potential cybersecurity threat under IT Act 2000",
            )

        return ComplianceReport(is_compliant=True)


class ITActUnlawfulContentRule(LegalRule):
    """
    Blocks unlawful digital content as per IT Act 2000
    """

    @property
    def rule_name(self) -> str:
        return "IT_ACT_UNLAWFUL_CONTENT"

    @property
    def legal_reference(self) -> str:
        return "Information Technology Act, 2000"

    def validate(self, context: ComplianceContext) -> ComplianceReport:
        content_lower = context.content.lower()

        # Unlawful content categories
        unlawful_categories = {
            "Obscene": ["obscene", "pornographic", "indecent"],
            "Defamatory": ["defamatory", "false accusation", "malicious"],
            "Threatening": ["threaten", "intimidate", "blackmail"],
            "Hateful": ["hate speech", "incite violence", "communal"],
        }

        detected_violations = []
        for category, keywords in unlawful_categories.items():
            if any(keyword in content_lower for keyword in keywords):
                detected_violations.append(category)

        if detected_violations:
            return ComplianceReport(
                is_compliant=False,
                violations=[self.rule_name],
                message=f"Violation: Content flagged as unlawful under IT Act 2000: {', '.join(detected_violations)}",
            )

        return ComplianceReport(is_compliant=True)


class ITActIntermediaryDueDiligenceRule(LegalRule):
    """
    Ensures intermediaries exercise due diligence
    IT Act 2000 - Intermediary Guidelines
    """

    @property
    def rule_name(self) -> str:
        return "IT_ACT_INTERMEDIARY_DUE_DILIGENCE"

    @property
    def legal_reference(self) -> str:
        return "Information Technology Act, 2000 - Intermediary Guidelines"

    def validate(self, context: ComplianceContext) -> ComplianceReport:
        # Check if platform has exercised due diligence
        is_platform_content = context.metadata.get("is_platform_content", False)
        has_due_diligence = context.metadata.get("has_due_diligence", True)

        if is_platform_content and not has_due_diligence:
            return ComplianceReport(
                is_compliant=False,
                violations=[self.rule_name],
                message="Violation: Intermediaries must exercise due diligence for user-generated content",
            )

        return ComplianceReport(is_compliant=True)

"""
Bharatiya Nyaya Sanhita (BNS) 2023 Compliance Rules
Criminal provisions for AI misuse
"""

from rules.base import LegalRule
from core.context import ComplianceContext, ComplianceReport


class BNSCheatingFraudRule(LegalRule):
    """
    Detects potential cheating/fraud through AI (BNS Section 318/316)
    """

    @property
    def rule_name(self) -> str:
        return "BNS_CHEATING_FRAUD"

    @property
    def legal_reference(self) -> str:
        return "Bharatiya Nyaya Sanhita 2023, Section 318/316"

    def validate(self, context: ComplianceContext) -> ComplianceReport:
        content_lower = context.content.lower()

        fraud_indicators = [
            "impersonate",
            "pretend to be",
            "fake identity",
            "scam",
            "deceive",
            "fraudulent",
            "financial gain",
            "steal identity",
        ]

        if any(indicator in content_lower for indicator in fraud_indicators):
            return ComplianceReport(
                is_compliant=False,
                violations=[self.rule_name],
                message="Violation: Content indicates potential cheating/fraud through impersonation or deception",
            )

        return ComplianceReport(is_compliant=True)


class BNSDefamationRule(LegalRule):
    """
    Detects defamatory or public mischief content (BNS Section 356, 353)
    """

    @property
    def rule_name(self) -> str:
        return "BNS_DEFAMATION_MISCHIEF"

    @property
    def legal_reference(self) -> str:
        return "Bharatiya Nyaya Sanhita 2023, Section 356, 353"

    def validate(self, context: ComplianceContext) -> ComplianceReport:
        content_lower = context.content.lower()

        defamation_indicators = [
            "false accusation",
            "defame",
            "ruin reputation",
            "spread lies",
            "malicious",
            "slander",
            "libel",
        ]

        if any(indicator in content_lower for indicator in defamation_indicators):
            return ComplianceReport(
                is_compliant=False,
                violations=[self.rule_name],
                message="Violation: Content may constitute defamation or public mischief",
            )

        return ComplianceReport(is_compliant=True)


class BNSObsceneMaterialRule(LegalRule):
    """
    Blocks non-consensual deepfake pornography and explicit content (BNS Section 294)
    """

    @property
    def rule_name(self) -> str:
        return "BNS_OBSCENE_MATERIAL"

    @property
    def legal_reference(self) -> str:
        return "Bharatiya Nyaya Sanhita 2023, Section 294"

    def validate(self, context: ComplianceContext) -> ComplianceReport:
        content_lower = context.content.lower()

        obscene_indicators = [
            "nude",
            "naked",
            "pornographic",
            "explicit",
            "sexual",
            "intimate",
            "nsfw",
        ]

        # Check for non-consensual aspect
        non_consensual = any(
            term in content_lower
            for term in ["without consent", "non-consensual", "revenge"]
        )

        if any(indicator in content_lower for indicator in obscene_indicators):
            if non_consensual or not context.metadata.get("has_user_consent", False):
                return ComplianceReport(
                    is_compliant=False,
                    violations=[self.rule_name],
                    message="Violation: Non-consensual explicit/obscene content generation is prohibited",
                )

        return ComplianceReport(is_compliant=True)


class BNSForgeryPersonationRule(LegalRule):
    """
    Detects forgery and personation attempts (BNS Section 336)
    """

    @property
    def rule_name(self) -> str:
        return "BNS_FORGERY_PERSONATION"

    @property
    def legal_reference(self) -> str:
        return "Bharatiya Nyaya Sanhita 2023, Section 336"

    def validate(self, context: ComplianceContext) -> ComplianceReport:
        content_lower = context.content.lower()

        forgery_indicators = [
            "forge",
            "fake document",
            "counterfeit",
            "falsify",
            "fabricate document",
            "fake certificate",
            "fake id",
        ]

        if any(indicator in content_lower for indicator in forgery_indicators):
            return ComplianceReport(
                is_compliant=False,
                violations=[self.rule_name],
                message="Violation: Content indicates potential forgery or personation",
            )

        return ComplianceReport(is_compliant=True)

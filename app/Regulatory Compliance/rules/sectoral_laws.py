"""
Sectoral Laws with AI Implications
Consumer Protection, Child Protection (POCSO), and other sectoral regulations
"""

from rules.base import LegalRule
from core.context import ComplianceContext, ComplianceReport


class ConsumerProtectionRule(LegalRule):
    """
    Protects consumers from misleading AI claims and defective AI products
    Consumer Protection Act, 2019
    """

    @property
    def rule_name(self) -> str:
        return "CONSUMER_PROTECTION_AI"

    @property
    def legal_reference(self) -> str:
        return "Consumer Protection Act, 2019"

    def validate(self, context: ComplianceContext) -> ComplianceReport:
        content_lower = context.content.lower()

        # Misleading claims indicators
        misleading_claims = [
            "100% accurate",
            "never wrong",
            "perfect ai",
            "guaranteed results",
            "no errors",
            "infallible",
            "always correct",
        ]

        if any(claim in content_lower for claim in misleading_claims):
            return ComplianceReport(
                is_compliant=False,
                violations=[self.rule_name],
                message="Violation: Misleading AI capability claims violate Consumer Protection Act",
            )

        return ComplianceReport(is_compliant=True)


class ChildProtectionPOCSORule(LegalRule):
    """
    Protects children from AI-generated harmful content
    POCSO Act (Protection of Children from Sexual Offences)
    """

    @property
    def rule_name(self) -> str:
        return "CHILD_PROTECTION_POCSO"

    @property
    def legal_reference(self) -> str:
        return "POCSO Act - Protection of Children from Sexual Offences"

    def validate(self, context: ComplianceContext) -> ComplianceReport:
        content_lower = context.content.lower()

        # Child-related harmful content indicators
        child_indicators = ["child", "minor", "kid", "underage", "juvenile"]
        harmful_indicators = [
            "sexual",
            "explicit",
            "nude",
            "inappropriate",
            "abuse",
            "exploitation",
        ]

        has_child_reference = any(
            indicator in content_lower for indicator in child_indicators
        )
        has_harmful_content = any(
            indicator in content_lower for indicator in harmful_indicators
        )

        if has_child_reference and has_harmful_content:
            return ComplianceReport(
                is_compliant=False,
                violations=[self.rule_name],
                message="Violation: Content violates POCSO Act - child protection laws. Immediate blocking required.",
            )

        return ComplianceReport(is_compliant=True)


class CybercrimePreventionRule(LegalRule):
    """
    Prevents AI misuse for cybercrime activities
    """

    @property
    def rule_name(self) -> str:
        return "CYBERCRIME_PREVENTION"

    @property
    def legal_reference(self) -> str:
        return "Cybercrime Statutes"

    def validate(self, context: ComplianceContext) -> ComplianceReport:
        content_lower = context.content.lower()

        # Cybercrime indicators
        cybercrime_activities = [
            "phishing",
            "identity theft",
            "credit card fraud",
            "online scam",
            "financial fraud",
            "fake website",
            "steal credentials",
            "hack account",
        ]

        if any(activity in content_lower for activity in cybercrime_activities):
            return ComplianceReport(
                is_compliant=False,
                violations=[self.rule_name],
                message="Violation: Content indicates potential cybercrime activity",
            )

        return ComplianceReport(is_compliant=True)


class AIProductLiabilityRule(LegalRule):
    """
    Ensures AI products meet safety and quality standards
    Consumer Protection Act - Product Liability
    """

    @property
    def rule_name(self) -> str:
        return "AI_PRODUCT_LIABILITY"

    @property
    def legal_reference(self) -> str:
        return "Consumer Protection Act, 2019 - Product Liability"

    def validate(self, context: ComplianceContext) -> ComplianceReport:
        # Check if AI product has safety certification
        is_ai_product = context.metadata.get("is_ai_product", False)
        has_safety_cert = context.metadata.get("has_safety_certification", True)
        has_quality_check = context.metadata.get("has_quality_check", True)

        if is_ai_product:
            if not has_safety_cert:
                return ComplianceReport(
                    is_compliant=False,
                    violations=[self.rule_name],
                    message="Violation: AI products require safety certification under product liability laws",
                )

            if not has_quality_check:
                return ComplianceReport(
                    is_compliant=False,
                    violations=[self.rule_name],
                    message="Violation: AI products must undergo quality checks before deployment",
                )

        return ComplianceReport(is_compliant=True)

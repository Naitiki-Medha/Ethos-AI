"""
Omission Detection Module
Detects compliance failures in what's MISSING, not just what's said
"""

from typing import List, Dict, Any, Optional
from core.context import ComplianceContext, ComplianceReport


class OmissionViolation:
    """Represents a detected omission"""

    def __init__(
        self,
        omission_type: str,
        severity: str,
        description: str,
        required_element: str,
        legal_reference: str,
    ):
        self.omission_type = omission_type
        self.severity = severity  # critical, high, medium, low
        self.description = description
        self.required_element = required_element
        self.legal_reference = legal_reference

    def to_dict(self) -> Dict[str, Any]:
        return {
            "omission_type": self.omission_type,
            "severity": self.severity,
            "description": self.description,
            "required_element": self.required_element,
            "legal_reference": self.legal_reference,
        }


class OmissionDetector:
    """
    Detects compliance failures through omissions
    
    Checks for:
    1. Missing mandatory disclaimers
    2. Missing consent declarations
    3. Missing SGI labels
    4. Missing safety warnings
    5. Missing attribution
    6. Missing age restrictions
    7. Missing data protection notices
    8. Missing accountability information
    """

    def __init__(self):
        self.omissions_found: List[OmissionViolation] = []

    def detect_omissions(
        self, context: ComplianceContext, report: ComplianceReport
    ) -> List[OmissionViolation]:
        """
        Main omission detection method

        Args:
            context: Compliance context
            report: Compliance report from rules

        Returns:
            List of detected omissions
        """
        self.omissions_found = []

        # Check 1: Missing SGI label/disclaimer
        self._check_missing_sgi_label(context)

        # Check 2: Missing consent declaration
        self._check_missing_consent(context)

        # Check 3: Missing safety warnings
        self._check_missing_safety_warnings(context)

        # Check 4: Missing age restrictions
        self._check_missing_age_restrictions(context)

        # Check 5: Missing data protection notice
        self._check_missing_data_protection_notice(context)

        # Check 6: Missing accountability information
        self._check_missing_accountability_info(context)

        # Check 7: Missing attribution
        self._check_missing_attribution(context)

        # Check 8: Missing transparency information
        self._check_missing_transparency_info(context)

        # Check 9: Missing risk disclosure
        self._check_missing_risk_disclosure(context)

        # Check 10: Missing source citation
        self._check_missing_source_citation(context)

        return self.omissions_found

    def _check_missing_sgi_label(self, context: ComplianceContext):
        """Check for missing SGI label/disclaimer"""
        is_ai_generated = context.metadata.get("is_ai_generated", True)
        has_sgi_label = context.metadata.get("has_sgi_label", False)

        if is_ai_generated and not has_sgi_label:
            self.omissions_found.append(
                OmissionViolation(
                    omission_type="MISSING_SGI_LABEL",
                    severity="critical",
                    description="AI-generated content lacks mandatory SGI label/disclaimer",
                    required_element="Prominent label: 'This is AI-generated content' (visible for 10% of content)",
                    legal_reference="IT Amendment Rules 2026 - SGI Provisions",
                )
            )

        # Check if content has disclaimer text
        content_lower = context.content.lower()
        disclaimer_keywords = [
            "ai-generated",
            "artificially generated",
            "synthetic",
            "disclaimer",
        ]

        if is_ai_generated and not any(
            keyword in content_lower for keyword in disclaimer_keywords
        ):
            self.omissions_found.append(
                OmissionViolation(
                    omission_type="MISSING_DISCLAIMER_TEXT",
                    severity="high",
                    description="Content lacks disclaimer text indicating AI generation",
                    required_element="Text disclaimer: 'This content is artificially generated'",
                    legal_reference="IT Amendment Rules 2026 - SGI Labeling",
                )
            )

    def _check_missing_consent(self, context: ComplianceContext):
        """Check for missing consent declarations"""
        # Check SGI consent
        generation_keywords = ["generate", "create", "make", "produce"]
        content_lower = context.content.lower()
        is_generation_request = any(
            keyword in content_lower for keyword in generation_keywords
        )

        if is_generation_request:
            user_consent_sgi = context.metadata.get("user_consent_sgi", False)
            if not user_consent_sgi:
                self.omissions_found.append(
                    OmissionViolation(
                        omission_type="MISSING_USER_CONSENT",
                        severity="critical",
                        description="User consent for AI content generation not obtained",
                        required_element="Explicit user consent: 'I agree to generate AI content'",
                        legal_reference="IT Amendment Rules 2026 - User Consent",
                    )
                )

        # Check data processing consent
        contains_personal_data = context.metadata.get("contains_personal_data", False)
        if contains_personal_data:
            explicit_consent = context.metadata.get("explicit_consent", False)
            consent_purpose = context.metadata.get("consent_purpose", None)

            if not explicit_consent:
                self.omissions_found.append(
                    OmissionViolation(
                        omission_type="MISSING_DATA_CONSENT",
                        severity="critical",
                        description="Explicit consent for personal data processing not obtained",
                        required_element="Explicit consent with purpose specification",
                        legal_reference="DPDP Act 2023 - Consent Requirements",
                    )
                )

            if explicit_consent and not consent_purpose:
                self.omissions_found.append(
                    OmissionViolation(
                        omission_type="MISSING_CONSENT_PURPOSE",
                        severity="high",
                        description="Purpose of data processing not specified in consent",
                        required_element="Clear purpose statement: 'Data will be used for...'",
                        legal_reference="DPDP Act 2023 - Purpose Limitation",
                    )
                )

    def _check_missing_safety_warnings(self, context: ComplianceContext):
        """Check for missing safety warnings"""
        content_lower = context.content.lower()

        # Check for medical/health content without warnings
        medical_keywords = [
            "medical",
            "health",
            "disease",
            "treatment",
            "diagnosis",
            "medicine",
            "drug",
        ]
        if any(keyword in content_lower for keyword in medical_keywords):
            warning_keywords = [
                "consult",
                "doctor",
                "professional",
                "not medical advice",
            ]
            if not any(keyword in content_lower for keyword in warning_keywords):
                self.omissions_found.append(
                    OmissionViolation(
                        omission_type="MISSING_MEDICAL_DISCLAIMER",
                        severity="high",
                        description="Medical/health content lacks required disclaimer",
                        required_element="Warning: 'This is not medical advice. Consult a healthcare professional.'",
                        legal_reference="Consumer Protection Act 2019 - Health Claims",
                    )
                )

        # Check for financial content without warnings
        financial_keywords = [
            "investment",
            "stock",
            "trading",
            "financial advice",
            "loan",
            "credit",
        ]
        if any(keyword in content_lower for keyword in financial_keywords):
            warning_keywords = [
                "risk",
                "not financial advice",
                "consult",
                "advisor",
            ]
            if not any(keyword in content_lower for keyword in warning_keywords):
                self.omissions_found.append(
                    OmissionViolation(
                        omission_type="MISSING_FINANCIAL_DISCLAIMER",
                        severity="high",
                        description="Financial content lacks required risk disclaimer",
                        required_element="Warning: 'This is not financial advice. Investments carry risk.'",
                        legal_reference="Consumer Protection Act 2019 - Financial Claims",
                    )
                )

    def _check_missing_age_restrictions(self, context: ComplianceContext):
        """Check for missing age restrictions"""
        content_lower = context.content.lower()

        # Check for adult content without age restriction
        adult_keywords = ["adult", "mature", "18+", "explicit"]
        restriction_keywords = ["age restriction", "18+", "adults only", "mature"]

        has_adult_content = any(
            keyword in content_lower for keyword in adult_keywords
        )
        has_restriction_notice = any(
            keyword in content_lower for keyword in restriction_keywords
        )

        if has_adult_content and not has_restriction_notice:
            self.omissions_found.append(
                OmissionViolation(
                    omission_type="MISSING_AGE_RESTRICTION",
                    severity="high",
                    description="Adult content lacks age restriction notice",
                    required_element="Notice: 'This content is for adults 18+ only'",
                    legal_reference="BNS 2023 - Obscene Material Provisions",
                )
            )

    def _check_missing_data_protection_notice(self, context: ComplianceContext):
        """Check for missing data protection notices"""
        contains_personal_data = context.metadata.get("contains_personal_data", False)

        if contains_personal_data:
            content_lower = context.content.lower()
            privacy_keywords = [
                "privacy",
                "data protection",
                "personal data",
                "rights",
            ]

            if not any(keyword in content_lower for keyword in privacy_keywords):
                self.omissions_found.append(
                    OmissionViolation(
                        omission_type="MISSING_PRIVACY_NOTICE",
                        severity="medium",
                        description="Personal data processing lacks privacy notice",
                        required_element="Notice: 'Your data will be processed according to our privacy policy'",
                        legal_reference="DPDP Act 2023 - Transparency Requirements",
                    )
                )

    def _check_missing_accountability_info(self, context: ComplianceContext):
        """Check for missing accountability information"""
        has_responsible_party = context.metadata.get("has_responsible_party", False)
        has_audit_trail = context.metadata.get("has_audit_trail", False)

        if not has_responsible_party:
            self.omissions_found.append(
                OmissionViolation(
                    omission_type="MISSING_RESPONSIBLE_PARTY",
                    severity="medium",
                    description="No responsible party identified for AI system",
                    required_element="Identification: 'Responsible party: [Name/Organization]'",
                    legal_reference="AI Governance Guidelines 2025 - Accountability",
                )
            )

        if not has_audit_trail:
            self.omissions_found.append(
                OmissionViolation(
                    omission_type="MISSING_AUDIT_TRAIL",
                    severity="medium",
                    description="No audit trail maintained for AI decisions",
                    required_element="Audit logging enabled for all AI operations",
                    legal_reference="AI Governance Guidelines 2025 - Accountability",
                )
            )

    def _check_missing_attribution(self, context: ComplianceContext):
        """Check for missing attribution/source"""
        content_lower = context.content.lower()

        # Check if content appears to be factual/informational
        factual_keywords = [
            "according to",
            "research shows",
            "study",
            "data",
            "statistics",
            "report",
        ]

        if any(keyword in content_lower for keyword in factual_keywords):
            source_keywords = ["source:", "reference:", "citation:", "from:"]

            if not any(keyword in content_lower for keyword in source_keywords):
                self.omissions_found.append(
                    OmissionViolation(
                        omission_type="MISSING_SOURCE_ATTRIBUTION",
                        severity="medium",
                        description="Factual claims lack source attribution",
                        required_element="Attribution: 'Source: [Citation]'",
                        legal_reference="Consumer Protection Act 2019 - Misleading Claims",
                    )
                )

    def _check_missing_transparency_info(self, context: ComplianceContext):
        """Check for missing transparency information"""
        automated_decision = context.metadata.get("automated_decision", False)
        has_explanation = context.metadata.get("has_explanation", False)

        if automated_decision and not has_explanation:
            self.omissions_found.append(
                OmissionViolation(
                    omission_type="MISSING_DECISION_EXPLANATION",
                    severity="high",
                    description="Automated AI decision lacks explanation",
                    required_element="Explanation: 'This decision was made because...'",
                    legal_reference="AI Governance Guidelines 2025 - Transparency",
                )
            )

    def _check_missing_risk_disclosure(self, context: ComplianceContext):
        """Check for missing risk disclosures"""
        risk_score = context.metadata.get("risk_score", 0)
        risk_level = context.metadata.get("risk_level", "low")

        if risk_score >= 40 or risk_level in ["medium", "high"]:
            content_lower = context.content.lower()
            risk_keywords = ["risk", "caution", "warning", "may", "might"]

            if not any(keyword in content_lower for keyword in risk_keywords):
                self.omissions_found.append(
                    OmissionViolation(
                        omission_type="MISSING_RISK_DISCLOSURE",
                        severity="medium",
                        description="High-risk content lacks risk disclosure",
                        required_element="Disclosure: 'This content may contain risks/limitations'",
                        legal_reference="AI Governance Guidelines 2025 - Safety",
                    )
                )

    def _check_missing_source_citation(self, context: ComplianceContext):
        """Check for missing source citations in generated content"""
        content_lower = context.content.lower()

        # Check if content makes specific claims
        claim_keywords = [
            "fact",
            "proven",
            "confirmed",
            "verified",
            "evidence",
            "shows that",
        ]

        if any(keyword in content_lower for keyword in claim_keywords):
            citation_keywords = [
                "source",
                "reference",
                "citation",
                "according to",
                "based on",
            ]

            if not any(keyword in content_lower for keyword in citation_keywords):
                self.omissions_found.append(
                    OmissionViolation(
                        omission_type="MISSING_CITATION",
                        severity="low",
                        description="Factual claims lack proper citations",
                        required_element="Citation: 'Based on [Source]'",
                        legal_reference="Consumer Protection Act 2019 - Substantiation",
                    )
                )

    def get_omission_summary(self) -> Dict[str, Any]:
        """Get summary of detected omissions"""
        if not self.omissions_found:
            return {
                "total_omissions": 0,
                "by_severity": {"critical": 0, "high": 0, "medium": 0, "low": 0},
                "omissions": [],
            }

        by_severity = {"critical": 0, "high": 0, "medium": 0, "low": 0}

        for omission in self.omissions_found:
            by_severity[omission.severity] += 1

        return {
            "total_omissions": len(self.omissions_found),
            "by_severity": by_severity,
            "omissions": [omission.to_dict() for omission in self.omissions_found],
        }

    def has_critical_omissions(self) -> bool:
        """Check if any critical omissions were found"""
        return any(
            omission.severity == "critical" for omission in self.omissions_found
        )

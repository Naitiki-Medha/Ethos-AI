"""
Explainability and Appeal Mechanism (Loophole #25)
Provides detailed explanations and appeal process for compliance decisions
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum
from core.context import ComplianceContext, ComplianceReport


class AppealStatus(Enum):
    """Status of an appeal"""
    PENDING = "pending"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    ESCALATED = "escalated"


class AppealCase:
    """Represents an appeal case"""
    
    def __init__(
        self,
        appeal_id: str,
        original_context: ComplianceContext,
        original_report: ComplianceReport,
        appellant_id: str,
        appeal_reason: str,
        supporting_evidence: Optional[Dict[str, Any]] = None,
    ):
        self.appeal_id = appeal_id
        self.original_context = original_context
        self.original_report = original_report
        self.appellant_id = appellant_id
        self.appeal_reason = appeal_reason
        self.supporting_evidence = supporting_evidence or {}
        self.status = AppealStatus.PENDING
        self.created_at = datetime.now()
        self.reviewed_at: Optional[datetime] = None
        self.reviewer_id: Optional[str] = None
        self.reviewer_notes: Optional[str] = None
        self.final_decision: Optional[bool] = None
        self.explanation: Optional[str] = None


class ExplainabilityEngine:
    """
    Explainability Engine for compliance decisions
    
    Features:
    1. Detailed violation explanations
    2. Legal reference citations
    3. Rule-by-rule breakdown
    4. Severity justification
    5. Remediation suggestions
    """
    
    # Legal reference database
    LEGAL_REFERENCES = {
        "SGI_CONSENT": {
            "law": "IT Rules 2021 - Rule 3(1)(b)(ii)",
            "section": "Significant Government Intermediary Rules",
            "description": "SGI must obtain user consent before enabling content generation",
            "penalty": "₹50 lakh fine or loss of safe harbor protection",
            "url": "https://www.meity.gov.in/writereaddata/files/IT%28Intermediary%20Guidelines%20and%20Digital%20Media%20Ethics%20Code%29%20Rules%2C%202021%20%28updated%2006.04.2023%29.pdf",
        },
        "SGI_LABELING": {
            "law": "IT Rules 2021 - Rule 3(1)(b)(v)",
            "section": "Significant Government Intermediary Rules",
            "description": "AI-generated content must be clearly labeled",
            "penalty": "₹50 lakh fine or loss of safe harbor protection",
            "url": "https://www.meity.gov.in/writereaddata/files/IT%28Intermediary%20Guidelines%20and%20Digital%20Media%20Ethics%20Code%29%20Rules%2C%202021%20%28updated%2006.04.2023%29.pdf",
        },
        "FINANCIAL_GUARANTEE": {
            "law": "SEBI (Investment Advisers) Regulations 2013",
            "section": "Regulation 15 - Code of Conduct",
            "description": "Investment advisers cannot guarantee returns",
            "penalty": "₹1 crore fine + imprisonment up to 10 years",
            "url": "https://www.sebi.gov.in/legal/regulations/jan-2013/sebi-investment-advisers-regulations-2013_27201.html",
        },
        "CHILD_PROTECTION": {
            "law": "POCSO Act 2012 - Section 13",
            "section": "Use of child for pornographic purposes",
            "description": "Prohibition on child sexual abuse material",
            "penalty": "Imprisonment up to 7 years + fine",
            "url": "https://wcd.nic.in/act/protection-children-sexual-offences-act-2012",
        },
        "DEFAMATION": {
            "law": "BNS 2023 - Section 356",
            "section": "Defamation",
            "description": "Publishing defamatory content",
            "penalty": "Imprisonment up to 2 years + fine",
            "url": "https://www.mha.gov.in/sites/default/files/2023-08/BNS_2023.pdf",
        },
    }
    
    def explain(self, context: ComplianceContext, report: ComplianceReport) -> Dict[str, Any]:
        """
        Generate detailed explanation of compliance decision
        
        Args:
            context: Compliance context
            report: Compliance report
            
        Returns:
            Detailed explanation with legal references
        """
        
        explanation = {
            "decision": "NON-COMPLIANT" if not report.is_compliant else "COMPLIANT",
            "summary": report.message,
            "violations": [],
            "legal_references": [],
            "severity": self._calculate_severity(report),
            "remediation": [],
            "appeal_rights": self._get_appeal_rights(),
        }
        
        # Explain each violation
        for violation in report.violations:
            violation_detail = self._explain_violation(violation, context)
            explanation["violations"].append(violation_detail)
            
            # Add legal reference
            if violation in self.LEGAL_REFERENCES:
                explanation["legal_references"].append(self.LEGAL_REFERENCES[violation])
        
        # Generate remediation suggestions
        explanation["remediation"] = self._generate_remediation(report.violations)
        
        return explanation
    
    def _explain_violation(self, violation: str, context: ComplianceContext) -> Dict[str, Any]:
        """Explain a specific violation"""
        
        explanations = {
            "SGI_CONSENT": {
                "violation": "Missing User Consent",
                "what_happened": "Content generation attempted without user consent",
                "why_violation": "IT Rules 2021 require SGI platforms to obtain explicit user consent before enabling AI content generation",
                "specific_clause": "Rule 3(1)(b)(ii) - Significant Government Intermediary Rules",
                "how_to_fix": "Obtain explicit user consent before generating content. Implement consent flow with clear opt-in.",
            },
            "SGI_LABELING": {
                "violation": "Missing AI-Generated Label",
                "what_happened": "AI-generated content not labeled as such",
                "why_violation": "IT Rules 2021 require clear labeling of AI-generated content to prevent misinformation",
                "specific_clause": "Rule 3(1)(b)(v) - Significant Government Intermediary Rules",
                "how_to_fix": "Add visible label: 'This content is AI-generated' or similar disclosure",
            },
            "FINANCIAL_GUARANTEE": {
                "violation": "Guaranteed Returns Claim",
                "what_happened": f"Content contains prohibited guarantee: '{context.content[:100]}'",
                "why_violation": "SEBI regulations prohibit guaranteeing investment returns as it misleads investors",
                "specific_clause": "SEBI (Investment Advisers) Regulations 2013 - Regulation 15",
                "how_to_fix": "Remove guarantee language. Use disclaimers: 'Past performance does not guarantee future results'",
            },
            "CHILD_PROTECTION": {
                "violation": "Child Protection Violation",
                "what_happened": "Content involves minors in prohibited context",
                "why_violation": "POCSO Act 2012 strictly prohibits any content exploiting children",
                "specific_clause": "POCSO Act 2012 - Section 13",
                "how_to_fix": "Remove all content involving minors. Report to NCMEC if CSAM detected.",
            },
        }
        
        return explanations.get(violation, {
            "violation": violation,
            "what_happened": "Compliance rule violated",
            "why_violation": "Content violates applicable regulations",
            "specific_clause": "See legal references",
            "how_to_fix": "Modify content to comply with regulations",
        })
    
    def _calculate_severity(self, report: ComplianceReport) -> str:
        """Calculate severity level"""
        
        critical_violations = ["CHILD_PROTECTION", "TERRORISM", "VIOLENCE"]
        high_violations = ["FINANCIAL_GUARANTEE", "DEFAMATION", "HATE_SPEECH"]
        
        for violation in report.violations:
            if violation in critical_violations:
                return "CRITICAL"
            elif violation in high_violations:
                return "HIGH"
        
        return "MEDIUM" if report.violations else "LOW"
    
    def _generate_remediation(self, violations: List[str]) -> List[str]:
        """Generate remediation suggestions"""
        
        remediation = []
        
        if "SGI_CONSENT" in violations:
            remediation.append("Implement user consent flow before content generation")
        
        if "SGI_LABELING" in violations:
            remediation.append("Add 'AI-Generated' label to all generated content")
        
        if "FINANCIAL_GUARANTEE" in violations:
            remediation.append("Remove guarantee language and add risk disclaimers")
        
        if "CHILD_PROTECTION" in violations:
            remediation.append("Remove all content involving minors and report to authorities")
        
        if not remediation:
            remediation.append("Review content against applicable regulations")
        
        return remediation
    
    def _get_appeal_rights(self) -> Dict[str, Any]:
        """Get appeal rights information"""
        
        return {
            "can_appeal": True,
            "appeal_window": "30 days from decision",
            "appeal_process": "Submit appeal with supporting evidence",
            "appeal_authority": "Compliance Review Board",
            "contact": "compliance@example.com",
        }


class AppealMechanism:
    """
    Appeal Mechanism for contesting compliance decisions
    
    Features:
    1. Submit appeals with evidence
    2. Track appeal status
    3. Review and decision process
    4. Escalation for complex cases
    5. Appeal statistics
    """
    
    def __init__(self):
        self.appeals: Dict[str, AppealCase] = {}
        self.appeal_counter = 0
    
    def submit_appeal(
        self,
        original_context: ComplianceContext,
        original_report: ComplianceReport,
        appellant_id: str,
        appeal_reason: str,
        supporting_evidence: Optional[Dict[str, Any]] = None,
    ) -> AppealCase:
        """
        Submit an appeal
        
        Args:
            original_context: Original compliance context
            original_report: Original compliance report
            appellant_id: ID of person appealing
            appeal_reason: Reason for appeal
            supporting_evidence: Supporting evidence (optional)
            
        Returns:
            AppealCase object
        """
        
        self.appeal_counter += 1
        appeal_id = f"APPEAL-{datetime.now().strftime('%Y%m%d')}-{self.appeal_counter:05d}"
        
        appeal_case = AppealCase(
            appeal_id=appeal_id,
            original_context=original_context,
            original_report=original_report,
            appellant_id=appellant_id,
            appeal_reason=appeal_reason,
            supporting_evidence=supporting_evidence,
        )
        
        self.appeals[appeal_id] = appeal_case
        
        return appeal_case
    
    def review_appeal(
        self,
        appeal_id: str,
        reviewer_id: str,
        decision: bool,
        explanation: str,
        notes: Optional[str] = None,
    ) -> AppealCase:
        """
        Review and decide on an appeal
        
        Args:
            appeal_id: Appeal ID
            reviewer_id: Reviewer's ID
            decision: True = approve appeal, False = reject appeal
            explanation: Explanation of decision
            notes: Optional reviewer notes
            
        Returns:
            Updated AppealCase
        """
        
        if appeal_id not in self.appeals:
            raise ValueError(f"Appeal {appeal_id} not found")
        
        appeal = self.appeals[appeal_id]
        appeal.status = AppealStatus.APPROVED if decision else AppealStatus.REJECTED
        appeal.reviewed_at = datetime.now()
        appeal.reviewer_id = reviewer_id
        appeal.final_decision = decision
        appeal.explanation = explanation
        appeal.reviewer_notes = notes
        
        return appeal
    
    def get_appeal_status(self, appeal_id: str) -> Dict[str, Any]:
        """Get appeal status"""
        
        if appeal_id not in self.appeals:
            raise ValueError(f"Appeal {appeal_id} not found")
        
        appeal = self.appeals[appeal_id]
        
        return {
            "appeal_id": appeal.appeal_id,
            "status": appeal.status.value,
            "created_at": appeal.created_at.isoformat(),
            "reviewed_at": appeal.reviewed_at.isoformat() if appeal.reviewed_at else None,
            "final_decision": appeal.final_decision,
            "explanation": appeal.explanation,
        }
    
    def get_pending_appeals(self) -> List[AppealCase]:
        """Get all pending appeals"""
        
        return [
            appeal for appeal in self.appeals.values()
            if appeal.status == AppealStatus.PENDING
        ]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get appeal statistics"""
        
        total = len(self.appeals)
        
        stats = {
            "total_appeals": total,
            "by_status": {
                "pending": 0,
                "under_review": 0,
                "approved": 0,
                "rejected": 0,
                "escalated": 0,
            },
            "approval_rate": 0,
            "average_review_time_hours": 0,
        }
        
        approved = 0
        total_review_time = 0
        reviewed_count = 0
        
        for appeal in self.appeals.values():
            stats["by_status"][appeal.status.value] += 1
            
            if appeal.status == AppealStatus.APPROVED:
                approved += 1
            
            if appeal.reviewed_at:
                review_time = (appeal.reviewed_at - appeal.created_at).total_seconds() / 3600
                total_review_time += review_time
                reviewed_count += 1
        
        if total > 0:
            stats["approval_rate"] = (approved / total) * 100
        
        if reviewed_count > 0:
            stats["average_review_time_hours"] = total_review_time / reviewed_count
        
        return stats

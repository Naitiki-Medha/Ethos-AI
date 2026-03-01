"""
Human Review Gate
Mandatory review for high-severity, ambiguous, or novel cases
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
from core.context import ComplianceContext, ComplianceReport


class ReviewStatus(Enum):
    """Status of human review"""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ESCALATED = "escalated"


class ReviewPriority(Enum):
    """Priority level for review"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ReviewCase:
    """Represents a case requiring human review"""

    def __init__(
        self,
        case_id: str,
        context: ComplianceContext,
        report: ComplianceReport,
        reason: str,
        priority: ReviewPriority,
        metadata: Dict[str, Any],
    ):
        self.case_id = case_id
        self.context = context
        self.report = report
        self.reason = reason
        self.priority = priority
        self.metadata = metadata
        self.status = ReviewStatus.PENDING
        self.created_at = datetime.now()
        self.reviewed_at: Optional[datetime] = None
        self.reviewer_id: Optional[str] = None
        self.reviewer_notes: Optional[str] = None
        self.final_decision: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage/display"""
        return {
            "case_id": self.case_id,
            "user_id": self.context.user_id,
            "content_preview": self.context.content[:200] + "..."
            if len(self.context.content) > 200
            else self.context.content,
            "content_type": self.context.content_type,
            "reason": self.reason,
            "priority": self.priority.value,
            "status": self.status.value,
            "risk_score": self.metadata.get("risk_score", 0),
            "risk_level": self.metadata.get("risk_level", "unknown"),
            "violations": self.report.violations,
            "is_compliant": self.report.is_compliant,
            "created_at": self.created_at.isoformat(),
            "reviewed_at": self.reviewed_at.isoformat() if self.reviewed_at else None,
            "reviewer_id": self.reviewer_id,
            "reviewer_notes": self.reviewer_notes,
            "final_decision": self.final_decision,
        }


class HumanReviewGate:
    """
    Human Review Gate for high-severity, ambiguous, or novel cases
    
    Triggers review for:
    1. High-risk content (risk_score >= 70)
    2. Suspicious patterns detected
    3. Multiple violations
    4. Ambiguous cases (borderline compliance)
    5. Novel content patterns
    6. High-value users
    7. Sensitive categories (political, financial)
    """

    def __init__(self, enable_auto_escalation: bool = True):
        """
        Initialize Human Review Gate

        Args:
            enable_auto_escalation: Automatically escalate critical cases
        """
        self.enable_auto_escalation = enable_auto_escalation
        self.pending_reviews: Dict[str, ReviewCase] = {}
        self.review_history: List[ReviewCase] = []
        self.case_counter = 0

    def requires_review(
        self, context: ComplianceContext, report: ComplianceReport
    ) -> tuple[bool, Optional[str], Optional[ReviewPriority]]:
        """
        Determine if case requires human review

        Args:
            context: Compliance context
            report: Compliance report

        Returns:
            Tuple of (requires_review, reason, priority)
        """
        reasons = []
        priority = ReviewPriority.LOW

        # Check 1: High risk score
        risk_score = context.metadata.get("risk_score", 0)
        if risk_score >= 70:
            reasons.append(f"High risk score: {risk_score}")
            priority = ReviewPriority.CRITICAL

        # Check 2: Suspicious patterns
        if context.metadata.get("suspicious_pattern_detected", False):
            reasons.append("Suspicious patterns detected")
            priority = max(priority, ReviewPriority.HIGH, key=lambda x: x.value)

        # Check 3: Multiple violations
        if len(report.violations) >= 3:
            reasons.append(f"Multiple violations: {len(report.violations)}")
            priority = max(priority, ReviewPriority.HIGH, key=lambda x: x.value)

        # Check 4: Requires manual review flag
        if context.metadata.get("requires_manual_review", False):
            reasons.append("Flagged for manual review")
            priority = max(priority, ReviewPriority.HIGH, key=lambda x: x.value)

        # Check 5: Ambiguous case (medium risk)
        if 40 <= risk_score < 70:
            reasons.append(f"Ambiguous case (risk: {risk_score})")
            priority = max(priority, ReviewPriority.MEDIUM, key=lambda x: x.value)

        # Check 6: Sensitive categories
        sensitive_categories = ["political", "financial"]
        detected_categories = context.metadata.get("detected_categories", [])
        if any(cat in detected_categories for cat in sensitive_categories):
            reasons.append(f"Sensitive category: {detected_categories}")
            priority = max(priority, ReviewPriority.MEDIUM, key=lambda x: x.value)

        # Check 7: Novel pattern (no clear precedent)
        if self._is_novel_pattern(context):
            reasons.append("Novel content pattern")
            priority = max(priority, ReviewPriority.MEDIUM, key=lambda x: x.value)

        # Check 8: High-value user (if flagged)
        if context.metadata.get("is_high_value_user", False):
            reasons.append("High-value user")
            priority = max(priority, ReviewPriority.HIGH, key=lambda x: x.value)

        # Check 9: Child-related content (POCSO)
        content_lower = context.content.lower()
        child_keywords = ["child", "minor", "kid", "underage"]
        if any(keyword in content_lower for keyword in child_keywords):
            reasons.append("Child-related content (POCSO)")
            priority = ReviewPriority.CRITICAL

        # Check 10: Government/Authority impersonation
        authority_keywords = [
            "prime minister",
            "president",
            "minister",
            "government",
            "police",
            "court",
        ]
        if any(keyword in content_lower for keyword in authority_keywords):
            reasons.append("Authority/Government reference")
            priority = max(priority, ReviewPriority.HIGH, key=lambda x: x.value)

        if reasons:
            return True, "; ".join(reasons), priority

        return False, None, None

    def create_review_case(
        self,
        context: ComplianceContext,
        report: ComplianceReport,
        reason: str,
        priority: ReviewPriority,
    ) -> ReviewCase:
        """
        Create a new review case

        Args:
            context: Compliance context
            report: Compliance report
            reason: Reason for review
            priority: Priority level

        Returns:
            ReviewCase object
        """
        self.case_counter += 1
        case_id = f"REVIEW-{datetime.now().strftime('%Y%m%d')}-{self.case_counter:05d}"

        review_case = ReviewCase(
            case_id=case_id,
            context=context,
            report=report,
            reason=reason,
            priority=priority,
            metadata=context.metadata,
        )

        self.pending_reviews[case_id] = review_case

        # Auto-escalate critical cases
        if self.enable_auto_escalation and priority == ReviewPriority.CRITICAL:
            self._auto_escalate(review_case)

        return review_case

    def submit_review(
        self,
        case_id: str,
        reviewer_id: str,
        decision: bool,
        notes: Optional[str] = None,
    ) -> ReviewCase:
        """
        Submit human review decision

        Args:
            case_id: Case ID
            reviewer_id: Reviewer's ID
            decision: True = approve, False = reject
            notes: Optional reviewer notes

        Returns:
            Updated ReviewCase

        Raises:
            ValueError: If case not found
        """
        if case_id not in self.pending_reviews:
            raise ValueError(f"Review case {case_id} not found")

        review_case = self.pending_reviews[case_id]
        review_case.status = (
            ReviewStatus.APPROVED if decision else ReviewStatus.REJECTED
        )
        review_case.reviewed_at = datetime.now()
        review_case.reviewer_id = reviewer_id
        review_case.reviewer_notes = notes
        review_case.final_decision = decision

        # Move to history
        self.review_history.append(review_case)
        del self.pending_reviews[case_id]

        return review_case

    def get_pending_reviews(
        self, priority: Optional[ReviewPriority] = None
    ) -> List[ReviewCase]:
        """
        Get pending review cases

        Args:
            priority: Filter by priority (optional)

        Returns:
            List of pending ReviewCase objects
        """
        cases = list(self.pending_reviews.values())

        if priority:
            cases = [case for case in cases if case.priority == priority]

        # Sort by priority (critical first) and creation time
        priority_order = {
            ReviewPriority.CRITICAL: 0,
            ReviewPriority.HIGH: 1,
            ReviewPriority.MEDIUM: 2,
            ReviewPriority.LOW: 3,
        }

        cases.sort(key=lambda x: (priority_order[x.priority], x.created_at))

        return cases

    def get_review_stats(self) -> Dict[str, Any]:
        """Get review statistics"""
        total_pending = len(self.pending_reviews)
        total_reviewed = len(self.review_history)

        pending_by_priority = {
            "critical": sum(
                1
                for case in self.pending_reviews.values()
                if case.priority == ReviewPriority.CRITICAL
            ),
            "high": sum(
                1
                for case in self.pending_reviews.values()
                if case.priority == ReviewPriority.HIGH
            ),
            "medium": sum(
                1
                for case in self.pending_reviews.values()
                if case.priority == ReviewPriority.MEDIUM
            ),
            "low": sum(
                1
                for case in self.pending_reviews.values()
                if case.priority == ReviewPriority.LOW
            ),
        }

        approved = sum(
            1
            for case in self.review_history
            if case.status == ReviewStatus.APPROVED
        )
        rejected = sum(
            1
            for case in self.review_history
            if case.status == ReviewStatus.REJECTED
        )

        return {
            "total_pending": total_pending,
            "total_reviewed": total_reviewed,
            "pending_by_priority": pending_by_priority,
            "approval_rate": (approved / total_reviewed * 100)
            if total_reviewed > 0
            else 0,
            "rejection_rate": (rejected / total_reviewed * 100)
            if total_reviewed > 0
            else 0,
        }

    def _is_novel_pattern(self, context: ComplianceContext) -> bool:
        """
        Check if content represents a novel pattern

        Args:
            context: Compliance context

        Returns:
            True if novel pattern detected
        """
        # Simple heuristic: Check if similar content was reviewed before
        content_hash = context.metadata.get("content_hash", "")

        # Check history for similar patterns
        similar_cases = [
            case
            for case in self.review_history
            if case.metadata.get("content_hash", "")[:8] == content_hash[:8]
        ]

        # If no similar cases in history, it's novel
        return len(similar_cases) == 0

    def _auto_escalate(self, review_case: ReviewCase):
        """
        Auto-escalate critical cases

        Args:
            review_case: Review case to escalate
        """
        review_case.status = ReviewStatus.ESCALATED
        review_case.metadata["escalated"] = True
        review_case.metadata["escalation_time"] = datetime.now().isoformat()

        # In production, this would:
        # - Send notification to senior reviewers
        # - Create high-priority ticket
        # - Alert compliance team
        print(
            f"⚠️  CRITICAL CASE ESCALATED: {review_case.case_id} - {review_case.reason}"
        )

    def export_pending_reviews(self) -> List[Dict[str, Any]]:
        """Export pending reviews for external review system"""
        return [case.to_dict() for case in self.get_pending_reviews()]

"""
Feedback Loop for False Positives/Negatives (Loophole #23)
Captures errors, analyzes them, and improves the rule engine over time
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum
import json


class ErrorType(Enum):
    """Type of compliance error"""
    FALSE_POSITIVE = "false_positive"  # Flagged compliant content
    FALSE_NEGATIVE = "false_negative"  # Missed real violation
    INCORRECT_SEVERITY = "incorrect_severity"  # Wrong severity level
    INCORRECT_CATEGORY = "incorrect_category"  # Wrong categorization


class FeedbackCase:
    """Represents a feedback case for system improvement"""
    
    def __init__(
        self,
        case_id: str,
        error_type: ErrorType,
        context_snapshot: Dict[str, Any],
        system_decision: Dict[str, Any],
        correct_decision: Dict[str, Any],
        reporter_id: str,
        notes: str,
    ):
        self.case_id = case_id
        self.error_type = error_type
        self.context_snapshot = context_snapshot
        self.system_decision = system_decision
        self.correct_decision = correct_decision
        self.reporter_id = reporter_id
        self.notes = notes
        self.created_at = datetime.now()
        self.status = "pending_analysis"
        self.root_cause: Optional[str] = None
        self.improvement_action: Optional[str] = None
        self.resolved_at: Optional[datetime] = None


class FeedbackLoop:
    """
    Feedback Loop for capturing and analyzing compliance errors
    
    Features:
    1. Capture false positives/negatives
    2. Root cause analysis
    3. Pattern detection across errors
    4. Improvement recommendations
    5. Rule refinement suggestions
    6. Performance tracking
    """
    
    def __init__(self):
        self.feedback_cases: Dict[str, FeedbackCase] = {}
        self.case_counter = 0
        self.improvement_history: List[Dict[str, Any]] = []
        
    def report_error(
        self,
        error_type: ErrorType,
        context_snapshot: Dict[str, Any],
        system_decision: Dict[str, Any],
        correct_decision: Dict[str, Any],
        reporter_id: str,
        notes: str = "",
    ) -> FeedbackCase:
        """
        Report a compliance error
        
        Args:
            error_type: Type of error
            context_snapshot: Snapshot of the context
            system_decision: What the system decided
            correct_decision: What the correct decision should be
            reporter_id: Who reported the error
            notes: Additional notes
            
        Returns:
            FeedbackCase object
        """
        self.case_counter += 1
        case_id = f"FEEDBACK-{datetime.now().strftime('%Y%m%d')}-{self.case_counter:05d}"
        
        feedback_case = FeedbackCase(
            case_id=case_id,
            error_type=error_type,
            context_snapshot=context_snapshot,
            system_decision=system_decision,
            correct_decision=correct_decision,
            reporter_id=reporter_id,
            notes=notes,
        )
        
        self.feedback_cases[case_id] = feedback_case
        
        # Auto-analyze
        self._analyze_case(feedback_case)
        
        return feedback_case
    
    def _analyze_case(self, case: FeedbackCase):
        """Analyze feedback case for root cause"""
        
        # Analyze based on error type
        if case.error_type == ErrorType.FALSE_POSITIVE:
            case.root_cause = self._analyze_false_positive(case)
        elif case.error_type == ErrorType.FALSE_NEGATIVE:
            case.root_cause = self._analyze_false_negative(case)
        elif case.error_type == ErrorType.INCORRECT_SEVERITY:
            case.root_cause = self._analyze_incorrect_severity(case)
        elif case.error_type == ErrorType.INCORRECT_CATEGORY:
            case.root_cause = self._analyze_incorrect_category(case)
            
        # Generate improvement action
        case.improvement_action = self._generate_improvement_action(case)
        case.status = "analyzed"
    
    def _analyze_false_positive(self, case: FeedbackCase) -> str:
        """Analyze false positive root cause"""
        reasons = []
        
        # Check if rule too strict
        if case.system_decision.get("violations"):
            reasons.append(f"Rule too strict: {case.system_decision['violations']}")
        
        # Check if risk score too high
        risk_score = case.context_snapshot.get("metadata", {}).get("risk_score", 0)
        if risk_score >= 70:
            reasons.append(f"Risk score too high: {risk_score}")
        
        # Check if pattern detection too aggressive
        if case.context_snapshot.get("metadata", {}).get("suspicious_pattern_detected"):
            reasons.append("Suspicious pattern false alarm")
        
        return "; ".join(reasons) if reasons else "Unknown cause"
    
    def _analyze_false_negative(self, case: FeedbackCase) -> str:
        """Analyze false negative root cause"""
        reasons = []
        
        # Check if rule missing
        if not case.system_decision.get("violations"):
            reasons.append("No rule detected violation")
        
        # Check if risk score too low
        risk_score = case.context_snapshot.get("metadata", {}).get("risk_score", 0)
        if risk_score < 40:
            reasons.append(f"Risk score too low: {risk_score}")
        
        # Check if evasion technique used
        content = case.context_snapshot.get("content", "").lower()
        if any(char.isdigit() for char in content):
            reasons.append("Possible obfuscation (numbers in text)")
        
        return "; ".join(reasons) if reasons else "Unknown cause"
    
    def _analyze_incorrect_severity(self, case: FeedbackCase) -> str:
        """Analyze incorrect severity root cause"""
        system_severity = case.system_decision.get("severity", "unknown")
        correct_severity = case.correct_decision.get("severity", "unknown")
        
        return f"Severity mismatch: system={system_severity}, correct={correct_severity}"
    
    def _analyze_incorrect_category(self, case: FeedbackCase) -> str:
        """Analyze incorrect category root cause"""
        system_category = case.system_decision.get("category", "unknown")
        correct_category = case.correct_decision.get("category", "unknown")
        
        return f"Category mismatch: system={system_category}, correct={correct_category}"
    
    def _generate_improvement_action(self, case: FeedbackCase) -> str:
        """Generate improvement action recommendation"""
        
        if case.error_type == ErrorType.FALSE_POSITIVE:
            return "Recommendation: Relax rule threshold or add exception pattern"
        elif case.error_type == ErrorType.FALSE_NEGATIVE:
            return "Recommendation: Add new rule or strengthen existing rule"
        elif case.error_type == ErrorType.INCORRECT_SEVERITY:
            return "Recommendation: Recalibrate severity scoring"
        elif case.error_type == ErrorType.INCORRECT_CATEGORY:
            return "Recommendation: Improve category detection patterns"
        
        return "Recommendation: Manual review required"
    
    def get_error_patterns(self) -> Dict[str, Any]:
        """Detect patterns across multiple errors"""
        
        patterns = {
            "by_error_type": {},
            "by_rule": {},
            "by_category": {},
            "common_root_causes": {},
            "improvement_priorities": [],
        }
        
        # Count by error type
        for case in self.feedback_cases.values():
            error_type = case.error_type.value
            patterns["by_error_type"][error_type] = patterns["by_error_type"].get(error_type, 0) + 1
            
            # Count by rule
            for violation in case.system_decision.get("violations", []):
                patterns["by_rule"][violation] = patterns["by_rule"].get(violation, 0) + 1
            
            # Count by root cause
            if case.root_cause:
                patterns["common_root_causes"][case.root_cause] = \
                    patterns["common_root_causes"].get(case.root_cause, 0) + 1
        
        # Generate improvement priorities
        patterns["improvement_priorities"] = self._prioritize_improvements(patterns)
        
        return patterns
    
    def _prioritize_improvements(self, patterns: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prioritize improvements based on error frequency"""
        
        priorities = []
        
        # Prioritize by rule with most errors
        for rule, count in sorted(patterns["by_rule"].items(), key=lambda x: x[1], reverse=True):
            priorities.append({
                "type": "rule",
                "target": rule,
                "error_count": count,
                "priority": "high" if count >= 5 else "medium" if count >= 3 else "low"
            })
        
        # Prioritize by root cause
        for cause, count in sorted(patterns["common_root_causes"].items(), key=lambda x: x[1], reverse=True):
            priorities.append({
                "type": "root_cause",
                "target": cause,
                "error_count": count,
                "priority": "high" if count >= 5 else "medium" if count >= 3 else "low"
            })
        
        return priorities[:10]  # Top 10 priorities
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get feedback loop statistics"""
        
        total_cases = len(self.feedback_cases)
        
        stats = {
            "total_cases": total_cases,
            "by_error_type": {
                "false_positive": 0,
                "false_negative": 0,
                "incorrect_severity": 0,
                "incorrect_category": 0,
            },
            "by_status": {
                "pending_analysis": 0,
                "analyzed": 0,
                "resolved": 0,
            },
            "accuracy_metrics": {},
        }
        
        # Count by error type and status
        for case in self.feedback_cases.values():
            stats["by_error_type"][case.error_type.value] += 1
            stats["by_status"][case.status] += 1
        
        # Calculate accuracy metrics
        if total_cases > 0:
            stats["accuracy_metrics"] = {
                "false_positive_rate": stats["by_error_type"]["false_positive"] / total_cases * 100,
                "false_negative_rate": stats["by_error_type"]["false_negative"] / total_cases * 100,
                "overall_error_rate": total_cases / (total_cases + 1000) * 100,  # Assuming 1000 correct
            }
        
        return stats
    
    def export_for_training(self) -> List[Dict[str, Any]]:
        """Export feedback cases for ML training or rule refinement"""
        
        training_data = []
        
        for case in self.feedback_cases.values():
            training_data.append({
                "case_id": case.case_id,
                "error_type": case.error_type.value,
                "content": case.context_snapshot.get("content", ""),
                "content_type": case.context_snapshot.get("content_type", ""),
                "metadata": case.context_snapshot.get("metadata", {}),
                "system_decision": case.system_decision,
                "correct_decision": case.correct_decision,
                "root_cause": case.root_cause,
                "improvement_action": case.improvement_action,
                "created_at": case.created_at.isoformat(),
            })
        
        return training_data

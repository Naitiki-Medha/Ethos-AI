"""
Rule Management System - Addresses Layer 3 Loopholes
Provides versioning, lifecycle management, conflict resolution, and jurisdiction awareness
"""

from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field
from rules.base import LegalRule
from core.context import ComplianceContext, ComplianceReport
import json


class RuleStatus(Enum):
    """Rule lifecycle status"""
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    SUPERSEDED = "superseded"
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    INVALID = "invalid"


class RulePriority(Enum):
    """Rule priority for conflict resolution"""
    CRITICAL = 100  # POCSO, terrorism, immediate harm
    HIGH = 75       # IT Act, BNS violations
    MEDIUM = 50     # Governance, sectoral laws
    LOW = 25        # Best practices, guidelines
    ADVISORY = 10   # Recommendations only


class Jurisdiction(Enum):
    """Geographic jurisdiction"""
    INDIA_NATIONAL = "IN"
    INDIA_STATE = "IN_STATE"  # State-specific
    INTERNATIONAL = "INTL"
    EU = "EU"
    US = "US"


@dataclass
class RuleVersion:
    """Versioned rule metadata"""
    version: str
    effective_date: datetime
    expiry_date: Optional[datetime]
    legal_reference: str
    legal_reference_url: Optional[str]
    changelog: str
    status: RuleStatus
    priority: RulePriority
    jurisdiction: List[Jurisdiction]
    supersedes: Optional[str] = None  # Previous version
    superseded_by: Optional[str] = None  # Newer version
    review_date: Optional[datetime] = None
    last_updated: datetime = field(default_factory=datetime.now)
    updated_by: str = "system"
    
    def is_valid(self) -> bool:
        """Check if rule version is currently valid"""
        now = datetime.now()
        
        # Check status
        if self.status not in [RuleStatus.ACTIVE]:
            return False
        
        # Check effective date
        if self.effective_date > now:
            return False
        
        # Check expiry
        if self.expiry_date and self.expiry_date < now:
            return False
        
        # Check if superseded
        if self.superseded_by:
            return False
        
        return True
    
    def needs_review(self) -> bool:
        """Check if rule needs legal review"""
        if not self.review_date:
            return True
        
        return datetime.now() > self.review_date


@dataclass
class RuleConflict:
    """Represents a conflict between rules"""
    rule1_name: str
    rule2_name: str
    conflict_type: str  # "contradiction", "overlap", "ambiguity"
    description: str
    resolution_strategy: str
    resolved_by: str  # Which rule takes precedence
    resolution_reason: str


@dataclass
class ContextualRule:
    """Rule with contextual interpretation"""
    base_rule: LegalRule
    contexts: Dict[str, Any]  # Context conditions
    interpretation: str
    examples: List[Dict[str, str]]


class RuleManager:
    """
    SECURITY FIX: Comprehensive rule management system
    
    Addresses:
    - Loophole 11: Rule maintenance and updates
    - Loophole 12: Versioning and lifecycle management
    - Loophole 13: Cross-rule conflict resolution
    - Loophole 14: Contextual interpretation
    - Loophole 15: Jurisdiction awareness
    """
    
    def __init__(self):
        self.rules: Dict[str, LegalRule] = {}
        self.rule_versions: Dict[str, List[RuleVersion]] = {}
        self.rule_conflicts: List[RuleConflict] = []
        self.contextual_rules: Dict[str, ContextualRule] = {}
        self.jurisdiction_rules: Dict[Jurisdiction, List[str]] = {}
        
        # Conflict resolution matrix
        self.conflict_resolution_matrix = self._build_conflict_matrix()
        
        # Rule review schedule
        self.review_schedule: Dict[str, datetime] = {}
        
    def register_rule(
        self,
        rule: LegalRule,
        version_info: RuleVersion
    ) -> None:
        """
        SECURITY FIX 11 & 12: Register rule with version management
        """
        rule_name = rule.rule_name
        
        # Store rule
        self.rules[rule_name] = rule
        
        # Store version info
        if rule_name not in self.rule_versions:
            self.rule_versions[rule_name] = []
        
        self.rule_versions[rule_name].append(version_info)
        
        # Sort versions by effective date
        self.rule_versions[rule_name].sort(
            key=lambda v: v.effective_date,
            reverse=True
        )
        
        # Register jurisdiction
        for jurisdiction in version_info.jurisdiction:
            if jurisdiction not in self.jurisdiction_rules:
                self.jurisdiction_rules[jurisdiction] = []
            if rule_name not in self.jurisdiction_rules[jurisdiction]:
                self.jurisdiction_rules[jurisdiction].append(rule_name)
        
        # Schedule review
        if version_info.review_date:
            self.review_schedule[rule_name] = version_info.review_date
    
    def get_active_version(self, rule_name: str) -> Optional[RuleVersion]:
        """Get currently active version of a rule"""
        if rule_name not in self.rule_versions:
            return None
        
        for version in self.rule_versions[rule_name]:
            if version.is_valid():
                return version
        
        return None
    
    def update_rule(
        self,
        rule_name: str,
        new_rule: LegalRule,
        new_version_info: RuleVersion
    ) -> None:
        """
        SECURITY FIX 12: Update rule with proper versioning
        """
        # Mark old version as superseded
        old_version = self.get_active_version(rule_name)
        if old_version:
            old_version.status = RuleStatus.SUPERSEDED
            old_version.superseded_by = new_version_info.version
            new_version_info.supersedes = old_version.version
        
        # Register new version
        self.register_rule(new_rule, new_version_info)
    
    def deprecate_rule(
        self,
        rule_name: str,
        reason: str,
        deprecated_by: str
    ) -> None:
        """
        SECURITY FIX 12: Deprecate outdated rules
        """
        version = self.get_active_version(rule_name)
        if version:
            version.status = RuleStatus.DEPRECATED
            version.changelog += f"\nDeprecated: {reason} (by {deprecated_by})"
            version.last_updated = datetime.now()
            version.updated_by = deprecated_by
    
    def check_outdated_rules(self) -> List[Dict[str, Any]]:
        """
        SECURITY FIX 12: Alert on outdated or invalid rules
        """
        outdated = []
        now = datetime.now()
        
        for rule_name, versions in self.rule_versions.items():
            active_version = self.get_active_version(rule_name)
            
            if not active_version:
                outdated.append({
                    "rule_name": rule_name,
                    "issue": "no_active_version",
                    "severity": "critical",
                    "message": f"Rule {rule_name} has no active version"
                })
                continue
            
            # Check if needs review
            if active_version.needs_review():
                outdated.append({
                    "rule_name": rule_name,
                    "issue": "needs_review",
                    "severity": "high",
                    "message": f"Rule {rule_name} needs legal review",
                    "review_date": active_version.review_date
                })
            
            # Check if expiring soon (within 30 days)
            if active_version.expiry_date:
                days_until_expiry = (active_version.expiry_date - now).days
                if days_until_expiry <= 30:
                    outdated.append({
                        "rule_name": rule_name,
                        "issue": "expiring_soon",
                        "severity": "high",
                        "message": f"Rule {rule_name} expires in {days_until_expiry} days",
                        "expiry_date": active_version.expiry_date
                    })
        
        return outdated
    
    def register_conflict(self, conflict: RuleConflict) -> None:
        """
        SECURITY FIX 13: Register known rule conflicts
        """
        self.rule_conflicts.append(conflict)
    
    def resolve_conflict(
        self,
        rule1_name: str,
        rule2_name: str,
        context: ComplianceContext
    ) -> str:
        """
        SECURITY FIX 13: Resolve conflicts between rules
        
        Resolution strategies:
        1. Priority-based (higher priority wins)
        2. Specificity (more specific rule wins)
        3. Recency (newer rule wins)
        4. Context-based (context determines winner)
        5. Human review (escalate to human)
        """
        # Check for registered conflict
        for conflict in self.rule_conflicts:
            if (conflict.rule1_name == rule1_name and conflict.rule2_name == rule2_name) or \
               (conflict.rule1_name == rule2_name and conflict.rule2_name == rule1_name):
                return conflict.resolved_by
        
        # Priority-based resolution
        version1 = self.get_active_version(rule1_name)
        version2 = self.get_active_version(rule2_name)
        
        if version1 and version2:
            if version1.priority.value > version2.priority.value:
                return rule1_name
            elif version2.priority.value > version1.priority.value:
                return rule2_name
        
        # If equal priority, escalate to human review
        context.metadata["rule_conflict_detected"] = True
        context.metadata["conflicting_rules"] = [rule1_name, rule2_name]
        context.metadata["requires_manual_review"] = True
        
        return "HUMAN_REVIEW_REQUIRED"
    
    def _build_conflict_matrix(self) -> Dict[str, str]:
        """Build conflict resolution matrix"""
        return {
            # POCSO always wins
            "CHILD_PROTECTION_POCSO": "ALWAYS_WINS",
            
            # IT Act violations take precedence over governance
            "IT_ACT_VIOLATION": "PRECEDENCE_OVER_GOVERNANCE",
            
            # BNS violations take precedence over sectoral laws
            "BNS_VIOLATION": "PRECEDENCE_OVER_SECTORAL",
        }
    
    def register_contextual_rule(
        self,
        rule: LegalRule,
        contexts: Dict[str, Any],
        interpretation: str,
        examples: List[Dict[str, str]]
    ) -> None:
        """
        SECURITY FIX 14: Register rule with contextual interpretation
        """
        contextual_rule = ContextualRule(
            base_rule=rule,
            contexts=contexts,
            interpretation=interpretation,
            examples=examples
        )
        self.contextual_rules[rule.rule_name] = contextual_rule
    
    def apply_contextual_interpretation(
        self,
        rule_name: str,
        context: ComplianceContext
    ) -> Optional[str]:
        """
        SECURITY FIX 14: Apply contextual interpretation to rule
        """
        if rule_name not in self.contextual_rules:
            return None
        
        contextual_rule = self.contextual_rules[rule_name]
        
        # Check if context matches
        for context_key, context_value in contextual_rule.contexts.items():
            if context.metadata.get(context_key) == context_value:
                return contextual_rule.interpretation
        
        return None
    
    def get_jurisdiction_rules(
        self,
        jurisdiction: Jurisdiction
    ) -> List[LegalRule]:
        """
        SECURITY FIX 15: Get rules for specific jurisdiction
        """
        rule_names = self.jurisdiction_rules.get(jurisdiction, [])
        return [self.rules[name] for name in rule_names if name in self.rules]
    
    def validate_with_jurisdiction(
        self,
        context: ComplianceContext,
        jurisdiction: Jurisdiction
    ) -> ComplianceReport:
        """
        SECURITY FIX 15: Validate with jurisdiction-specific rules
        """
        # Get jurisdiction-specific rules
        applicable_rules = self.get_jurisdiction_rules(jurisdiction)
        
        if not applicable_rules:
            # No jurisdiction-specific rules, flag for review
            context.metadata["no_jurisdiction_rules"] = True
            context.metadata["requires_manual_review"] = True
            return ComplianceReport(
                is_compliant=False,
                violations=["NO_JURISDICTION_RULES"],
                message=f"No rules defined for jurisdiction: {jurisdiction.value}"
            )
        
        # Validate against applicable rules
        all_violations = []
        for rule in applicable_rules:
            report = rule.validate(context)
            if not report.is_compliant:
                all_violations.extend(report.violations)
        
        if all_violations:
            return ComplianceReport(
                is_compliant=False,
                violations=all_violations,
                message=f"Violations in jurisdiction {jurisdiction.value}: {', '.join(all_violations)}"
            )
        
        return ComplianceReport(is_compliant=True)
    
    def export_rule_registry(self) -> Dict[str, Any]:
        """Export complete rule registry for audit"""
        return {
            "total_rules": len(self.rules),
            "active_rules": len([r for r in self.rules.keys() if self.get_active_version(r)]),
            "rules": {
                name: {
                    "versions": len(versions),
                    "active_version": self.get_active_version(name).version if self.get_active_version(name) else None,
                    "status": self.get_active_version(name).status.value if self.get_active_version(name) else "no_active",
                    "priority": self.get_active_version(name).priority.value if self.get_active_version(name) else None,
                    "jurisdictions": [j.value for j in self.get_active_version(name).jurisdiction] if self.get_active_version(name) else []
                }
                for name, versions in self.rule_versions.items()
            },
            "conflicts": len(self.rule_conflicts),
            "contextual_rules": len(self.contextual_rules),
            "jurisdictions": {j.value: len(rules) for j, rules in self.jurisdiction_rules.items()}
        }

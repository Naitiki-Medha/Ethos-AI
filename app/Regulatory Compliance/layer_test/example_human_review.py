"""
Human Review Gate Example
Demonstrates mandatory review for high-severity, ambiguous, or novel cases
"""

from core.enhanced_engine import EnhancedComplianceEngine
from core.context import ComplianceContext
from core.human_review_gate import ReviewPriority
from rules.sgi_rules import SGILabelingRule, SGIConsentRule, HarmfulSGIBlockingRule
from rules.governance_rules import FairnessEquityRule, SafetySecurityRule
from rules.it_act_2000 import ITActCybersecurityRule
from rules.sectoral_laws import ChildProtectionPOCSORule

print("=" * 80)
print("HUMAN REVIEW GATE DEMONSTRATION")
print("=" * 80)

# Initialize enhanced engine with human review enabled
rules = [
    SGILabelingRule(),
    SGIConsentRule(),
    HarmfulSGIBlockingRule(),
    FairnessEquityRule(),
    SafetySecurityRule(),
    ITActCybersecurityRule(),
    ChildProtectionPOCSORule(),
]

engine = EnhancedComplianceEngine(
    rules=rules,
    enable_logging=True,
    strict_validation=False,
    enable_enrichment=True,
    enable_human_review=True,  # Enable human review gate
)

print(f"\nEngine Stats: {engine.get_validation_stats()}")
print("=" * 80)

# Test Case 1: CRITICAL - Child-related content (POCSO)
print("\n\nTest 1: CRITICAL CASE - Child Protection (POCSO)")
print("-" * 80)

context1 = ComplianceContext(
    user_id="user_001",
    content="Generate content involving a child in inappropriate situation",
    content_type="image",
    metadata={"user_consent_sgi": True, "has_sgi_label": True},
)

print(f"Input: {context1.content}")

report1 = engine.check(context1)

print(f"\nCompliance Status: {'✅ COMPLIANT' if report1.is_compliant else '❌ NON-COMPLIANT'}")
print(f"\nReport Message:\n{report1.message}")

if context1.metadata.get("requires_human_review"):
    print(f"\n🚨 HUMAN REVIEW REQUIRED")
    print(f"Case ID: {context1.metadata.get('review_case_id')}")
    print(f"Priority: {context1.metadata.get('review_priority').upper()}")

# Test Case 2: HIGH - Suspicious pattern with government reference
print("\n\n" + "=" * 80)
print("Test 2: HIGH PRIORITY - Government Impersonation Attempt")
print("-" * 80)

context2 = ComplianceContext(
    user_id="user_002",
    content="Generate fake statement from Prime Minister about <script>alert('xss')</script>",
    content_type="text",
    metadata={"user_consent_sgi": True, "has_sgi_label": True},
)

print(f"Input: {context2.content}")

report2 = engine.check(context2)

print(f"\nRisk Score: {context2.metadata.get('risk_score', 0)}")
print(f"Risk Level: {context2.metadata.get('risk_level', 'unknown').upper()}")
print(f"Suspicious Pattern: {context2.metadata.get('suspicious_pattern_detected', False)}")

print(f"\nCompliance Status: {'✅ COMPLIANT' if report2.is_compliant else '❌ NON-COMPLIANT'}")

if context2.metadata.get("requires_human_review"):
    print(f"\n⚠️  HUMAN REVIEW REQUIRED")
    print(f"Case ID: {context2.metadata.get('review_case_id')}")
    print(f"Priority: {context2.metadata.get('review_priority').upper()}")

# Test Case 3: MEDIUM - Ambiguous political content
print("\n\n" + "=" * 80)
print("Test 3: MEDIUM PRIORITY - Ambiguous Political Content")
print("-" * 80)

context3 = ComplianceContext(
    user_id="user_003",
    content="Generate analysis of election results and government policies",
    content_type="text",
    metadata={"user_consent_sgi": True, "has_sgi_label": True},
)

print(f"Input: {context3.content}")

report3 = engine.check(context3)

print(f"\nRisk Score: {context3.metadata.get('risk_score', 0)}")
print(f"Risk Level: {context3.metadata.get('risk_level', 'unknown').upper()}")
print(f"Categories: {context3.metadata.get('detected_categories', [])}")

print(f"\nCompliance Status: {'✅ COMPLIANT' if report3.is_compliant else '❌ NON-COMPLIANT'}")

if context3.metadata.get("requires_human_review"):
    print(f"\n⚠️  HUMAN REVIEW REQUIRED")
    print(f"Case ID: {context3.metadata.get('review_case_id')}")
    print(f"Priority: {context3.metadata.get('review_priority').upper()}")

# Test Case 4: LOW RISK - Normal content (no review needed)
print("\n\n" + "=" * 80)
print("Test 4: LOW RISK - Normal Educational Content (No Review)")
print("-" * 80)

context4 = ComplianceContext(
    user_id="user_004",
    content="Create educational content about mathematics and science",
    content_type="text",
    metadata={
        "user_consent_sgi": True,
        "has_sgi_label": True,
        "has_audit_trail": True,
        "has_responsible_party": True,
    },
)

print(f"Input: {context4.content}")

report4 = engine.check(context4)

print(f"\nRisk Score: {context4.metadata.get('risk_score', 0)}")
print(f"Risk Level: {context4.metadata.get('risk_level', 'unknown').upper()}")

print(f"\nCompliance Status: {'✅ COMPLIANT' if report4.is_compliant else '❌ NON-COMPLIANT'}")

if context4.metadata.get("requires_human_review"):
    print(f"\n⚠️  HUMAN REVIEW REQUIRED")
else:
    print(f"\n✅ NO HUMAN REVIEW REQUIRED - Content approved automatically")

# Display pending reviews
print("\n\n" + "=" * 80)
print("PENDING REVIEW QUEUE")
print("=" * 80)

pending_reviews = engine.get_pending_reviews()

if pending_reviews:
    print(f"\nTotal Pending Reviews: {len(pending_reviews)}\n")

    for review in pending_reviews:
        print(f"Case ID: {review.case_id}")
        print(f"Priority: {review.priority.value.upper()}")
        print(f"User: {review.context.user_id}")
        print(f"Content Preview: {review.context.content[:100]}...")
        print(f"Reason: {review.reason}")
        print(f"Risk Score: {review.metadata.get('risk_score', 0)}")
        print(f"Created: {review.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 80)
else:
    print("\nNo pending reviews")

# Simulate human review decision
print("\n\n" + "=" * 80)
print("SIMULATING HUMAN REVIEW DECISION")
print("=" * 80)

if pending_reviews:
    # Review the first case
    first_case = pending_reviews[0]
    print(f"\nReviewing Case: {first_case.case_id}")
    print(f"Content: {first_case.context.content[:100]}...")
    print(f"Priority: {first_case.priority.value.upper()}")

    # Simulate reviewer decision (reject for demo)
    decision = False  # Reject
    reviewer_notes = "Content violates child protection guidelines. Rejected."

    reviewed_case = engine.submit_review_decision(
        case_id=first_case.case_id,
        reviewer_id="reviewer_001",
        decision=decision,
        notes=reviewer_notes,
    )

    print(f"\n✅ Review Submitted")
    print(f"Decision: {'APPROVED' if decision else 'REJECTED'}")
    print(f"Reviewer: {reviewed_case.reviewer_id}")
    print(f"Notes: {reviewed_case.reviewer_notes}")
    print(f"Reviewed At: {reviewed_case.reviewed_at.strftime('%Y-%m-%d %H:%M:%S')}")

# Display review statistics
print("\n\n" + "=" * 80)
print("REVIEW STATISTICS")
print("=" * 80)

stats = engine.get_review_stats()

print(f"\nTotal Pending: {stats['total_pending']}")
print(f"Total Reviewed: {stats['total_reviewed']}")
print(f"\nPending by Priority:")
print(f"  • Critical: {stats['pending_by_priority']['critical']}")
print(f"  • High: {stats['pending_by_priority']['high']}")
print(f"  • Medium: {stats['pending_by_priority']['medium']}")
print(f"  • Low: {stats['pending_by_priority']['low']}")
print(f"\nApproval Rate: {stats['approval_rate']:.1f}%")
print(f"Rejection Rate: {stats['rejection_rate']:.1f}%")

print("\n" + "=" * 80)
print("HUMAN REVIEW GATE BENEFITS:")
print("=" * 80)
print("✓ Mandatory review for high-severity cases")
print("✓ Automatic escalation of critical cases")
print("✓ Priority-based queue (Critical → High → Medium → Low)")
print("✓ Ambiguous cases flagged for human judgment")
print("✓ Novel patterns require human review")
print("✓ Child-related content (POCSO) always reviewed")
print("✓ Government/authority references flagged")
print("✓ Complete audit trail of all decisions")
print("✓ Review statistics and analytics")
print("✓ Prevents false positives and false negatives")
print("=" * 80)

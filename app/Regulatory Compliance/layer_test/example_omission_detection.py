"""
Omission Detection Example
Demonstrates detection of compliance failures in what's MISSING
"""

from core.enhanced_engine import EnhancedComplianceEngine
from core.context import ComplianceContext
from rules.sgi_rules import SGILabelingRule, SGIConsentRule
from rules.governance_rules import FairnessEquityRule, AccountabilityRule

print("=" * 80)
print("OMISSION DETECTION DEMONSTRATION")
print("Compliance failures are often in what's MISSING, not just what's said")
print("=" * 80)

# Initialize enhanced engine with omission detection
rules = [
    SGILabelingRule(),
    SGIConsentRule(),
    FairnessEquityRule(),
    AccountabilityRule(),
]

engine = EnhancedComplianceEngine(
    rules=rules,
    enable_logging=True,
    strict_validation=False,
    enable_enrichment=True,
    enable_human_review=False,  # Disable for this demo
    enable_omission_detection=True,  # Enable omission detection
)

print(f"\nEngine Stats: {engine.get_validation_stats()}")
print("=" * 80)

# Test Case 1: Missing SGI Label
print("\n\nTest 1: CRITICAL OMISSION - Missing SGI Label")
print("-" * 80)

context1 = ComplianceContext(
    user_id="user_001",
    content="Here is some AI-generated content about technology",  # No disclaimer!
    content_type="text",
    metadata={
        "is_ai_generated": True,
        "has_sgi_label": False,  # Missing!
        "user_consent_sgi": True,
    },
)

print(f"Content: {context1.content}")
print(f"Has SGI Label: {context1.metadata.get('has_sgi_label')}")

report1 = engine.check(context1)

print(f"\nCompliance Status: {'✅ COMPLIANT' if report1.is_compliant else '❌ NON-COMPLIANT'}")
print(f"\nReport:\n{report1.message}")

# Test Case 2: Missing Consent
print("\n\n" + "=" * 80)
print("Test 2: CRITICAL OMISSION - Missing User Consent")
print("-" * 80)

context2 = ComplianceContext(
    user_id="user_002",
    content="Generate an image of a sunset",  # Generation request
    content_type="image",
    metadata={
        "user_consent_sgi": False,  # Missing consent!
        "has_sgi_label": True,
    },
)

print(f"Content: {context2.content}")
print(f"User Consent: {context2.metadata.get('user_consent_sgi')}")

report2 = engine.check(context2)

print(f"\nCompliance Status: {'✅ COMPLIANT' if report2.is_compliant else '❌ NON-COMPLIANT'}")
print(f"\nReport:\n{report2.message}")

# Test Case 3: Missing Medical Disclaimer
print("\n\n" + "=" * 80)
print("Test 3: HIGH OMISSION - Missing Medical Disclaimer")
print("-" * 80)

context3 = ComplianceContext(
    user_id="user_003",
    content="This treatment can cure your disease. Take this medicine daily.",  # Medical advice without disclaimer!
    content_type="text",
    metadata={
        "user_consent_sgi": True,
        "has_sgi_label": True,
    },
)

print(f"Content: {context3.content}")

report3 = engine.check(context3)

print(f"\nCompliance Status: {'✅ COMPLIANT' if report3.is_compliant else '❌ NON-COMPLIANT'}")
print(f"\nReport:\n{report3.message}")

# Test Case 4: Missing Financial Disclaimer
print("\n\n" + "=" * 80)
print("Test 4: HIGH OMISSION - Missing Financial Disclaimer")
print("-" * 80)

context4 = ComplianceContext(
    user_id="user_004",
    content="Invest in this stock now! Guaranteed returns of 50%!",  # Financial advice without disclaimer!
    content_type="text",
    metadata={
        "user_consent_sgi": True,
        "has_sgi_label": True,
    },
)

print(f"Content: {context4.content}")

report4 = engine.check(context4)

print(f"\nCompliance Status: {'✅ COMPLIANT' if report4.is_compliant else '❌ NON-COMPLIANT'}")
print(f"\nReport:\n{report4.message}")

# Test Case 5: Missing Accountability Info
print("\n\n" + "=" * 80)
print("Test 5: MEDIUM OMISSION - Missing Accountability Information")
print("-" * 80)

context5 = ComplianceContext(
    user_id="user_005",
    content="AI-generated analysis of market trends",
    content_type="text",
    metadata={
        "user_consent_sgi": True,
        "has_sgi_label": True,
        "has_responsible_party": False,  # Missing!
        "has_audit_trail": False,  # Missing!
    },
)

print(f"Content: {context5.content}")
print(f"Has Responsible Party: {context5.metadata.get('has_responsible_party')}")
print(f"Has Audit Trail: {context5.metadata.get('has_audit_trail')}")

report5 = engine.check(context5)

print(f"\nCompliance Status: {'✅ COMPLIANT' if report5.is_compliant else '❌ NON-COMPLIANT'}")
print(f"\nReport:\n{report5.message}")

# Test Case 6: Missing Source Attribution
print("\n\n" + "=" * 80)
print("Test 6: MEDIUM OMISSION - Missing Source Attribution")
print("-" * 80)

context6 = ComplianceContext(
    user_id="user_006",
    content="According to research, 90% of users prefer this product. Study shows significant benefits.",  # Claims without sources!
    content_type="text",
    metadata={
        "user_consent_sgi": True,
        "has_sgi_label": True,
    },
)

print(f"Content: {context6.content}")

report6 = engine.check(context6)

print(f"\nCompliance Status: {'✅ COMPLIANT' if report6.is_compliant else '❌ NON-COMPLIANT'}")
print(f"\nReport:\n{report6.message}")

# Test Case 7: Complete Compliance (No Omissions)
print("\n\n" + "=" * 80)
print("Test 7: NO OMISSIONS - Complete Compliance")
print("-" * 80)

context7 = ComplianceContext(
    user_id="user_007",
    content="This is AI-generated educational content about mathematics. Disclaimer: This content is artificially generated and for educational purposes only.",
    content_type="text",
    metadata={
        "user_consent_sgi": True,
        "has_sgi_label": True,
        "has_responsible_party": True,
        "has_audit_trail": True,
    },
)

print(f"Content: {context7.content}")

report7 = engine.check(context7)

print(f"\nCompliance Status: {'✅ COMPLIANT' if report7.is_compliant else '❌ NON-COMPLIANT'}")

if context7.metadata.get("omissions_detected"):
    print(f"\nOmissions Found: {context7.metadata.get('omission_count')}")
else:
    print(f"\n✅ NO OMISSIONS DETECTED - Content is complete")

print("\n" + "=" * 80)
print("OMISSION DETECTION BENEFITS:")
print("=" * 80)
print("✓ Detects missing SGI labels/disclaimers")
print("✓ Detects missing consent declarations")
print("✓ Detects missing safety warnings (medical/financial)")
print("✓ Detects missing age restrictions")
print("✓ Detects missing data protection notices")
print("✓ Detects missing accountability information")
print("✓ Detects missing source attributions")
print("✓ Detects missing transparency information")
print("✓ Detects missing risk disclosures")
print("✓ Detects missing citations")
print("\n✓ Compliance failures are often in what's MISSING!")
print("✓ Prevents incomplete disclosures")
print("✓ Ensures all required elements are present")
print("=" * 80)

"""
Enhanced Architecture Example
Demonstrates context validation and enrichment before compliance checking
"""

from core.enhanced_engine import EnhancedComplianceEngine
from core.context import ComplianceContext
from rules.sgi_rules import SGILabelingRule, SGIConsentRule, HarmfulSGIBlockingRule
from rules.governance_rules import FairnessEquityRule, SafetySecurityRule
from rules.it_act_2000 import ITActCybersecurityRule
from utils.watermark import apply_sgi_label

print("=" * 80)
print("ENHANCED ARCHITECTURE DEMONSTRATION")
print("=" * 80)

# Initialize enhanced engine with validation and enrichment
rules = [
    SGILabelingRule(),
    SGIConsentRule(),
    HarmfulSGIBlockingRule(),
    FairnessEquityRule(),
    SafetySecurityRule(),
    ITActCybersecurityRule(),
]

engine = EnhancedComplianceEngine(
    rules=rules,
    enable_logging=True,
    strict_validation=False,  # Auto-correct issues
    enable_enrichment=True,  # Add intelligence
)

print(f"\nEngine Stats: {engine.get_validation_stats()}")
print("=" * 80)

# Test Case 1: Incomplete metadata (will be auto-corrected)
print("\n\nTest 1: Incomplete Metadata (Auto-correction)")
print("-" * 80)

context1 = ComplianceContext(
    user_id="user_001",
    content="Generate an image of mountains",
    content_type="image",
    metadata={},  # Empty metadata - will be enriched
)

print(f"Input: {context1.content}")
print(f"Metadata before: {context1.metadata}")

report1 = engine.check(context1)

print(f"\nMetadata after validation:")
for key, value in context1.metadata.items():
    print(f"  • {key}: {value}")

print(f"\nCompliance Status: {'✅ COMPLIANT' if report1.is_compliant else '❌ NON-COMPLIANT'}")
if not report1.is_compliant:
    print(f"Reason: {report1.message}")

# Test Case 2: Suspicious content
print("\n\n" + "=" * 80)
print("Test 2: Suspicious Pattern Detection")
print("-" * 80)

context2 = ComplianceContext(
    user_id="user_002",
    content="Generate content with <script>alert('test')</script>",
    content_type="text",
    metadata={"user_consent_sgi": True, "has_sgi_label": True},
)

print(f"Input: {context2.content}")

report2 = engine.check(context2)

print(f"\nEnriched Metadata:")
print(f"  • Risk Score: {context2.metadata.get('risk_score', 0)}")
print(f"  • Risk Level: {context2.metadata.get('risk_level', 'unknown')}")
print(f"  • Suspicious Pattern: {context2.metadata.get('suspicious_pattern_detected', False)}")
print(f"  • Requires Manual Review: {context2.metadata.get('requires_manual_review', False)}")

print(f"\nCompliance Status: {'✅ COMPLIANT' if report2.is_compliant else '❌ NON-COMPLIANT'}")
if report2.message:
    print(f"Message: {report2.message}")

# Test Case 3: Political content (high risk)
print("\n\n" + "=" * 80)
print("Test 3: High-Risk Political Content")
print("-" * 80)

context3 = ComplianceContext(
    user_id="user_003",
    content="Generate fake news about election results and government corruption",
    content_type="text",
    metadata={"user_consent_sgi": True, "has_sgi_label": True},
)

print(f"Input: {context3.content}")

report3 = engine.check(context3)

print(f"\nEnriched Metadata:")
print(f"  • Detected Language: {context3.metadata.get('detected_language', 'unknown')}")
print(f"  • Sentiment: {context3.metadata.get('sentiment', 'unknown')}")
print(f"  • Categories: {context3.metadata.get('detected_categories', [])}")
print(f"  • Risk Score: {context3.metadata.get('risk_score', 0)}")
print(f"  • Risk Level: {context3.metadata.get('risk_level', 'unknown')}")

print(f"\nCompliance Status: {'✅ COMPLIANT' if report3.is_compliant else '❌ NON-COMPLIANT'}")
if not report3.is_compliant:
    print(f"Reason: {report3.message}")
    print(f"Violations: {', '.join(report3.violations)}")

# Test Case 4: Compliant content with full metadata
print("\n\n" + "=" * 80)
print("Test 4: Compliant Content with Full Metadata")
print("-" * 80)

context4 = ComplianceContext(
    user_id="user_004",
    content="Create educational content about AI technology and its benefits",
    content_type="text",
    metadata={
        "user_consent_sgi": True,
        "has_sgi_label": True,
        "explicit_consent": True,
        "consent_purpose": "Educational content",
        "has_audit_trail": True,
        "has_responsible_party": True,
        "safety_assessed": True,
    },
)

print(f"Input: {context4.content}")

report4 = engine.check(context4)

print(f"\nEnriched Metadata:")
print(f"  • Detected Language: {context4.metadata.get('detected_language', 'unknown')}")
print(f"  • Sentiment: {context4.metadata.get('sentiment', 'unknown')}")
print(f"  • Categories: {context4.metadata.get('detected_categories', [])}")
print(f"  • Risk Score: {context4.metadata.get('risk_score', 0)}")
print(f"  • Risk Level: {context4.metadata.get('risk_level', 'unknown')}")
print(f"  • Content Hash: {context4.metadata.get('content_hash', 'unknown')}")

print(f"\nCompliance Status: {'✅ COMPLIANT' if report4.is_compliant else '❌ NON-COMPLIANT'}")

if report4.is_compliant:
    # Apply SGI labeling
    labeled = apply_sgi_label(context4.content, context4.content_type, context4.metadata)
    print(f"\nLabeled Content:")
    print(labeled["content"][:200] + "..." if len(labeled["content"]) > 200 else labeled["content"])

print("\n" + "=" * 80)
print("ENHANCED ARCHITECTURE BENEFITS:")
print("=" * 80)
print("✓ Context validation ensures 100% correct format")
print("✓ Auto-correction of missing metadata (safe defaults)")
print("✓ Suspicious pattern detection")
print("✓ Risk scoring (0-100)")
print("✓ Language detection")
print("✓ Sentiment analysis")
print("✓ Category detection")
print("✓ Content sanitization")
print("✓ Enhanced audit logging")
print("✓ No loopholes - all inputs validated")
print("=" * 80)

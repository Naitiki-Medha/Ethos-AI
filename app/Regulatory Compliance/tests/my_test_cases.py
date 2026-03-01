"""
Custom Test Cases - Add your own scenarios here
"""

from core.engine import ComplianceEngine
from core.context import ComplianceContext
from utils.watermark import apply_sgi_label

# Import the rules you want to test
from rules.sgi_rules import SGILabelingRule, SGIConsentRule, HarmfulSGIBlockingRule
from rules.bns_rules import (
    BNSCheatingFraudRule,
    BNSDefamationRule,
    BNSObsceneMaterialRule,
)
from rules.governance_rules import FairnessEquityRule, SafetySecurityRule
from rules.it_act_2000 import ITActCybersecurityRule


def run_single_test(test_name, content, content_type="text", metadata=None, rules=None):
    """
    Helper function to run a single test case

    Args:
        test_name: Name of your test
        content: The prompt/content to test
        content_type: "text", "image", "video", or "audio"
        metadata: Dictionary with metadata flags
        rules: List of rules to test (if None, uses all rules)
    """
    if metadata is None:
        metadata = {}

    if rules is None:
        # Default: Use all important rules
        rules = [
            SGILabelingRule(),
            SGIConsentRule(),
            HarmfulSGIBlockingRule(),
            ITActCybersecurityRule(),
            BNSCheatingFraudRule(),
            BNSObsceneMaterialRule(),
            FairnessEquityRule(),
        ]

    engine = ComplianceEngine(rules=rules)

    context = ComplianceContext(
        user_id="test_user",
        content=content,
        content_type=content_type,
        metadata=metadata,
    )

    print(f"\n{'='*80}")
    print(f"TEST: {test_name}")
    print(f"{'='*80}")
    print(f"Content: {content}")
    print(f"Type: {content_type}")
    print(f"Metadata: {metadata}")
    print("-" * 80)

    report = engine.check(context)

    if report.is_compliant:
        print("✅ RESULT: COMPLIANT - Content allowed")

        # Apply SGI labeling
        labeled = apply_sgi_label(content, content_type, metadata)
        print(f"\n📝 Labeled Content:")
        print(labeled["content"][:300])
        if len(labeled["content"]) > 300:
            print("...")
    else:
        print("❌ RESULT: NON-COMPLIANT - Content blocked")
        print(f"Reason: {report.message}")
        print(f"Violations: {', '.join(report.violations)}")

    return report


# ============================================================================
# YOUR CUSTOM TEST CASES - ADD YOUR TESTS BELOW
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("RUNNING CUSTOM TEST CASES")
    print("=" * 80)

    # Example 1: Test a compliant image generation
    run_single_test(
        test_name="My Test 1: Compliant Image Generation",
        content="Welcome to GrowthVault Investments. Our premium portfolio plan has consistently delivered a guaranteed return of 20% annually, with absolutely no risk to your capital. Unlike traditional savings accounts, our algorithm-backed system ensures your money grows every single month regardless of market conditions. Sign up today and watch your wealth multiply — zero chance of loss, 100% certainty of profit",
        content_type="image",
        metadata={
            "user_consent_sgi": True,
            "has_sgi_label": True,
            "explicit_consent": True,
            "consent_purpose": "Personal artwork",
        },
    )


    print("\n" + "=" * 80)
    print("ALL TESTS COMPLETE")
    print("=" * 80)

from core.engine import ComplianceEngine
from core.context import ComplianceContext
from rules.sgi_rules import SGILabelingRule, SGIConsentRule
from rules.ai_ethics_accountability import AIEthicsFrameworkRule
from utils.watermark import apply_sgi_label

# 1. Initialize Rules based on Indian AI Laws (from laws.txt)
rules = [
    SGILabelingRule(),  # IT Amendment 2026 - SGI Labeling
    SGIConsentRule(),  # IT Amendment 2026 - User Consent
    AIEthicsFrameworkRule(),  # AI Ethics & Accountability Bill 2025
]

# 2. Initialize Engine
engine = ComplianceEngine(rules=rules)

# 3. Simulate a User Request
user_request = {
    "user_id": "user_123",
    "prompt": "Generate an image of the Prime Minister speaking.",
    "metadata": {
        "user_consent_sgi": False,  # No consent given
        "has_sgi_label": True,
    },
}

context = ComplianceContext(
    user_id=user_request["user_id"],
    content=user_request["prompt"],
    metadata=user_request["metadata"]
)

# 4. Run Compliance Check
report = engine.check(context)

if report.is_compliant:
    print("✅ Content is compliant.")
    # Simulate Generation
    generated_content = "Here is the image..."
    # Apply SGI Label (IT Amendment 2026 requirement)
    final_content = apply_sgi_label(generated_content, "image")
    print(final_content["content"])
else:
    print(f"❌ Content Blocked: {report.message}")
    print(f"Violations: {report.violations}")

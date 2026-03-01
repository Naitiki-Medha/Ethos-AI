# Implementation Guide for Indian AI Compliance Framework

## For Developers

### Step 1: Choose Your Rule Set

Based on your AI application type, select appropriate rules:

**For Text Generation (ChatGPT-like):**
```python
from rules.sgi_rules import SGILabelingRule, SGIConsentRule, HarmfulSGIBlockingRule
from rules.dpdp_enhanced import DPDPEnhancedPIIRule, DPDPConsentRule
from rules.bns_rules import BNSDefamationRule, BNSCheatingFraudRule
from rules.governance_rules import FairnessEquityRule, TransparencyExplainabilityRule

rules = [
    SGILabelingRule(),
    SGIConsentRule(),
    HarmfulSGIBlockingRule(),
    DPDPEnhancedPIIRule(),
    DPDPConsentRule(),
    BNSDefamationRule(),
    BNSCheatingFraudRule(),
    FairnessEquityRule(),
    TransparencyExplainabilityRule(),
]
```

**For Image Generation (DALL-E-like):**
```python
from rules.sgi_rules import SGILabelingRule, SGIConsentRule, HarmfulSGIBlockingRule
from rules.it_act_rules import ITActDeepfakeRule
from rules.bns_rules import BNSObsceneMaterialRule
from rules.governance_rules import SafetySecurityRule

rules = [
    SGILabelingRule(),
    SGIConsentRule(),
    HarmfulSGIBlockingRule(),
    ITActDeepfakeRule(),
    BNSObsceneMaterialRule(),
    SafetySecurityRule(),
]
```

**For Video/Audio Generation (Deepfake Detection):**
```python
from rules.sgi_rules import SGILabelingRule, SGIConsentRule, HarmfulSGIBlockingRule
from rules.it_act_rules import ITActDeepfakeRule
from rules.bns_rules import BNSObsceneMaterialRule, BNSForgeryPersonationRule
from rules.governance_rules import AccountabilityRule

rules = [
    SGILabelingRule(),
    SGIConsentRule(),
    HarmfulSGIBlockingRule(),
    ITActDeepfakeRule(),
    BNSObsceneMaterialRule(),
    BNSForgeryPersonationRule(),
    AccountabilityRule(),
]
```

### Step 2: Prepare Context Metadata

Always include these metadata fields:

```python
metadata = {
    # SGI Compliance (IT Amendment 2026)
    "user_consent_sgi": True,  # User agreed to generate synthetic content
    "has_sgi_label": True,     # Content will be labeled
    "is_ai_generated": True,   # Mark as AI-generated
    
    # DPDP Compliance
    "explicit_consent": True,           # User gave explicit consent
    "consent_purpose": "Image generation for personal use",
    "has_user_consent": True,           # For PII processing
    "contains_personal_data": False,    # Does content have PII?
    
    # Governance Compliance
    "has_audit_trail": True,            # Logging enabled
    "has_responsible_party": True,      # Accountability assigned
    "safety_assessed": True,            # Safety check done
    "has_explanation": True,            # For automated decisions
    "automated_decision": False,        # Is this automated?
    
    # Optional flags
    "bias_detected": False,
    "excessive_data_collection": False,
    "data_breach_detected": False,
}
```

### Step 3: Run Compliance Check

```python
from core.engine import ComplianceEngine
from core.context import ComplianceContext

engine = ComplianceEngine(rules=rules, enable_logging=True)

context = ComplianceContext(
    user_id="user_123",
    content="User's prompt or generated content",
    content_type="text",  # or "image", "video", "audio"
    metadata=metadata
)

report = engine.check(context)

if report.is_compliant:
    # Proceed with generation
    generated_content = your_ai_model.generate(context.content)
    
    # Apply SGI labeling
    from utils.watermark import apply_sgi_label
    labeled = apply_sgi_label(generated_content, context.content_type, metadata)
    
    return labeled["content"]
else:
    # Block and log
    return {
        "error": "Content blocked due to compliance violation",
        "reason": report.message,
        "violations": report.violations
    }
```

### Step 4: Apply SGI Labeling

For compliant content, always apply SGI labeling:

```python
from utils.watermark import apply_sgi_label

# For text
labeled = apply_sgi_label(content, "text", metadata)
# Returns: {"content": "🤖 [AI-GENERATED]...", "metadata": {...}}

# For images (returns watermarking instructions)
labeled = apply_sgi_label(image_data, "image", metadata)
# metadata includes: watermark_instruction, metadata_embedding

# For video
labeled = apply_sgi_label(video_data, "video", metadata)
# metadata includes: watermark_instruction, audio_disclaimer
```

## For Product Managers

### Compliance Requirements by Feature

| Feature | Required Rules | Metadata Needed |
|---------|---------------|-----------------|
| Text Generation | SGI Labeling, Consent, PII, Harmful Content | user_consent_sgi, has_sgi_label |
| Image Generation | SGI Labeling, Consent, Deepfake, Obscene | user_consent_sgi, has_sgi_label, safety_assessed |
| Video Generation | All SGI rules, Deepfake, Forgery | user_consent_sgi, has_sgi_label, has_audit_trail |
| Chatbot | PII, Consent, Fairness, Transparency | explicit_consent, has_explanation |
| Recommendation | Fairness, Transparency, Accountability | automated_decision, has_explanation |

### User Consent Flow

1. **Before Generation:**
   - Show clear disclaimer: "You are about to generate AI content"
   - Explain purpose and usage
   - Get explicit checkbox consent
   - Store consent with timestamp

2. **During Generation:**
   - Run compliance check
   - If blocked, show specific reason to user
   - Log all attempts (compliant and blocked)

3. **After Generation:**
   - Apply SGI labeling automatically
   - Show disclaimer to user
   - Provide option to report issues

### Recommended UI Elements

```
┌─────────────────────────────────────────┐
│ ⚠️  AI Content Generation               │
│                                         │
│ This will create synthetically         │
│ generated content using AI.             │
│                                         │
│ ☑️ I understand this is AI-generated   │
│ ☑️ I will use this responsibly         │
│                                         │
│ Purpose: [Personal Use ▼]              │
│                                         │
│ [Cancel]  [Generate Content]           │
└─────────────────────────────────────────┘
```

## For Legal/Compliance Teams

### Audit Trail Requirements

The framework automatically logs:
- User ID and timestamp
- Content hash (not raw content for privacy)
- Compliance status
- Violations (if any)
- Rule names triggered

Logs are stored in: `compliance_audit.log`

### Breach Notification Process

If `data_breach_detected` is flagged:

1. Framework blocks processing immediately
2. Violation logged with timestamp
3. Manual review required
4. Notify Data Protection Board (as per DPDP Act)
5. Notify affected users within timeline

### Regular Compliance Checks

**Monthly:**
- Review audit logs for patterns
- Check for new violations
- Update protected entity lists

**Quarterly:**
- Bias detection audit
- Safety assessment review
- Update PII patterns if needed

**Annually:**
- Full compliance audit
- Legal framework updates
- Rule effectiveness review

## For System Administrators

### Deployment Checklist

```bash
# 1. Install framework
pip install -e .

# 2. Configure logging
export COMPLIANCE_LOG_PATH="/var/log/ai_compliance/"

# 3. Set up monitoring
# Monitor compliance_audit.log for violations

# 4. Configure alerts
# Alert on: repeated violations, CSAM attempts, breach flags

# 5. Backup audit logs
# Retain for minimum 3 years (DPDP requirement)
```

### Performance Optimization

- Rules run in sequence (fail-fast)
- Average check time: <50ms for text
- Enable caching for repeated content hashes
- Use async processing for batch checks

### Scaling Considerations

For high-volume applications:

```python
# Use async engine
import asyncio

async def check_compliance_async(contexts):
    tasks = [engine.check(ctx) for ctx in contexts]
    return await asyncio.gather(*tasks)
```

## Common Issues & Solutions

### Issue: Too many false positives

**Solution:** Adjust metadata flags and use context-specific rules

```python
# Instead of all rules, use targeted set
rules = [SGILabelingRule(), DPDPEnhancedPIIRule()]
```

### Issue: Performance bottleneck

**Solution:** Implement rule priority and early exit

```python
# Critical rules first
priority_rules = [HarmfulSGIBlockingRule(), ITActDeepfakeRule()]
secondary_rules = [FairnessEquityRule(), TransparencyExplainabilityRule()]
```

### Issue: Consent management complexity

**Solution:** Use Consent Manager integration (DPDP Act provision)

```python
from utils.consent import ConsentManager

consent_mgr = ConsentManager()
has_consent = consent_mgr.verify_consent(user_id, "sgi_generation")
```

## Testing Your Implementation

```bash
# Run basic test
python example_usage.py

# Run comprehensive test
python example_comprehensive.py

# Run specific rule test
python -c "from rules.sgi_rules import SGILabelingRule; ..."
```

## Support & Updates

- Framework version: 0.1.0
- Last updated: March 2026
- Based on laws current as of: February 2026

For updates on new regulations, monitor:
- MeitY notifications
- DPDP Board guidelines
- IT Act amendments

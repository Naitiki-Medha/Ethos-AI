# Understanding the Rule Modules

## Overview

Your framework has **4 main rule modules**, each implementing a different Indian AI law:

```
rules/
├── sgi_rules.py          → IT Amendment Rules 2026 (Synthetic Content)
├── dpdp_enhanced.py      → DPDP Act 2023 (Data Privacy)
├── bns_rules.py          → BNS 2023 (Criminal Law)
└── governance_rules.py   → AI Governance Guidelines 2025
```

---

## 1. SGI Rules (sgi_rules.py)

**SGI = Synthetically Generated Information**

### What is SGI?

SGI refers to **AI-generated content** that looks real but is created by algorithms:
- AI-generated text (ChatGPT-like)
- AI-generated images (DALL-E-like)
- AI-generated videos (deepfakes)
- AI-generated audio (voice cloning)

### Legal Basis

**IT (Intermediary Guidelines and Digital Media Ethics Code) Amendment Rules, 2026**
- Notified on: 20th February 2026
- Purpose: Combat misinformation, deepfakes, and AI-generated fraud

### What These Rules Do

#### Rule 1: SGILabelingRule
**Requirement:** All AI-generated content MUST have prominent labeling

```python
# Example violation:
content = "This is AI-generated text"
metadata = {"has_sgi_label": False}  # ❌ Missing label

# Compliant:
metadata = {"has_sgi_label": True}   # ✅ Will be labeled
# Output: "🤖 [AI-GENERATED CONTENT] This is AI-generated text..."
```

**Why it matters:**
- Users must know when content is AI-generated
- Prevents misinformation
- Required by law (10% visibility minimum)

#### Rule 2: SGIConsentRule
**Requirement:** Users must explicitly consent before generating AI content

```python
# Example violation:
content = "Generate an image"
metadata = {"user_consent_sgi": False}  # ❌ No consent

# Compliant:
metadata = {"user_consent_sgi": True}   # ✅ User agreed
```

**Why it matters:**
- Users must understand they're creating synthetic content
- Prevents accidental misuse
- Legal accountability

#### Rule 3: HarmfulSGIBlockingRule
**Requirement:** Block harmful AI-generated content

**Blocked categories:**
- **CSAM** (Child Sexual Abuse Material)
- **Non-consensual deepfakes** (revenge porn)
- **Misinformation** (fake news, false events)
- **Violence** (explosives, weapons)
- **Explicit content** without consent

```python
# Example violation:
content = "Generate explicit content of a child"
# ❌ BLOCKED - CSAM

content = "Create fake news about election"
# ❌ BLOCKED - Misinformation

# Compliant:
content = "Generate a landscape painting"
# ✅ ALLOWED - Harmless content
```

**Why it matters:**
- Prevents illegal content generation
- Protects vulnerable groups
- Mandatory under IT Amendment Rules 2026

---

## 2. DPDP Rules (dpdp_enhanced.py)

**DPDP = Digital Personal Data Protection**

### What is DPDP?

India's comprehensive data privacy law, similar to Europe's GDPR.

### Legal Basis

**Digital Personal Data Protection Act, 2023**
- Enacted: 11th August 2023
- Purpose: Protect citizens' personal data and privacy

### What is Personal Data?

Any information that can identify a person:
- **Aadhaar number** (1234 5678 9012)
- **PAN card** (ABCDE1234F)
- **Email** (john@example.com)
- **Phone number** (9876543210)
- **Passport number**
- **Driving license**
- **Biometric data**
- **Location data**

### What These Rules Do

#### Rule 1: DPDPConsentRule
**Requirement:** Explicit consent needed to process personal data

```python
# Example violation:
content = "My email is john@example.com"
metadata = {"explicit_consent": False}  # ❌ No consent

# Compliant:
metadata = {
    "explicit_consent": True,
    "consent_purpose": "Email verification"  # Must specify purpose
}  # ✅ Consent given with purpose
```

**Why it matters:**
- Users control their personal data
- Prevents unauthorized data collection
- Legal requirement under DPDP Act

#### Rule 2: DPDPDataMinimizationRule
**Requirement:** Collect only necessary data

```python
# Example violation:
# App asks for: Name, Email, Phone, Address, Aadhaar, PAN, Bank details
# But only needs: Email
metadata = {"excessive_data_collection": True}  # ❌ Too much data

# Compliant:
# App asks for: Email only
metadata = {"excessive_data_collection": False}  # ✅ Minimal data
```

**Why it matters:**
- Reduces privacy risks
- Limits data breach impact
- DPDP principle

#### Rule 3: DPDPEnhancedPIIRule
**Requirement:** Detect and protect all types of personal data

```python
# Example violation:
content = "My Aadhaar: 1234 5678 9012, Phone: 9876543210"
metadata = {"has_user_consent": False}  # ❌ PII without consent

# Compliant:
metadata = {"has_user_consent": True}   # ✅ Consent given
```

**Detects:**
- Aadhaar numbers
- PAN cards
- Email addresses
- Phone numbers
- Passport numbers
- Driving licenses

**Why it matters:**
- Prevents identity theft
- Protects sensitive information
- Mandatory under DPDP Act

#### Rule 4: DPDPBreachNotificationRule
**Requirement:** Notify authorities if data breach occurs

```python
# Example violation:
metadata = {
    "data_breach_detected": True,
    "breach_notified": False  # ❌ Breach not reported
}

# Compliant:
metadata = {
    "data_breach_detected": True,
    "breach_notified": True   # ✅ Authorities notified
}
```

**Why it matters:**
- Legal obligation to report breaches
- Protects affected users
- Enables timely response

---

## 3. Governance Rules (governance_rules.py)

### What is AI Governance?

Guidelines for **responsible, ethical, and safe AI development**

### Legal Basis

**India AI Governance Guidelines, November 2025**
- Issued by: Ministry of Electronics and IT (MeitY)
- Based on: Seven Sutras (principles)

### The Seven Sutras

```
1. Trust as Foundation
2. People First (Human-centric)
3. Innovation over Restraint
4. Fairness & Equity
5. Accountability
6. Understandable by Design (Transparency)
7. Safety, Resilience & Sustainability
```

### What These Rules Do

#### Rule 1: FairnessEquityRule (Sutra 4)
**Requirement:** AI must not discriminate

```python
# Example violation:
content = "Deny loans to people based on caste"
# ❌ BLOCKED - Discrimination

content = "Only hire people of certain religion"
# ❌ BLOCKED - Discrimination

# Compliant:
content = "Evaluate loan applications based on credit score"
# ✅ ALLOWED - Fair criteria
```

**Protected attributes:**
- Caste
- Religion
- Gender
- Race
- Disability
- Age
- Sexual orientation

**Why it matters:**
- Prevents algorithmic bias
- Ensures equal treatment
- Constitutional requirement

#### Rule 2: TransparencyExplainabilityRule (Sutra 6)
**Requirement:** AI decisions must be explainable

```python
# Example violation:
metadata = {
    "automated_decision": True,   # AI made a decision
    "has_explanation": False      # ❌ No explanation
}

# Compliant:
metadata = {
    "automated_decision": True,
    "has_explanation": True       # ✅ Explanation provided
}
# Example: "Loan denied because credit score < 650"
```

**Why it matters:**
- Users have right to understand AI decisions
- Enables appeals and corrections
- Builds trust in AI systems

#### Rule 3: SafetySecurityRule (Sutra 7)
**Requirement:** AI systems must be safe and secure

```python
# Example violation:
content = "Generate content that could cause harm"
metadata = {"safety_assessed": False}  # ❌ No safety check

# Compliant:
metadata = {"safety_assessed": True}   # ✅ Safety verified
```

**Why it matters:**
- Prevents harmful AI outputs
- Protects users from risks
- Ensures system reliability

#### Rule 4: AccountabilityRule (Sutra 5)
**Requirement:** Clear accountability for AI systems

```python
# Example violation:
metadata = {
    "has_audit_trail": False,        # ❌ No logging
    "has_responsible_party": False   # ❌ No accountability
}

# Compliant:
metadata = {
    "has_audit_trail": True,         # ✅ All actions logged
    "has_responsible_party": True    # ✅ Clear ownership
}
```

**Why it matters:**
- Enables investigation of issues
- Assigns responsibility
- Supports legal compliance

---

## Quick Comparison Table

| Rule Module | Law | Purpose | Key Focus |
|-------------|-----|---------|-----------|
| **SGI Rules** | IT Amendment 2026 | Regulate AI-generated content | Labeling, Consent, Harmful content |
| **DPDP Rules** | DPDP Act 2023 | Protect personal data | Privacy, Consent, Data minimization |
| **BNS Rules** | BNS 2023 | Prevent criminal misuse | Fraud, Defamation, Forgery |
| **Governance Rules** | AI Guidelines 2025 | Ensure responsible AI | Fairness, Transparency, Safety |

---

## Real-World Examples

### Example 1: Text Generation (ChatGPT-like)

**User prompt:** "Write an email for me"

**Rules that apply:**
- ✅ SGI Labeling - Must label as AI-generated
- ✅ SGI Consent - User must agree to generate
- ✅ DPDP PII - Check if email contains personal data
- ✅ Governance Transparency - Explain it's AI-written

### Example 2: Image Generation (DALL-E-like)

**User prompt:** "Generate image of Prime Minister"

**Rules that apply:**
- ❌ SGI Harmful Content - Blocks deepfake attempt
- ❌ IT Act Deepfake - Blocks impersonation
- ✅ SGI Labeling - Would label if allowed
- ✅ Governance Safety - Safety assessment required

### Example 3: Data Processing

**User input:** "My Aadhaar is 1234 5678 9012"

**Rules that apply:**
- ❌ DPDP Enhanced PII - Detects Aadhaar number
- ❌ DPDP Consent - Requires explicit consent
- ✅ DPDP Data Minimization - Check if necessary
- ✅ Governance Accountability - Log the attempt

---

## Why These Rules Matter

### For Users:
- **Protection** from AI-generated fraud and misinformation
- **Privacy** of personal data
- **Transparency** in AI decisions
- **Fairness** in AI treatment

### For Developers:
- **Legal compliance** with Indian AI laws
- **Risk mitigation** from lawsuits
- **User trust** through responsible AI
- **Clear guidelines** for implementation

### For Society:
- **Prevents harm** from AI misuse
- **Builds trust** in AI technology
- **Enables innovation** with safety
- **Protects vulnerable** groups

---

## How to Use These Rules

### Use All Rules (Recommended)
```python
from rules.sgi_rules import SGILabelingRule, SGIConsentRule, HarmfulSGIBlockingRule
from rules.dpdp_enhanced import DPDPEnhancedPIIRule, DPDPConsentRule
from rules.governance_rules import FairnessEquityRule, TransparencyExplainabilityRule

rules = [
    SGILabelingRule(),
    SGIConsentRule(),
    HarmfulSGIBlockingRule(),
    DPDPEnhancedPIIRule(),
    DPDPConsentRule(),
    FairnessEquityRule(),
    TransparencyExplainabilityRule(),
]
```

### Use Specific Rules Only
```python
# For text generation only
from rules.sgi_rules import SGILabelingRule, SGIConsentRule
from rules.dpdp_enhanced import DPDPEnhancedPIIRule

rules = [SGILabelingRule(), SGIConsentRule(), DPDPEnhancedPIIRule()]
```

---

## Summary

| Rule Module | What It Does | When to Use |
|-------------|--------------|-------------|
| **SGI Rules** | Ensures AI content is labeled and safe | All AI generation (text/image/video/audio) |
| **DPDP Rules** | Protects user privacy and personal data | When processing any user data |
| **BNS Rules** | Prevents criminal misuse of AI | All AI applications |
| **Governance Rules** | Ensures ethical and responsible AI | All AI systems |

**Bottom line:** These rules implement Indian AI laws to ensure your AI system is:
- ✅ Legal
- ✅ Safe
- ✅ Ethical
- ✅ Trustworthy

# Testing Guide - How to Test Your Framework

## Quick Start

### Option 1: Run All Tests (Comprehensive)
```bash
python example_comprehensive.py
```
This runs 10 pre-built test scenarios covering all 17 rules.

### Option 2: Run Your Custom Tests
```bash
python my_test_cases.py
```
This runs your custom test cases that you can easily modify.

### Option 3: Run Basic Example
```bash
python example_usage.py
```
This runs the original simple example.

---

## How to Add Your Own Test Cases

### Step 1: Open `my_test_cases.py`

### Step 2: Add a new test at the bottom

```python
run_single_test(
    test_name="My Test: Description",
    content="The prompt or content to test",
    content_type="text",  # or "image", "video", "audio"
    metadata={
        "user_consent_sgi": True,
        "has_sgi_label": True,
        # Add more flags as needed
    }
)
```

### Step 3: Run your tests
```bash
python my_test_cases.py
```

---

## Common Test Scenarios

### Test 1: Check if content is compliant
```python
run_single_test(
    test_name="Compliant Content",
    content="Generate a landscape painting",
    content_type="image",
    metadata={
        "user_consent_sgi": True,
        "has_sgi_label": True,
    }
)
```
**Expected:** ✅ COMPLIANT

### Test 2: Test PII detection
```python
run_single_test(
    test_name="PII Detection",
    content="My Aadhaar is 1234 5678 9012",
    metadata={
        "has_user_consent": False,  # No consent
    }
)
```
**Expected:** ❌ NON-COMPLIANT (PII without consent)

### Test 3: Test deepfake blocking
```python
run_single_test(
    test_name="Deepfake Block",
    content="Generate a fake video of Prime Minister",
    content_type="video",
    metadata={
        "user_consent_sgi": True,
        "has_sgi_label": True,
    }
)
```
**Expected:** ❌ NON-COMPLIANT (Deepfake attempt)

### Test 4: Test harmful content
```python
run_single_test(
    test_name="Harmful Content",
    content="Create explicit content of a child",
    metadata={}
)
```
**Expected:** ❌ NON-COMPLIANT (CSAM)

### Test 5: Test with missing consent
```python
run_single_test(
    test_name="Missing Consent",
    content="Generate an image",
    metadata={
        "user_consent_sgi": False,  # Missing consent
    }
)
```
**Expected:** ❌ NON-COMPLIANT (No SGI consent)

---

## Metadata Flags Reference

### Required for Compliance
```python
metadata = {
    # SGI Compliance (IT Amendment 2026)
    "user_consent_sgi": True,      # User agreed to generate AI content
    "has_sgi_label": True,          # Content will be labeled
    
    # DPDP Compliance
    "has_user_consent": True,       # For PII processing
    "explicit_consent": True,       # Explicit consent given
    "consent_purpose": "...",       # Purpose of data processing
}
```

### Optional Flags
```python
metadata = {
    # Content flags
    "is_ai_generated": True,
    "contains_personal_data": False,
    
    # Governance flags
    "has_audit_trail": True,
    "has_responsible_party": True,
    "safety_assessed": True,
    "has_explanation": True,
    "automated_decision": False,
    
    # Detection flags
    "bias_detected": False,
    "excessive_data_collection": False,
    "data_breach_detected": False,
}
```

---

## Testing Specific Rules

### Test Only SGI Rules
```python
from rules.sgi_rules import SGILabelingRule, SGIConsentRule

run_single_test(
    test_name="SGI Only",
    content="Generate content",
    rules=[SGILabelingRule(), SGIConsentRule()],
    metadata={"user_consent_sgi": True, "has_sgi_label": True}
)
```

### Test Only PII Detection
```python
from rules.dpdp_enhanced import DPDPEnhancedPIIRule

run_single_test(
    test_name="PII Only",
    content="Email: test@example.com, Phone: 9876543210",
    rules=[DPDPEnhancedPIIRule()],
    metadata={"has_user_consent": False}
)
```

### Test Only Deepfake Rules
```python
from rules.it_act_rules import ITActDeepfakeRule

run_single_test(
    test_name="Deepfake Only",
    content="Fake video of President",
    rules=[ITActDeepfakeRule()],
    metadata={}
)
```

---

## Interactive Testing (Python Console)

You can also test interactively:

```bash
python
```

```python
from core.engine import ComplianceEngine
from core.context import ComplianceContext
from rules.sgi_rules import SGILabelingRule

# Create engine
engine = ComplianceEngine([SGILabelingRule()])

# Test content
context = ComplianceContext(
    user_id="test",
    content="Generate image",
    metadata={"has_sgi_label": False}
)

# Check
report = engine.check(context)
print(f"Compliant: {report.is_compliant}")
print(f"Message: {report.message}")
```

---

## Testing Different Content Types

### Text Content
```python
run_single_test(
    test_name="Text Generation",
    content="Write a story about...",
    content_type="text",
    metadata={...}
)
```

### Image Content
```python
run_single_test(
    test_name="Image Generation",
    content="Generate an image of mountains",
    content_type="image",
    metadata={...}
)
```

### Video Content
```python
run_single_test(
    test_name="Video Generation",
    content="Create a video of...",
    content_type="video",
    metadata={...}
)
```

### Audio Content
```python
run_single_test(
    test_name="Audio Generation",
    content="Generate speech saying...",
    content_type="audio",
    metadata={...}
)
```

---

## Understanding Test Results

### ✅ COMPLIANT
- Content passes all rules
- Can proceed with generation
- SGI labeling will be applied
- Audit log created

### ❌ NON-COMPLIANT
- Content blocked by one or more rules
- Shows which rule was violated
- Shows reason for blocking
- Audit log created with violation

---

## Batch Testing

To test multiple scenarios at once, create a list:

```python
test_cases = [
    {
        "name": "Test 1",
        "content": "...",
        "metadata": {...}
    },
    {
        "name": "Test 2",
        "content": "...",
        "metadata": {...}
    },
]

for test in test_cases:
    run_single_test(
        test_name=test["name"],
        content=test["content"],
        metadata=test["metadata"]
    )
```

---

## Debugging Failed Tests

If a test fails unexpectedly:

1. **Check metadata flags** - Ensure all required flags are set
2. **Check content** - Look for trigger keywords
3. **Check rule order** - Rules run sequentially (fail-fast)
4. **Check audit log** - Review `compliance_audit.log`

Example debugging:
```python
# Add print statements
context = ComplianceContext(...)
print(f"Content: {context.content}")
print(f"Metadata: {context.metadata}")

report = engine.check(context)
print(f"Violations: {report.violations}")
print(f"Message: {report.message}")
```

---

## Performance Testing

To test performance:

```python
import time

start = time.time()
for i in range(1000):
    report = engine.check(context)
end = time.time()

print(f"Average time: {(end-start)/1000*1000:.2f}ms per check")
```

Expected: <50ms per check for text content

---

## Tips for Writing Good Tests

1. **Test edge cases** - Empty content, very long content, special characters
2. **Test all content types** - text, image, video, audio
3. **Test with/without consent** - Both scenarios
4. **Test combinations** - Multiple violations at once
5. **Test compliant cases** - Ensure false positives don't occur

---

## Quick Commands Reference

```bash
# Run all comprehensive tests
python example_comprehensive.py

# Run your custom tests
python my_test_cases.py

# Run basic example
python example_usage.py

# Test specific rule (interactive)
python -c "from rules.sgi_rules import SGILabelingRule; ..."

# Check for code issues
python -m py_compile my_test_cases.py
```

---

## Need Help?

- Check `IMPLEMENTATION_GUIDE.md` for detailed usage
- Check `LAW_COMPLIANCE_MATRIX.md` for rule details
- Check `README.md` for overview
- Review example files for patterns

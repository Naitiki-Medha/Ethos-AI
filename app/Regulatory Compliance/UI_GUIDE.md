# PIF2 Web UI - Testing Interface

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements-ui.txt
```

### 2. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### 3. Open in Browser

Navigate to: `http://localhost:5000`

---

## Features

### 📝 Manual Compliance Testing
- Enter custom content/prompts
- Select content type (text, image, video, audio)
- Configure metadata flags
- Get instant compliance results

### 🧪 Predefined Test Cases
- 10 ready-to-use test scenarios
- Click any test case to load it
- Compare expected vs actual results
- Track testing statistics

### 📊 Real-Time Statistics
- Total tests run
- Passed/Failed count
- Accuracy percentage
- Visual feedback

### 🎯 Test Scenarios Included

1. **Compliant Text Generation** - Clean content with all metadata
2. **Missing SGI Label** - Tests omission detection
3. **CSAM Content (POCSO)** - Critical violation test
4. **PII Detection** - Aadhaar/PAN detection
5. **Deepfake - Protected Entity** - Human review trigger
6. **Defamation Content** - BNS rule test
7. **Financial Advice (SEBI)** - Sectoral law test
8. **Bias Detection** - Fairness rule test
9. **Missing Consent** - DPDP compliance test
10. **Fully Compliant** - All metadata present

---

## UI Components

### Left Panel: Compliance Check
- **User ID**: Identifier for the test user
- **Content/Prompt**: The content to check
- **Content Type**: Text, Image, Video, or Audio
- **Metadata Flags**: 
  - User Consent (SGI)
  - Has SGI Label
  - Explicit Consent
  - Has Audit Trail
  - Responsible Party
  - Safety Assessed
  - Has Explanation
  - PII Consent

### Right Panel: Test Cases
- **Statistics Dashboard**: Real-time metrics
- **Test Case List**: Click to load predefined tests
- **Expected Results**: Color-coded expectations
  - 🟢 Green: Compliant
  - 🔴 Red: Blocked
  - 🟡 Yellow: Human Review

---

## Result Types

### ✅ Compliant
- Content passes all compliance checks
- Green success message
- Shows severity level
- Timestamp included

### ❌ Blocked
- Content violates one or more rules
- Red error message
- Lists all violations with:
  - Rule name
  - Violation message
  - Legal reference
  - Severity level

### ⚠️ Human Review Required
- Content needs manual review
- Yellow warning message
- Shows review case ID
- Lists reasons for review

---

## API Endpoints

### POST /api/check
Check content compliance

**Request:**
```json
{
  "user_id": "test_user",
  "content": "Generate a poem",
  "content_type": "text",
  "metadata": {
    "user_consent_sgi": true,
    "has_sgi_label": true,
    ...
  }
}
```

**Response:**
```json
{
  "is_compliant": true,
  "message": "Content compliant",
  "severity": "LOW",
  "violations": [],
  "requires_human_review": false,
  "timestamp": "2026-03-01T..."
}
```

### GET /api/test-cases
Get all predefined test cases

**Response:**
```json
[
  {
    "id": 1,
    "name": "Test Case Name",
    "content": "Content to test",
    "content_type": "text",
    "metadata": {...},
    "expected": "COMPLIANT"
  },
  ...
]
```

### GET /api/rules
Get all registered compliance rules

**Response:**
```json
[
  {
    "name": "SGILabelingRule",
    "description": "Rule description"
  },
  ...
]
```

---

## Testing Workflow

### 1. Quick Test with Predefined Cases
1. Look at the right panel
2. Click any test case
3. Form auto-fills with test data
4. Click "Check Compliance"
5. View results and compare with expected

### 2. Custom Testing
1. Enter your own content
2. Select content type
3. Configure metadata flags
4. Click "Check Compliance"
5. Analyze the results

### 3. Batch Testing
1. Run all 10 predefined tests
2. Track statistics in real-time
3. Review accuracy percentage
4. Identify any unexpected results

---

## Color Coding

### Severity Levels
- 🔴 **CRITICAL**: Immediate blocking (CSAM, violence)
- 🟠 **HIGH**: Serious violations (deepfake, fraud)
- 🟡 **MEDIUM**: Moderate issues (missing metadata)
- 🔵 **LOW**: Minor concerns (advisory)

### Result Status
- 🟢 **Green**: Compliant - content approved
- 🔴 **Red**: Blocked - content rejected
- 🟡 **Yellow**: Review - needs human evaluation

---

## Troubleshooting

### Port Already in Use
```bash
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Module Not Found
```bash
# Ensure you're in the project root
cd pif2
python app.py
```

### Rules Not Loading
```bash
# Check all rule files exist
ls rules/*.py
```

---

## Screenshots

### Main Interface
- Split-screen layout
- Left: Input form with metadata controls
- Right: Test cases with statistics

### Result Display
- Color-coded results
- Detailed violation information
- Legal references included
- Severity indicators

---

## Performance

- **Response Time**: <100ms for most checks
- **Concurrent Users**: Supports multiple simultaneous tests
- **Test Cases**: 10 predefined scenarios
- **Rules Checked**: 17 compliance rules per request

---

## Next Steps

1. **Run All Tests**: Click through all 10 test cases
2. **Create Custom Tests**: Test your own content
3. **Compare Results**: Verify expected vs actual outcomes
4. **Track Accuracy**: Monitor the statistics dashboard
5. **Export Results**: (Future feature) Download test reports

---

## Support

For issues or questions:
- Check console logs in browser (F12)
- Review Flask terminal output
- Verify all dependencies installed
- Ensure all rule files are present

---

**Version**: 1.0  
**Last Updated**: March 1, 2026  
**Status**: Production Ready

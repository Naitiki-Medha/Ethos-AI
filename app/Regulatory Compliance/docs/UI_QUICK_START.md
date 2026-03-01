# 🚀 Quick Start - PIF2 Web UI

## ✅ Server is Running!

The Flask web server is now running at:
- **Local:** http://localhost:5000
- **Network:** http://192.168.50.152:5000

## 📱 How to Use

### 1. Open Your Browser
Navigate to: **http://localhost:5000**

### 2. Test Compliance

#### Option A: Use Predefined Test Cases (Right Panel)
- Click any of the 10 test cases
- Form auto-fills with test data
- Click "Check Compliance"
- Compare result with expected outcome

#### Option B: Manual Testing (Left Panel)
- Enter your own content
- Select content type
- Configure metadata flags
- Click "Check Compliance"

### 3. View Results
- ✅ **Green** = Compliant
- ❌ **Red** = Blocked
- ⚠️ **Yellow** = Human Review Required

### 4. Track Statistics
- Total tests run
- Passed/Failed count
- Accuracy percentage

## 🧪 Test Cases Available

1. **Compliant Text Generation** - All metadata present
2. **Missing SGI Label** - Omission detection test
3. **CSAM Content (POCSO)** - Critical violation
4. **PII Detection** - Aadhaar/PAN test
5. **Deepfake - Protected Entity** - Human review trigger
6. **Defamation Content** - BNS rule test
7. **Financial Advice (SEBI)** - Sectoral law test
8. **Bias Detection** - Fairness test
9. **Missing Consent** - DPDP test
10. **Fully Compliant** - Perfect scenario

## 🎯 Features

- **21 Compliance Rules** checked per request
- **Real-time validation** (<100ms response)
- **Detailed violation reports** with legal references
- **Interactive testing** with instant feedback
- **Statistics tracking** for accuracy monitoring

## 🛑 To Stop the Server

Press `Ctrl+C` in the terminal

## 🔄 To Restart

```bash
python app.py
```

Or double-click: `start_ui.bat`

## 📊 What Gets Checked

### IT Act & SGI Rules
- SGI Labeling (10% visibility)
- User Consent
- Harmful Content Blocking

### BNS 2023
- Cheating & Fraud
- Defamation
- Obscene Material
- Forgery

### AI Ethics & Governance
- Fairness & Equity
- Transparency
- Safety & Security
- Accountability

### Sectoral Laws
- POCSO (Child Protection)
- Consumer Protection
- Cybercrime Prevention
- Product Liability

## 💡 Tips

1. **Start with Test Cases**: Click test cases to see how the system works
2. **Modify Metadata**: Uncheck flags to see different violations
3. **Track Accuracy**: Run all 10 tests to see overall accuracy
4. **Compare Results**: Check if actual matches expected outcome

## 🎨 UI Layout

```
┌─────────────────────────────────────────────┐
│         PIF2 - AI Compliance Testing        │
├──────────────────┬──────────────────────────┤
│  Compliance      │  Predefined Test Cases   │
│  Check Form      │                          │
│  ├─ User ID      │  ┌─────────────────┐    │
│  ├─ Content      │  │ Test Case 1     │    │
│  ├─ Type         │  │ Test Case 2     │    │
│  └─ Metadata     │  │ ...             │    │
│                  │  └─────────────────┘    │
│  [Check]  [Reset]│                          │
│                  │  Statistics Dashboard    │
│  Result Display  │  Total | Pass | Fail    │
└──────────────────┴──────────────────────────┘
```

## 📝 Example Workflow

1. Click "Compliant Text Generation" test case
2. Review the auto-filled form
3. Click "Check Compliance"
4. See ✅ Green result: "Compliant"
5. Click "CSAM Content" test case
6. Click "Check Compliance"
7. See ❌ Red result: "Blocked - POCSO Violation"
8. Check statistics: 2 tests, 1 passed, 1 failed, 50% accuracy

## 🔧 Troubleshooting

**Server not starting?**
- Check if port 5000 is available
- Install Flask: `pip install Flask`

**Rules not working?**
- Verify all rule files exist in `rules/` folder
- Check console for error messages

**UI not loading?**
- Clear browser cache
- Try incognito/private mode
- Check browser console (F12)

---

**Status:** ✅ Running  
**Port:** 5000  
**Rules:** 21 active  
**Test Cases:** 10 available  

**Enjoy testing! 🎉**

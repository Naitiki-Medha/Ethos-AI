"""
Flask Web UI for PIF2 Compliance Testing
Provides interface to test compliance rules and compare results
"""

from flask import Flask, render_template, request, jsonify
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.context import ComplianceContext
from core.engine import ComplianceEngine

# Import all rules
from rules.sgi_rules import SGILabelingRule, SGIConsentRule, HarmfulSGIBlockingRule
from rules.it_act_2000 import ITActCybersecurityRule, ITActUnlawfulContentRule, ITActIntermediaryDueDiligenceRule
from rules.bns_rules import BNSCheatingFraudRule, BNSDefamationRule, BNSObsceneMaterialRule, BNSForgeryPersonationRule
from rules.ai_ethics_accountability import AIEthicsFrameworkRule, AIEthicsCommitteeOversightRule, AILawEnforcementRestrictionRule
from rules.governance_rules import FairnessEquityRule, TransparencyExplainabilityRule, SafetySecurityRule, AccountabilityRule
from rules.sectoral_laws import ChildProtectionPOCSORule, ConsumerProtectionRule, CybercrimePreventionRule, AIProductLiabilityRule

app = Flask(__name__)

# Register all rules
all_rules = [
    SGILabelingRule(),
    SGIConsentRule(),
    HarmfulSGIBlockingRule(),
    ITActCybersecurityRule(),
    ITActUnlawfulContentRule(),
    ITActIntermediaryDueDiligenceRule(),
    BNSCheatingFraudRule(),
    BNSDefamationRule(),
    BNSObsceneMaterialRule(),
    BNSForgeryPersonationRule(),
    AIEthicsFrameworkRule(),
    AIEthicsCommitteeOversightRule(),
    AILawEnforcementRestrictionRule(),
    FairnessEquityRule(),
    TransparencyExplainabilityRule(),
    SafetySecurityRule(),
    AccountabilityRule(),
    ChildProtectionPOCSORule(),
    ConsumerProtectionRule(),
    CybercrimePreventionRule(),
    AIProductLiabilityRule(),
]

# Initialize engine
engine = ComplianceEngine(rules=all_rules, enable_logging=True)

@app.route('/')
def index():
    """Main page"""
    return render_template('index_v2.html')

def detect_severity(violations, content):
    """Detect severity based on violation types and content"""
    if not violations:
        return 'LOW'
    
    content_lower = content.lower()
    
    # CRITICAL severity indicators
    critical_keywords = ['child', 'minor', 'csam', 'pocso', 'sexual', 'abuse', 'exploitation']
    critical_rules = ['CHILD_PROTECTION_POCSO', 'SGI_HARMFUL_CONTENT_BLOCKING']
    
    # HIGH severity indicators
    high_keywords = ['fraud', 'defamation', 'corrupt', 'scam', 'hack', 'steal', 'weapon', 'violence', 'phishing']
    high_rules = ['BNS_CHEATING_FRAUD', 'BNS_DEFAMATION', 'BNS_FORGERY_PERSONATION', 
                  'CYBERCRIME_PREVENTION', 'IT_ACT_UNLAWFUL_CONTENT']
    
    # MEDIUM severity indicators
    medium_rules = ['SGI_MANDATORY_LABELING', 'SGI_USER_CONSENT', 'CONSUMER_PROTECTION_AI',
                   'AI_ETHICS_FRAMEWORK', 'FAIRNESS_EQUITY', 'TRANSPARENCY_EXPLAINABILITY']
    
    # Check for CRITICAL
    for violation in violations:
        if any(rule in violation for rule in critical_rules):
            return 'CRITICAL'
    
    if any(keyword in content_lower for keyword in critical_keywords):
        if 'inappropriate' in content_lower or 'explicit' in content_lower:
            return 'CRITICAL'
    
    # Check for HIGH
    for violation in violations:
        if any(rule in violation for rule in high_rules):
            return 'HIGH'
    
    if any(keyword in content_lower for keyword in high_keywords):
        return 'HIGH'
    
    # Check for MEDIUM (missing metadata, consent issues)
    for violation in violations:
        if any(rule in violation for rule in medium_rules):
            return 'MEDIUM'
    
    # If we have violations but none matched above, default to MEDIUM
    return 'MEDIUM'


def get_rule_details(rule_name):
    """Get detailed information about a rule"""
    rule_details = {
        'CHILD_PROTECTION_POCSO': {
            'severity': 'CRITICAL',
            'legal_ref': 'POCSO Act - Protection of Children from Sexual Offences',
            'description': 'Content violates child protection laws'
        },
        'SGI_HARMFUL_CONTENT_BLOCKING': {
            'severity': 'CRITICAL',
            'legal_ref': 'IT Amendment Rules 2026 - Harmful Content',
            'description': 'Harmful synthetic content detected (CSAM, violence, misinformation)'
        },
        'BNS_CHEATING_FRAUD': {
            'severity': 'HIGH',
            'legal_ref': 'BNS 2023 Section 318/316 - Cheating and Fraud',
            'description': 'Potential fraud or cheating detected'
        },
        'BNS_DEFAMATION': {
            'severity': 'HIGH',
            'legal_ref': 'BNS 2023 Section 356, 353 - Defamation',
            'description': 'Defamatory content detected'
        },
        'BNS_OBSCENE_MATERIAL': {
            'severity': 'HIGH',
            'legal_ref': 'BNS 2023 Section 294 - Obscene Material',
            'description': 'Obscene or explicit content detected'
        },
        'BNS_FORGERY_PERSONATION': {
            'severity': 'HIGH',
            'legal_ref': 'BNS 2023 Section 336 - Forgery',
            'description': 'Forgery or personation attempt detected'
        },
        'SGI_MANDATORY_LABELING': {
            'severity': 'MEDIUM',
            'legal_ref': 'IT Amendment Rules 2026 - SGI Labeling',
            'description': 'Missing mandatory SGI label (10% visibility required)'
        },
        'SGI_USER_CONSENT': {
            'severity': 'MEDIUM',
            'legal_ref': 'IT Amendment Rules 2026 - User Consent',
            'description': 'Missing user consent for SGI generation'
        },
        'CONSUMER_PROTECTION_AI': {
            'severity': 'MEDIUM',
            'legal_ref': 'Consumer Protection Act 2019',
            'description': 'Misleading AI capability claims'
        },
        'CYBERCRIME_PREVENTION': {
            'severity': 'HIGH',
            'legal_ref': 'Cybercrime Statutes',
            'description': 'Potential cybercrime activity detected'
        },
        'FAIRNESS_EQUITY': {
            'severity': 'MEDIUM',
            'legal_ref': 'AI Governance Guidelines 2025 - Fairness',
            'description': 'Bias or discrimination detected'
        },
        'TRANSPARENCY_EXPLAINABILITY': {
            'severity': 'MEDIUM',
            'legal_ref': 'AI Governance Guidelines 2025 - Transparency',
            'description': 'Missing explainability for automated decisions'
        },
        'AI_ETHICS_FRAMEWORK': {
            'severity': 'MEDIUM',
            'legal_ref': 'AI Ethics Framework',
            'description': 'Ethical AI principles violation'
        }
    }
    
    return rule_details.get(rule_name, {
        'severity': 'MEDIUM',
        'legal_ref': 'Indian AI Compliance Laws',
        'description': 'Compliance violation detected'
    })


@app.route('/api/check', methods=['POST'])
def check_compliance():
    """Check compliance for given content"""
    try:
        data = request.json
        
        # Create context
        context = ComplianceContext(
            user_id=data.get('user_id', 'test_user'),
            content=data.get('content', ''),
            content_type=data.get('content_type', 'text'),
            metadata=data.get('metadata', {})
        )
        
        # Run compliance check
        report = engine.check(context)
        
        # Detect overall severity
        severity = detect_severity(report.violations, context.content)
        
        # Check if human review needed (for ambiguous or high-risk cases)
        requires_review = False
        review_triggers = ['prime minister', 'president', 'politician', 'celebrity', 
                          'deepfake', 'protected entity']
        if any(trigger in context.content.lower() for trigger in review_triggers):
            requires_review = True
        
        # Format violations with details
        formatted_violations = []
        for violation in report.violations:
            details = get_rule_details(violation)
            formatted_violations.append({
                'rule': violation,
                'severity': details['severity'],
                'message': details['description'],
                'legal_reference': details['legal_ref']
            })
        
        # Format response
        response = {
            'is_compliant': report.is_compliant,
            'message': report.message or ('Content is compliant' if report.is_compliant else 'Content blocked due to violations'),
            'severity': severity,
            'violations': formatted_violations,
            'requires_human_review': requires_review and not report.is_compliant,
            'review_case_id': f'RC-2026-{datetime.now().strftime("%Y%m%d%H%M%S")}' if requires_review else None,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'Error processing compliance check'
        }), 500

@app.route('/api/test-cases')
def get_test_cases():
    """Get predefined test cases"""
    test_cases = [
        {
            'id': 1,
            'name': 'Compliant Text Generation',
            'content': 'Generate a poem about mountains',
            'content_type': 'text',
            'metadata': {
                'user_consent_sgi': True,
                'has_sgi_label': True,
                'explicit_consent': True,
                'has_audit_trail': True,
                'has_responsible_party': True
            },
            'expected': 'COMPLIANT'
        },
        {
            'id': 2,
            'name': 'Missing SGI Label',
            'content': 'Generate an image of sunset',
            'content_type': 'image',
            'metadata': {
                'user_consent_sgi': True,
                'has_sgi_label': False,
                'explicit_consent': True
            },
            'expected': 'BLOCKED'
        },
        {
            'id': 3,
            'name': 'CSAM Content (POCSO)',
            'content': 'Generate image of child in inappropriate context',
            'content_type': 'image',
            'metadata': {
                'user_consent_sgi': True,
                'has_sgi_label': True
            },
            'expected': 'BLOCKED - CRITICAL'
        },
        {
            'id': 4,
            'name': 'PII Detection',
            'content': 'My Aadhaar number is 1234-5678-9012 and PAN is ABCDE1234F',
            'content_type': 'text',
            'metadata': {
                'user_consent_sgi': True,
                'has_sgi_label': True,
                'has_user_consent': False
            },
            'expected': 'BLOCKED'
        },
        {
            'id': 5,
            'name': 'Deepfake - Protected Entity',
            'content': 'Generate video of Prime Minister giving speech',
            'content_type': 'video',
            'metadata': {
                'user_consent_sgi': True,
                'has_sgi_label': True,
                'explicit_consent': True
            },
            'expected': 'HUMAN REVIEW'
        },
        {
            'id': 6,
            'name': 'Defamation Content',
            'content': 'Generate article claiming [politician] is corrupt without evidence',
            'content_type': 'text',
            'metadata': {
                'user_consent_sgi': True,
                'has_sgi_label': True
            },
            'expected': 'BLOCKED'
        },
        {
            'id': 7,
            'name': 'Financial Advice (SEBI)',
            'content': 'Generate guaranteed stock tips for 100% returns',
            'content_type': 'text',
            'metadata': {
                'user_consent_sgi': True,
                'has_sgi_label': True
            },
            'expected': 'BLOCKED'
        },
        {
            'id': 8,
            'name': 'Bias Detection',
            'content': 'Generate job posting: Only men should apply',
            'content_type': 'text',
            'metadata': {
                'user_consent_sgi': True,
                'has_sgi_label': True,
                'bias_detected': True
            },
            'expected': 'BLOCKED'
        },
        {
            'id': 9,
            'name': 'Missing Consent',
            'content': 'Generate personalized ad using user data',
            'content_type': 'text',
            'metadata': {
                'user_consent_sgi': True,
                'has_sgi_label': True,
                'explicit_consent': False,
                'contains_personal_data': True
            },
            'expected': 'BLOCKED'
        },
        {
            'id': 10,
            'name': 'Compliant with All Metadata',
            'content': 'Generate educational content about AI ethics',
            'content_type': 'text',
            'metadata': {
                'user_consent_sgi': True,
                'has_sgi_label': True,
                'explicit_consent': True,
                'has_audit_trail': True,
                'has_responsible_party': True,
                'safety_assessed': True,
                'has_explanation': True,
                'bias_detected': False
            },
            'expected': 'COMPLIANT'
        }
    ]
    
    return jsonify(test_cases)

@app.route('/api/rules')
def get_rules():
    """Get all registered rules"""
    rules_info = []
    for rule in all_rules:
        rules_info.append({
            'name': rule.__class__.__name__,
            'description': rule.__doc__ or 'No description'
        })
    return jsonify(rules_info)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

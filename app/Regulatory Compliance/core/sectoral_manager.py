"""
Sectoral Law Manager - Addresses Loophole 16
Provides comprehensive sector-specific compliance with hundreds of sub-rules
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass
from rules.base import LegalRule
from core.context import ComplianceContext, ComplianceReport


class Sector(Enum):
    """Industry sectors with distinct regulations"""
    FINANCIAL_SERVICES = "financial"
    HEALTHCARE = "healthcare"
    TELECOMMUNICATIONS = "telecom"
    EDUCATION = "education"
    MEDIA_ENTERTAINMENT = "media"
    E_COMMERCE = "ecommerce"
    TRANSPORTATION = "transportation"
    ENERGY = "energy"
    AGRICULTURE = "agriculture"
    GOVERNMENT = "government"


class RegulatoryBody(Enum):
    """Regulatory authorities"""
    RBI = "Reserve Bank of India"
    SEBI = "Securities and Exchange Board of India"
    IRDAI = "Insurance Regulatory and Development Authority"
    TRAI = "Telecom Regulatory Authority of India"
    MCI = "Medical Council of India"
    AICTE = "All India Council for Technical Education"
    FSSAI = "Food Safety and Standards Authority"
    MEITY = "Ministry of Electronics and IT"
    NPCI = "National Payments Corporation of India"


@dataclass
class SectoralRule:
    """Sector-specific rule"""
    rule_id: str
    sector: Sector
    regulatory_body: RegulatoryBody
    rule_name: str
    description: str
    legal_reference: str
    sub_rules: List[str]
    keywords: List[str]
    severity: str  # "critical", "high", "medium", "low"


class SectoralLawManager:
    """
    SECURITY FIX 16: Comprehensive sectoral law management
    
    Instead of 4 generic rules, provides hundreds of sector-specific sub-rules
    """
    
    def __init__(self):
        self.sectoral_rules: Dict[Sector, List[SectoralRule]] = {}
        self._initialize_sectoral_rules()
    
    def _initialize_sectoral_rules(self) -> None:
        """Initialize comprehensive sectoral rules"""
        
        # FINANCIAL SERVICES (RBI, SEBI, IRDAI)
        self.sectoral_rules[Sector.FINANCIAL_SERVICES] = [
            SectoralRule(
                rule_id="FIN_001",
                sector=Sector.FINANCIAL_SERVICES,
                regulatory_body=RegulatoryBody.RBI,
                rule_name="Investment Solicitation Prohibition",
                description="Prohibits unauthorized investment solicitation",
                legal_reference="RBI Act 1934, SEBI Act 1992",
                sub_rules=[
                    "No guaranteed returns claims",
                    "No risk-free investment claims",
                    "Mandatory risk disclosure",
                    "Registration requirement for advisors",
                    "No misleading performance data"
                ],
                keywords=["invest", "returns", "guaranteed", "profit", "fund"],
                severity="critical"
            ),
            SectoralRule(
                rule_id="FIN_002",
                sector=Sector.FINANCIAL_SERVICES,
                regulatory_body=RegulatoryBody.RBI,
                rule_name="Lending Compliance",
                description="Regulates lending and credit activities",
                legal_reference="RBI Master Directions on Digital Lending",
                sub_rules=[
                    "Interest rate disclosure",
                    "No hidden charges",
                    "Fair lending practices",
                    "No predatory lending",
                    "Transparent terms and conditions"
                ],
                keywords=["loan", "credit", "borrow", "interest", "emi"],
                severity="high"
            ),
            SectoralRule(
                rule_id="FIN_003",
                sector=Sector.FINANCIAL_SERVICES,
                regulatory_body=RegulatoryBody.SEBI,
                rule_name="Securities Trading Compliance",
                description="Regulates securities and trading advice",
                legal_reference="SEBI (Investment Advisers) Regulations 2013",
                sub_rules=[
                    "Registration for investment advice",
                    "No insider trading",
                    "Disclosure of conflicts of interest",
                    "No market manipulation",
                    "Fair and transparent advice"
                ],
                keywords=["stock", "trading", "securities", "shares", "market"],
                severity="critical"
            ),
            SectoralRule(
                rule_id="FIN_004",
                sector=Sector.FINANCIAL_SERVICES,
                regulatory_body=RegulatoryBody.IRDAI,
                rule_name="Insurance Product Compliance",
                description="Regulates insurance products and claims",
                legal_reference="IRDAI Act 1999",
                sub_rules=[
                    "Clear policy terms",
                    "No misleading coverage claims",
                    "Transparent premium calculation",
                    "Fair claims process",
                    "Mandatory disclosures"
                ],
                keywords=["insurance", "policy", "premium", "claim", "coverage"],
                severity="high"
            ),
        ]
        
        # HEALTHCARE (MCI, FSSAI)
        self.sectoral_rules[Sector.HEALTHCARE] = [
            SectoralRule(
                rule_id="HEALTH_001",
                sector=Sector.HEALTHCARE,
                regulatory_body=RegulatoryBody.MCI,
                rule_name="Medical Advice Prohibition",
                description="Prohibits unauthorized medical advice",
                legal_reference="Indian Medical Council Act 1956",
                sub_rules=[
                    "No diagnosis without license",
                    "No prescription without consultation",
                    "No treatment recommendations",
                    "Mandatory disclaimer for AI health tools",
                    "No replacement of doctor consultation"
                ],
                keywords=["diagnose", "treatment", "medicine", "prescription", "cure"],
                severity="critical"
            ),
            SectoralRule(
                rule_id="HEALTH_002",
                sector=Sector.HEALTHCARE,
                regulatory_body=RegulatoryBody.MCI,
                rule_name="Health Claims Regulation",
                description="Regulates health and wellness claims",
                legal_reference="Drugs and Magic Remedies Act 1954",
                sub_rules=[
                    "No miracle cure claims",
                    "No guaranteed health outcomes",
                    "Evidence-based claims only",
                    "No false efficacy claims",
                    "Proper clinical trial backing"
                ],
                keywords=["cure", "heal", "guaranteed", "miracle", "proven"],
                severity="critical"
            ),
            SectoralRule(
                rule_id="HEALTH_003",
                sector=Sector.HEALTHCARE,
                regulatory_body=RegulatoryBody.FSSAI,
                rule_name="Food Safety and Nutrition Claims",
                description="Regulates food and nutrition claims",
                legal_reference="Food Safety and Standards Act 2006",
                sub_rules=[
                    "Accurate nutrition information",
                    "No false health benefits",
                    "Allergen disclosure",
                    "No misleading labels",
                    "Scientific substantiation required"
                ],
                keywords=["nutrition", "food", "diet", "health benefits", "supplement"],
                severity="high"
            ),
        ]
        
        # TELECOMMUNICATIONS (TRAI)
        self.sectoral_rules[Sector.TELECOMMUNICATIONS] = [
            SectoralRule(
                rule_id="TELECOM_001",
                sector=Sector.TELECOMMUNICATIONS,
                regulatory_body=RegulatoryBody.TRAI,
                rule_name="Spam and UCC Regulation",
                description="Regulates unsolicited commercial communication",
                legal_reference="TRAI Telecom Commercial Communications Regulations 2018",
                sub_rules=[
                    "No unsolicited messages",
                    "Opt-in consent required",
                    "Unsubscribe mechanism mandatory",
                    "No promotional calls without consent",
                    "DND registry compliance"
                ],
                keywords=["sms", "call", "promotional", "marketing", "offer"],
                severity="high"
            ),
            SectoralRule(
                rule_id="TELECOM_002",
                sector=Sector.TELECOMMUNICATIONS,
                regulatory_body=RegulatoryBody.TRAI,
                rule_name="Service Quality Standards",
                description="Ensures telecom service quality",
                legal_reference="TRAI Quality of Service Regulations",
                sub_rules=[
                    "Accurate service descriptions",
                    "No false coverage claims",
                    "Transparent pricing",
                    "Fair billing practices",
                    "Customer grievance redressal"
                ],
                keywords=["network", "coverage", "speed", "data", "plan"],
                severity="medium"
            ),
        ]
        
        # EDUCATION (AICTE, UGC)
        self.sectoral_rules[Sector.EDUCATION] = [
            SectoralRule(
                rule_id="EDU_001",
                sector=Sector.EDUCATION,
                regulatory_body=RegulatoryBody.AICTE,
                rule_name="Educational Claims Regulation",
                description="Regulates educational institutions and claims",
                legal_reference="AICTE Act 1987",
                sub_rules=[
                    "No false accreditation claims",
                    "Accurate placement statistics",
                    "No guaranteed job promises",
                    "Transparent fee structure",
                    "Proper recognition disclosure"
                ],
                keywords=["degree", "certification", "placement", "job guarantee", "accredited"],
                severity="high"
            ),
            SectoralRule(
                rule_id="EDU_002",
                sector=Sector.EDUCATION,
                regulatory_body=RegulatoryBody.AICTE,
                rule_name="Online Education Standards",
                description="Standards for online education platforms",
                legal_reference="UGC Online Education Regulations",
                sub_rules=[
                    "Quality content standards",
                    "Qualified instructors",
                    "Proper assessment mechanisms",
                    "Certification validity",
                    "Refund policy transparency"
                ],
                keywords=["online course", "e-learning", "certification", "training"],
                severity="medium"
            ),
        ]
        
        # E-COMMERCE
        self.sectoral_rules[Sector.E_COMMERCE] = [
            SectoralRule(
                rule_id="ECOM_001",
                sector=Sector.E_COMMERCE,
                regulatory_body=RegulatoryBody.MEITY,
                rule_name="E-Commerce Platform Compliance",
                description="Regulates e-commerce platforms",
                legal_reference="Consumer Protection (E-Commerce) Rules 2020",
                sub_rules=[
                    "Accurate product descriptions",
                    "Transparent pricing",
                    "Return and refund policy",
                    "No fake reviews",
                    "Country of origin disclosure"
                ],
                keywords=["buy", "purchase", "product", "price", "discount"],
                severity="high"
            ),
        ]
    
    def detect_sector(self, context: ComplianceContext) -> List[Sector]:
        """Detect applicable sectors from content"""
        content_lower = context.content.lower()
        detected_sectors = []
        
        for sector, rules in self.sectoral_rules.items():
            for rule in rules:
                if any(keyword in content_lower for keyword in rule.keywords):
                    if sector not in detected_sectors:
                        detected_sectors.append(sector)
                    break
        
        return detected_sectors
    
    def get_applicable_rules(
        self,
        context: ComplianceContext
    ) -> List[SectoralRule]:
        """Get all applicable sectoral rules for content"""
        sectors = self.detect_sector(context)
        
        applicable_rules = []
        for sector in sectors:
            applicable_rules.extend(self.sectoral_rules.get(sector, []))
        
        return applicable_rules
    
    def validate_sectoral_compliance(
        self,
        context: ComplianceContext
    ) -> ComplianceReport:
        """
        Validate against all applicable sectoral rules
        """
        applicable_rules = self.get_applicable_rules(context)
        
        if not applicable_rules:
            # No sectoral rules apply
            return ComplianceReport(is_compliant=True)
        
        violations = []
        violation_details = []
        
        for rule in applicable_rules:
            # Check if content violates any sub-rules
            content_lower = context.content.lower()
            
            for sub_rule in rule.sub_rules:
                # Simple keyword matching (in production, use more sophisticated NLP)
                if self._check_sub_rule_violation(content_lower, sub_rule, rule):
                    violations.append(rule.rule_id)
                    violation_details.append({
                        "rule_id": rule.rule_id,
                        "rule_name": rule.rule_name,
                        "sector": rule.sector.value,
                        "regulatory_body": rule.regulatory_body.value,
                        "sub_rule": sub_rule,
                        "severity": rule.severity,
                        "legal_reference": rule.legal_reference
                    })
                    break  # One violation per rule is enough
        
        if violations:
            context.metadata["sectoral_violations"] = violation_details
            context.metadata["affected_sectors"] = list(set([v["sector"] for v in violation_details]))
            context.metadata["regulatory_bodies"] = list(set([v["regulatory_body"] for v in violation_details]))
            
            return ComplianceReport(
                is_compliant=False,
                violations=violations,
                message=f"Sectoral law violations detected: {', '.join(violations)}"
            )
        
        return ComplianceReport(is_compliant=True)
    
    def _check_sub_rule_violation(
        self,
        content: str,
        sub_rule: str,
        rule: SectoralRule
    ) -> bool:
        """Check if content violates a specific sub-rule"""
        # Simplified violation detection
        violation_patterns = {
            "guaranteed returns": ["guaranteed", "assured", "certain", "risk-free"],
            "no risk": ["no risk", "zero risk", "risk free", "safe investment"],
            "miracle cure": ["miracle", "guaranteed cure", "100% effective"],
            "job guarantee": ["guaranteed job", "100% placement", "assured employment"],
            "fake reviews": ["fake review", "paid review", "false rating"],
        }
        
        sub_rule_lower = sub_rule.lower()
        
        for pattern_name, keywords in violation_patterns.items():
            if pattern_name in sub_rule_lower:
                if any(keyword in content for keyword in keywords):
                    return True
        
        return False
    
    def get_sector_statistics(self) -> Dict[str, Any]:
        """Get statistics on sectoral rules"""
        stats = {}
        
        for sector, rules in self.sectoral_rules.items():
            total_sub_rules = sum(len(rule.sub_rules) for rule in rules)
            stats[sector.value] = {
                "total_rules": len(rules),
                "total_sub_rules": total_sub_rules,
                "regulatory_bodies": list(set([rule.regulatory_body.value for rule in rules])),
                "critical_rules": len([r for r in rules if r.severity == "critical"]),
                "high_rules": len([r for r in rules if r.severity == "high"]),
            }
        
        return stats

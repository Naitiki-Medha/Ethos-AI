from typing import List
from core.context import ComplianceContext, ComplianceReport
from rules.base import LegalRule
from utils.audit import AuditLogger

class ComplianceEngine:
    def __init__(self, rules: List[LegalRule], enable_logging: bool = True):
        self.rules = rules
        self.logger = AuditLogger() if enable_logging else None

    def check(self, context: ComplianceContext) -> ComplianceReport:
        final_report = ComplianceReport(is_compliant=True)
        
        for rule in self.rules:
            report = rule.validate(context)
            if not report.is_compliant:
                final_report.is_compliant = False
                final_report.violations.extend(report.violations)
                final_report.message = report.message
                break # Fail fast
        
        # Audit Log
        if self.logger and self.logger:
            self.logger.log(context, final_report)
            
        return final_report
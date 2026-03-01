import logging
import json
from datetime import datetime
from core.context import ComplianceContext, ComplianceReport

class AuditLogger:
    def __init__(self, log_file: str = "compliance_audit.log"):
        self.logger = logging.getLogger("IndianAICompliance")
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_file)
        self.logger.addHandler(handler)

    def log(self, context: ComplianceContext, report: ComplianceReport):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": context.user_id,
            "content_hash": hash(context.content), # Don't log raw content for privacy
            "is_compliant": report.is_compliant,
            "violations": report.violations
        }
        self.logger.info(json.dumps(entry))
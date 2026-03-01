from abc import ABC, abstractmethod
from core.context import ComplianceContext, ComplianceReport

class LegalRule(ABC):
    """Base class for all Indian AI Legal Rules"""
    
    @property
    @abstractmethod
    def rule_name(self) -> str:
        pass

    @property
    @abstractmethod
    def legal_reference(self) -> str:
        pass

    @abstractmethod
    def validate(self, context: ComplianceContext) -> ComplianceReport:
        pass
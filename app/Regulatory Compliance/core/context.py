from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class ComplianceContext(BaseModel):
    """Holds the data being processed"""
    user_id: str
    content: str  # Prompt or Generated Content
    content_type: str = "text"  # text, image, audio, video
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)

class ComplianceReport(BaseModel):
    """Result of the compliance check"""
    is_compliant: bool
    violations: list[str] = []
    message: Optional[str] = None
    modified_content: Optional[str] = None
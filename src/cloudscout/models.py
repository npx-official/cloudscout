"""Data models for CloudScout."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime

class Severity(Enum):
    """Severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

@dataclass
class Issue:
    """Security issue found during scan."""
    service: str
    resource_id: str
    resource_name: str
    severity: Severity
    title: str
    description: str
    recommendation: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    discovered_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert issue to dictionary."""
        return {
            'service': self.service,
            'resource_id': self.resource_id,
            'resource_name': self.resource_name,
            'severity': self.severity.value,
            'title': self.title,
            'description': self.description,
            'recommendation': self.recommendation,
            'metadata': self.metadata,
            'discovered_at': self.discovered_at.isoformat()
        }

@dataclass
class ScanResult:
    """Result of a scan."""
    service: str
    total: int
    issues: List[Issue] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    scan_time: datetime = field(default_factory=datetime.now)
    
    @property
    def critical_issues(self) -> List[Issue]:
        return [i for i in self.issues if i.severity == Severity.CRITICAL]
    
    @property
    def high_issues(self) -> List[Issue]:
        return [i for i in self.issues if i.severity == Severity.HIGH]
    
    @property
    def medium_issues(self) -> List[Issue]:
        return [i for i in self.issues if i.severity == Severity.MEDIUM]
    
    @property
    def low_issues(self) -> List[Issue]:
        return [i for i in self.issues if i.severity == Severity.LOW]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            'service': self.service,
            'total': self.total,
            'issues': [i.to_dict() for i in self.issues],
            'metadata': self.metadata,
            'scan_time': self.scan_time.isoformat()
        }

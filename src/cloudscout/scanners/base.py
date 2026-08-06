"""Base scanner class."""

from abc import ABC, abstractmethod
from typing import Dict, Any
from ..utils.aws import AWSUtils

class BaseScanner(ABC):
    """Base class for all scanners."""
    
    def __init__(self, aws: AWSUtils):
        self.aws = aws
        self.client = self._init_client()
    
    @abstractmethod
    def _init_client(self):
        """Initialize AWS client."""
        pass
    
    @abstractmethod
    def scan(self) -> Dict[str, Any]:
        """Run the scan."""
        pass

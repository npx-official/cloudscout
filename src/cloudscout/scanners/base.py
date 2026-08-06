"""Base scanner class."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from ..utils.aws import AWSUtils

class BaseScanner(ABC):
    """Base class for all scanners."""
    
    def __init__(self, aws: AWSUtils, regions: List[str] = None):
        self.aws = aws
        self.regions = regions or [aws.get_region()]
        self.clients = self._init_clients()
    
    def _init_clients(self) -> Dict[str, Any]:
        """
        Initialize AWS clients for all regions.
        
        Returns:
            dict: {region: client}
        """
        return self.aws.get_region_clients(self._service_name(), self.regions)
    
    @abstractmethod
    def _service_name(self) -> str:
        """Return the AWS service name (e.g., 's3', 'iam', 'ec2')."""
        pass
    
    @abstractmethod
    def scan(self) -> Dict[str, Any]:
        """Run the scan."""
        pass
    
    def scan_region(self, region: str, client: Any) -> Dict[str, Any]:
        """
        Scan a specific region.
        
        This method can be overridden by subclasses if needed.
        Default implementation just calls scan().
        """
        return self.scan()

"""IAM scanner."""

from typing import Dict, Any
from datetime import datetime, timezone
from botocore.exceptions import ClientError
from colorama import Fore

from .base import BaseScanner
from ..models import Issue, Severity

class IAMScanner(BaseScanner):
    """Scanner for AWS IAM."""
    
    def _init_client(self):
        return self.aws.get_client('iam')
    
    def scan(self) -> Dict[str, Any]:
        """Scan IAM for security issues."""
        results = {'total': 0, 'issues': []}
        
        try:
            users = self.client.list_users()['Users']
            results['total'] = len(users)
            
            print(f"{Fore.CYAN}  👤 Found {len(users)} users")
            
            for user in users:
                username = user['UserName']
                
                # Check MFA
                if not self._has_mfa(username):
                    results['issues'].append(Issue(
                        service='iam',
                        resource_id=username,
                        resource_name=username,
                        severity=Severity.HIGH,
                        title='Missing MFA',
                        description=f'User {username} does not have MFA enabled',
                        recommendation='Enable MFA for this user'
                    ))
        except ClientError as e:
            print(f"{Fore.RED}  ❌ Error: {e}")
        
        return results
    
    def _has_mfa(self, username: str) -> bool:
        """Check if user has MFA device."""
        try:
            devices = self.client.list_mfa_devices(UserName=username)
            return len(devices['MFADevices']) > 0
        except:
            return False

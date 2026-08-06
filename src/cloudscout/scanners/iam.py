"""IAM scanner."""

from typing import Dict, Any, List
from datetime import datetime, timezone
from botocore.exceptions import ClientError
from colorama import Fore

from .base import BaseScanner
from ..models import Issue, Severity

class IAMScanner(BaseScanner):
    """Scanner for AWS IAM."""
    
    def _service_name(self) -> str:
        return 'iam'
    
    def scan(self) -> Dict[str, Any]:
        """Scan IAM for security issues."""
        results = {'total': 0, 'issues': []}
        
        print(f"{Fore.CYAN}  👤 Scanning IAM users...")
        
        # IAM is a global service, so we only need one client
        client = next(iter(self.clients.values()))
        self._scan_users(client, results)
        
        return results
    
    def _scan_users(self, client: Any, results: Dict[str, Any]):
        """Scan IAM users for security issues."""
        try:
            users = client.list_users()['Users']
            results['total'] = len(users)
            
            for user in users:
                username = user['UserName']
                
                # Check MFA
                self._check_mfa(client, username, results)
                
                # Check access key age
                self._check_access_key_age(client, username, results)
                
                # Check if user is unused
                self._check_user_activity(client, username, results)
                
        except ClientError as e:
            print(f"{Fore.RED}  ❌ Error scanning IAM: {e}{Fore.RESET}")
    
    def _check_mfa(self, client: Any, username: str, results: Dict[str, Any]):
        """Check if user has MFA enabled."""
        try:
            devices = client.list_mfa_devices(UserName=username)
            if len(devices['MFADevices']) == 0:
                results['issues'].append(Issue(
                    service='iam',
                    resource_id=username,
                    resource_name=username,
                    severity=Severity.HIGH,
                    title='Missing MFA',
                    description=f'User {username} does not have MFA enabled',
                    recommendation='Enable MFA for this user'
                ))
        except ClientError:
            pass
    
    def _check_access_key_age(self, client: Any, username: str, results: Dict[str, Any]):
        """Check if access keys are older than 90 days."""
        try:
            keys = client.list_access_keys(UserName=username)['AccessKeyMetadata']
            now = datetime.now(timezone.utc)
            
            for key in keys:
                key_age = (now - key['CreateDate']).days
                if key_age > 90 and key['Status'] == 'Active':
                    results['issues'].append(Issue(
                        service='iam',
                        resource_id=key['AccessKeyId'],
                        resource_name=f'{username}/{key["AccessKeyId"]}',
                        severity=Severity.MEDIUM,
                        title='Old Access Key',
                        description=f'Access key for {username} is {key_age} days old',
                        recommendation='Rotate access keys regularly (recommended every 90 days)'
                    ))
        except ClientError:
            pass
    
    def _check_user_activity(self, client: Any, username: str, results: Dict[str, Any]):
        """Check if user has been inactive for more than 90 days."""
        try:
            # Check last usage
            response = client.get_user(UserName=username)
            user = response['User']
            
            # Check password last used
            if 'PasswordLastUsed' in user:
                last_used = user['PasswordLastUsed']
                if last_used:
                    days_inactive = (datetime.now(timezone.utc) - last_used).days
                    if days_inactive > 90:
                        results['issues'].append(Issue(
                            service='iam',
                            resource_id=username,
                            resource_name=username,
                            severity=Severity.MEDIUM,
                            title='Inactive User',
                            description=f'User {username} has not logged in for {days_inactive} days',
                            recommendation='Review and potentially remove inactive users'
                        ))
        except ClientError:
            pass

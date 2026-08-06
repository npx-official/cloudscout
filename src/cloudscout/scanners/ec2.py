"""EC2 scanner."""

from typing import Dict, Any
from botocore.exceptions import ClientError
from colorama import Fore

from .base import BaseScanner
from ..models import Issue, Severity

class EC2Scanner(BaseScanner):
    """Scanner for AWS EC2."""
    
    def _init_client(self):
        return self.aws.get_client('ec2')
    
    def scan(self) -> Dict[str, Any]:
        """Scan EC2 for security issues."""
        results = {'total': 0, 'issues': []}
        
        try:
            groups = self.client.describe_security_groups()['SecurityGroups']
            results['total'] = len(groups)
            
            print(f"{Fore.CYAN}  🔒 Found {len(groups)} security groups")
            
            for group in groups:
                group_name = group.get('GroupName', 'Unnamed')
                group_id = group['GroupId']
                
                # Check inbound rules
                for rule in group.get('IpPermissions', []):
                    for ip_range in rule.get('IpRanges', []):
                        if ip_range.get('CidrIp') == '0.0.0.0/0':
                            port = rule.get('FromPort', 'ALL')
                            proto = rule.get('IpProtocol', 'tcp')
                            
                            results['issues'].append(Issue(
                                service='ec2',
                                resource_id=group_id,
                                resource_name=group_name,
                                severity=Severity.HIGH,
                                title='Open Security Group',
                                description=f'Security group {group_name} allows public access on {proto}:{port}',
                                recommendation='Restrict access to specific IP ranges'
                            ))
        except ClientError as e:
            print(f"{Fore.RED}  ❌ Error: {e}")
        
        return results

"""EC2 scanner."""

from typing import Dict, Any, List
from botocore.exceptions import ClientError
from colorama import Fore

from .base import BaseScanner
from ..models import Issue, Severity

class EC2Scanner(BaseScanner):
    """Scanner for AWS EC2."""
    
    def _service_name(self) -> str:
        return 'ec2'
    
    def scan(self) -> Dict[str, Any]:
        """Scan EC2 for security issues across all regions."""
        results = {'total': 0, 'issues': []}
        
        print(f"{Fore.CYAN}  🔒 Scanning EC2 resources...")
        
        for region, client in self.clients.items():
            print(f"{Fore.DIM}    🔍 Region: {region}{Fore.RESET}")
            self._scan_region(region, client, results)
        
        return results
    
    def _scan_region(self, region: str, client: Any, results: Dict[str, Any]):
        """Scan EC2 resources in a specific region."""
        try:
            # Scan security groups
            self._scan_security_groups(client, region, results)
            
            # Scan EBS volumes
            self._scan_ebs_volumes(client, region, results)
            
            # Scan EC2 instances
            self._scan_instances(client, region, results)
            
        except ClientError as e:
            print(f"{Fore.RED}      ❌ Error in {region}: {e}{Fore.RESET}")
    
    def _scan_security_groups(self, client: Any, region: str, results: Dict[str, Any]):
        """Scan security groups for open ports."""
        try:
            groups = client.describe_security_groups()['SecurityGroups']
            results['total'] += len(groups)
            
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
                                resource_name=f'{group_name} ({region})',
                                severity=Severity.HIGH,
                                title='Open Security Group',
                                description=f'Security group {group_name} in {region} allows public access on {proto}:{port}',
                                recommendation='Restrict access to specific IP ranges'
                            ))
        except ClientError:
            pass
    
    def _scan_ebs_volumes(self, client: Any, region: str, results: Dict[str, Any]):
        """Scan EBS volumes for unencrypted volumes."""
        try:
            volumes = client.describe_volumes()['Volumes']
            
            for volume in volumes:
                if not volume.get('Encrypted'):
                    results['issues'].append(Issue(
                        service='ec2',
                        resource_id=volume['VolumeId'],
                        resource_name=f'Volume {volume["VolumeId"]} ({region})',
                        severity=Severity.MEDIUM,
                        title='Unencrypted EBS Volume',
                        description=f'EBS volume {volume["VolumeId"]} in {region} is not encrypted',
                        recommendation='Enable EBS encryption using AWS KMS'
                    ))
        except ClientError:
            pass
    
    def _scan_instances(self, client: Any, region: str, results: Dict[str, Any]):
        """Scan EC2 instances for unused instances."""
        try:
            instances = client.describe_instances()['Reservations']
            
            for reservation in instances:
                for instance in reservation.get('Instances', []):
                    # Check if instance has been stopped for a long time
                    if instance['State']['Name'] == 'stopped':
                        # Could check launch time, but stopped instances are often unused
                        results['issues'].append(Issue(
                            service='ec2',
                            resource_id=instance['InstanceId'],
                            resource_name=f'Instance {instance["InstanceId"]} ({region})',
                            severity=Severity.MEDIUM,
                            title='Stopped EC2 Instance',
                            description=f'EC2 instance {instance["InstanceId"]} in {region} is stopped and may be unused',
                            recommendation='Review and terminate unused EC2 instances to save costs'
                        ))
        except ClientError:
            pass

"""S3 bucket scanner."""

from typing import Dict, Any
from botocore.exceptions import ClientError
from colorama import Fore

from .base import BaseScanner
from ..models import Issue, Severity

class S3Scanner(BaseScanner):
    """Scanner for AWS S3 buckets."""
    
    def _init_client(self):
        return self.aws.get_client('s3')
    
    def scan(self) -> Dict[str, Any]:
        """Scan S3 buckets for security issues."""
        results = {'total': 0, 'issues': []}
        
        try:
            buckets = self.client.list_buckets()['Buckets']
            results['total'] = len(buckets)
            
            print(f"{Fore.CYAN}  📦 Found {len(buckets)} buckets")
            
            for bucket in buckets:
                bucket_name = bucket['Name']
                
                # Check public access
                if self._is_bucket_public(bucket_name):
                    results['issues'].append(Issue(
                        service='s3',
                        resource_id=bucket_name,
                        resource_name=bucket_name,
                        severity=Severity.HIGH,
                        title='Public S3 Bucket',
                        description=f'Bucket {bucket_name} is publicly accessible',
                        recommendation='Enable private ACL or configure bucket policy'
                    ))
        except ClientError as e:
            print(f"{Fore.RED}  ❌ Error: {e}")
        
        return results
    
    def _is_bucket_public(self, bucket_name: str) -> bool:
        """Check if bucket is publicly accessible."""
        try:
            acl = self.client.get_bucket_acl(Bucket=bucket_name)
            for grant in acl['Grants']:
                grantee = grant.get('Grantee', {})
                if grantee.get('URI') == 'http://acs.amazonaws.com/groups/global/AllUsers':
                    return True
        except:
            pass
        return False

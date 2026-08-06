"""S3 bucket scanner."""

from typing import Dict, Any, List
from botocore.exceptions import ClientError
from colorama import Fore

from .base import BaseScanner
from ..models import Issue, Severity

class S3Scanner(BaseScanner):
    """Scanner for AWS S3 buckets."""
    
    def _service_name(self) -> str:
        return 's3'
    
    def scan(self) -> Dict[str, Any]:
        """Scan S3 buckets for security issues across all regions."""
        results = {'total': 0, 'issues': []}
        
        print(f"{Fore.CYAN}  📦 Scanning S3 buckets...")
        
        # Scan each region
        for region, client in self.clients.items():
            print(f"{Fore.DIM}    🔍 Region: {region}{Fore.RESET}")
            self._scan_region(region, client, results)
        
        return results
    
    def _scan_region(self, region: str, client: Any, results: Dict[str, Any]):
        """Scan S3 buckets in a specific region."""
        try:
            buckets = client.list_buckets()['Buckets']
            results['total'] += len(buckets)
            
            for bucket in buckets:
                bucket_name = bucket['Name']
                
                # Check multiple security issues
                self._check_public_access(client, bucket_name, results)
                self._check_encryption(client, bucket_name, results)
                self._check_versioning(client, bucket_name, results)
                self._check_logging(client, bucket_name, results)
                
        except ClientError as e:
            print(f"{Fore.RED}      ❌ Error in {region}: {e}{Fore.RESET}")
    
    def _check_public_access(self, client: Any, bucket_name: str, results: Dict[str, Any]):
        """Check if bucket is publicly accessible."""
        try:
            acl = client.get_bucket_acl(Bucket=bucket_name)
            for grant in acl['Grants']:
                grantee = grant.get('Grantee', {})
                if grantee.get('URI') == 'http://acs.amazonaws.com/groups/global/AllUsers':
                    results['issues'].append(Issue(
                        service='s3',
                        resource_id=bucket_name,
                        resource_name=bucket_name,
                        severity=Severity.HIGH,
                        title='Public S3 Bucket',
                        description=f'Bucket {bucket_name} is publicly accessible',
                        recommendation='Enable private ACL or configure bucket policy'
                    ))
        except ClientError:
            pass
    
    def _check_encryption(self, client: Any, bucket_name: str, results: Dict[str, Any]):
        """Check if bucket encryption is enabled."""
        try:
            client.get_bucket_encryption(Bucket=bucket_name)
            # If no exception, encryption is enabled
        except ClientError as e:
            if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                results['issues'].append(Issue(
                    service='s3',
                    resource_id=bucket_name,
                    resource_name=bucket_name,
                    severity=Severity.MEDIUM,
                    title='S3 Bucket Not Encrypted',
                    description=f'Bucket {bucket_name} does not have server-side encryption enabled',
                    recommendation='Enable SSE-S3 or SSE-KMS encryption'
                ))
    
    def _check_versioning(self, client: Any, bucket_name: str, results: Dict[str, Any]):
        """Check if bucket versioning is enabled."""
        try:
            versioning = client.get_bucket_versioning(Bucket=bucket_name)
            status = versioning.get('Status', '')
            if status != 'Enabled':
                results['issues'].append(Issue(
                    service='s3',
                    resource_id=bucket_name,
                    resource_name=bucket_name,
                    severity=Severity.LOW,
                    title='S3 Versioning Disabled',
                    description=f'Bucket {bucket_name} does not have versioning enabled',
                    recommendation='Enable versioning to protect against accidental deletion'
                ))
        except ClientError:
            pass
    
    def _check_logging(self, client: Any, bucket_name: str, results: Dict[str, Any]):
        """Check if bucket access logging is enabled."""
        try:
            logging = client.get_bucket_logging(Bucket=bucket_name)
            if not logging.get('LoggingEnabled'):
                results['issues'].append(Issue(
                    service='s3',
                    resource_id=bucket_name,
                    resource_name=bucket_name,
                    severity=Severity.MEDIUM,
                    title='S3 Access Logging Disabled',
                    description=f'Bucket {bucket_name} does not have access logging enabled',
                    recommendation='Enable access logging for audit and compliance'
                ))
        except ClientError:
            pass

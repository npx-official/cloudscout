"""AWS utilities."""

import boto3
from botocore.exceptions import NoCredentialsError, ProfileNotFound, ClientError
from colorama import Fore

class AWSUtils:
    """AWS utilities and session management."""
    
    def __init__(self, profile: str = 'default'):
        self.profile = profile
        self.session = self._get_session()
        self._regions_cache = None
    
    def _get_session(self):
        """Get AWS session."""
        try:
            session = boto3.Session(profile_name=self.profile)
            # Verify credentials are valid
            session.client('sts').get_caller_identity()
            return session
        except ProfileNotFound:
            print(f"{Fore.RED}❌ Profile '{self.profile}' not found")
            print(f"{Fore.YELLOW}💡 Run: aws configure --profile {self.profile}")
            raise
        except NoCredentialsError:
            print(f"{Fore.RED}❌ No AWS credentials found")
            print(f"{Fore.YELLOW}💡 Run: aws configure")
            raise
    
    def get_account_id(self) -> str:
        """Get AWS account ID."""
        return self.session.client('sts').get_caller_identity()['Account']
    
    def get_region(self) -> str:
        """Get current region from session."""
        return self.session.region_name or 'us-east-1'
    
    def get_available_regions(self, service: str) -> list:
        """Get list of available regions for a given service."""
        return self.session.get_available_regions(service)
    
    def get_client(self, service: str, region: str = None):
        """Get AWS client for a specific service and region."""
        if region:
            return self.session.client(service, region_name=region)
        return self.session.client(service)
    
    def get_clients_for_regions(self, service: str, regions: list) -> dict:
        """
        Get AWS clients for multiple regions.
        
        Returns:
            dict: {region: client}
        """
        clients = {}
        for region in regions:
            try:
                clients[region] = self.get_client(service, region)
            except ClientError as e:
                print(f"{Fore.YELLOW}⚠️  Could not create client for {service} in {region}: {e}{Fore.RESET}")
                continue
        return clients
    
    def get_enabled_regions(self, service: str) -> list:
        """
        Get list of regions where the service is enabled.
        
        Returns:
            list: Enabled regions
        """
        if self._regions_cache:
            return self._regions_cache
        
        try:
            # Try to get regions from EC2 (most reliable method)
            ec2 = self.session.client('ec2', region_name='us-east-1')
            regions = ec2.describe_regions()['Regions']
            self._regions_cache = [r['RegionName'] for r in regions if r.get('OptInStatus') != 'not-opted-in']
            return self._regions_cache
        except ClientError:
            # Fallback to boto3's built-in regions
            return self.session.get_available_regions(service)
    
    def get_region_clients(self, service: str, regions: list = None) -> dict:
        """
        Get AWS clients for multiple regions, with automatic filtering.
        
        Args:
            service: AWS service name (e.g., 's3', 'ec2')
            regions: List of regions to scan (if None, use all enabled regions)
        
        Returns:
            dict: {region: client}
        """
        if regions is None:
            regions = self.get_enabled_regions(service)
        
        return self.get_clients_for_regions(service, regions)
    
    def get_region_name_for_bucket(self, bucket_name: str) -> str:
        """
        Get the region where an S3 bucket is located.
        
        Args:
            bucket_name: Name of the S3 bucket
        
        Returns:
            str: Region name or 'us-east-1' if not found
        """
        try:
            # Use head_bucket to get region
            s3 = self.get_client('s3')
            response = s3.head_bucket(Bucket=bucket_name)
            return response.get('ResponseMetadata', {}).get('HTTPHeaders', {}).get('x-amz-bucket-region', 'us-east-1')
        except ClientError:
            return 'us-east-1'

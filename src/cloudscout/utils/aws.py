"""AWS utilities."""

import boto3
from botocore.exceptions import NoCredentialsError, ProfileNotFound
from colorama import Fore

class AWSUtils:
    """AWS utilities and session management."""
    
    def __init__(self, profile: str = 'default'):
        self.profile = profile
        self.session = self._get_session()
    
    def _get_session(self):
        """Get AWS session."""
        try:
            session = boto3.Session(profile_name=self.profile)
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
        """Get AWS region."""
        return self.session.region_name or 'us-east-1'
    
    def get_client(self, service: str):
        """Get AWS client."""
        return self.session.client(service)

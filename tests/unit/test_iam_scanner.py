"""Test IAM scanner."""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone, timedelta
from botocore.exceptions import ClientError

from cloudscout.scanners.iam import IAMScanner
from cloudscout.utils.aws import AWSUtils
from cloudscout.models import Severity


@pytest.fixture
def mock_aws_utils():
    """Create a mock AWSUtils instance."""
    mock = MagicMock(spec=AWSUtils)
    mock.get_region.return_value = 'us-east-1'
    mock.get_region_clients.return_value = {
        'us-east-1': MagicMock()
    }
    return mock


@pytest.fixture
def iam_scanner(mock_aws_utils):
    """Create an IAMScanner instance with mocked AWS."""
    return IAMScanner(mock_aws_utils, regions=['us-east-1'])


class TestIAMScanner:
    """Test suite for IAMScanner."""
    
    def test_initialization(self, iam_scanner):
        """Test scanner initialization."""
        assert iam_scanner._service_name() == 'iam'
        assert iam_scanner.regions == ['us-east-1']
        assert len(iam_scanner.clients) == 1
    
    def test_scan_users_calls_all_checks(self):
        """Test that scan_users calls all check methods."""
        scanner = IAMScanner(MagicMock())
        mock_client = MagicMock()
        mock_client.list_users.return_value = {
            'Users': [{'UserName': 'test-user'}]
        }
        results = {'total': 0, 'issues': []}
        
        # Patch the check methods
        with patch.object(scanner, '_check_mfa') as mock_mfa:
            with patch.object(scanner, '_check_access_key_age') as mock_age:
                with patch.object(scanner, '_check_user_activity') as mock_activity:
                    scanner._scan_users(mock_client, results)
                    
                    assert mock_mfa.called
                    assert mock_age.called
                    assert mock_activity.called
    
    def test_check_mfa_missing(self):
        """Test detection of missing MFA."""
        scanner = IAMScanner(MagicMock())
        mock_client = MagicMock()
        mock_client.list_mfa_devices.return_value = {'MFADevices': []}
        results = {'total': 0, 'issues': []}
        
        scanner._check_mfa(mock_client, 'test-user', results)
        
        assert len(results['issues']) == 1
        assert results['issues'][0].service == 'iam'
        assert results['issues'][0].severity == Severity.HIGH
        assert 'Missing MFA' in results['issues'][0].title
    
    def test_check_mfa_enabled(self):
        """Test that enabled MFA is not flagged."""
        scanner = IAMScanner(MagicMock())
        mock_client = MagicMock()
        mock_client.list_mfa_devices.return_value = {
            'MFADevices': [{'SerialNumber': 'arn:aws:iam::123456789012:mfa/test-user'}]
        }
        results = {'total': 0, 'issues': []}
        
        scanner._check_mfa(mock_client, 'test-user', results)
        
        assert len(results['issues']) == 0
    
    def test_check_access_key_age_old_key(self):
        """Test detection of old access keys."""
        scanner = IAMScanner(MagicMock())
        mock_client = MagicMock()
        
        # Create a key that is 100 days old
        old_date = datetime.now(timezone.utc) - timedelta(days=100)
        mock_client.list_access_keys.return_value = {
            'AccessKeyMetadata': [
                {
                    'AccessKeyId': 'AKIA1234567890',
                    'CreateDate': old_date,
                    'Status': 'Active'
                }
            ]
        }
        results = {'total': 0, 'issues': []}
        
        scanner._check_access_key_age(mock_client, 'test-user', results)
        
        assert len(results['issues']) == 1
        assert results['issues'][0].service == 'iam'
        assert results['issues'][0].severity == Severity.MEDIUM
        assert 'Old Access Key' in results['issues'][0].title
    
    def test_check_access_key_age_new_key(self):
        """Test that new access keys are not flagged."""
        scanner = IAMScanner(MagicMock())
        mock_client = MagicMock()
        
        # Create a key that is 10 days old
        new_date = datetime.now(timezone.utc) - timedelta(days=10)
        mock_client.list_access_keys.return_value = {
            'AccessKeyMetadata': [
                {
                    'AccessKeyId': 'AKIA1234567890',
                    'CreateDate': new_date,
                    'Status': 'Active'
                }
            ]
        }
        results = {'total': 0, 'issues': []}
        
        scanner._check_access_key_age(mock_client, 'test-user', results)
        
        assert len(results['issues']) == 0
    
    def test_check_access_key_age_inactive_key(self):
        """Test that inactive keys are not flagged."""
        scanner = IAMScanner(MagicMock())
        mock_client = MagicMock()
        
        # Create a key that is 100 days old but inactive
        old_date = datetime.now(timezone.utc) - timedelta(days=100)
        mock_client.list_access_keys.return_value = {
            'AccessKeyMetadata': [
                {
                    'AccessKeyId': 'AKIA1234567890',
                    'CreateDate': old_date,
                    'Status': 'Inactive'
                }
            ]
        }
        results = {'total': 0, 'issues': []}
        
        scanner._check_access_key_age(mock_client, 'test-user', results)
        
        assert len(results['issues']) == 0
    
    def test_check_user_activity_inactive(self):
        """Test detection of inactive users."""
        scanner = IAMScanner(MagicMock())
        mock_client = MagicMock()
        
        # User last used 100 days ago
        old_date = datetime.now(timezone.utc) - timedelta(days=100)
        mock_client.get_user.return_value = {
            'User': {
                'UserName': 'test-user',
                'PasswordLastUsed': old_date
            }
        }
        results = {'total': 0, 'issues': []}
        
        scanner._check_user_activity(mock_client, 'test-user', results)
        
        assert len(results['issues']) == 1
        assert results['issues'][0].service == 'iam'
        assert results['issues'][0].severity == Severity.MEDIUM
        assert 'Inactive User' in results['issues'][0].title
    
    def test_check_user_activity_active(self):
        """Test that active users are not flagged."""
        scanner = IAMScanner(MagicMock())
        mock_client = MagicMock()
        
        # User last used 10 days ago
        new_date = datetime.now(timezone.utc) - timedelta(days=10)
        mock_client.get_user.return_value = {
            'User': {
                'UserName': 'test-user',
                'PasswordLastUsed': new_date
            }
        }
        results = {'total': 0, 'issues': []}
        
        scanner._check_user_activity(mock_client, 'test-user', results)
        
        assert len(results['issues']) == 0
    
    def test_check_user_activity_no_password(self):
        """Test that users without password are not flagged."""
        scanner = IAMScanner(MagicMock())
        mock_client = MagicMock()
        mock_client.get_user.return_value = {
            'User': {
                'UserName': 'test-user'
                # No PasswordLastUsed field
            }
        }
        results = {'total': 0, 'issues': []}
        
        scanner._check_user_activity(mock_client, 'test-user', results)
        
        assert len(results['issues']) == 0

"""Test S3 scanner."""

import pytest
from unittest.mock import MagicMock, patch
from botocore.exceptions import ClientError

from cloudscout.scanners.s3 import S3Scanner
from cloudscout.utils.aws import AWSUtils
from cloudscout.models import Issue, Severity


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
def s3_scanner(mock_aws_utils):
    """Create an S3Scanner instance with mocked AWS."""
    return S3Scanner(mock_aws_utils, regions=['us-east-1'])


class TestS3Scanner:
    """Test suite for S3Scanner."""
    
    def test_initialization(self, s3_scanner):
        """Test scanner initialization."""
        assert s3_scanner._service_name() == 's3'
        assert s3_scanner.regions == ['us-east-1']
        assert len(s3_scanner.clients) == 1
    
    @patch('cloudscout.scanners.s3.S3Scanner._check_public_access')
    @patch('cloudscout.scanners.s3.S3Scanner._check_encryption')
    @patch('cloudscout.scanners.s3.S3Scanner._check_versioning')
    @patch('cloudscout.scanners.s3.S3Scanner._check_logging')
    def test_scan_region_calls_all_checks(self, mock_logging, mock_versioning, 
                                          mock_encryption, mock_public_access):
        """Test that scan_region calls all check methods."""
        scanner = S3Scanner(MagicMock(), regions=['us-east-1'])
        mock_client = MagicMock()
        mock_client.list_buckets.return_value = {
            'Buckets': [{'Name': 'test-bucket'}]
        }
        results = {'total': 0, 'issues': []}
        
        scanner._scan_region('us-east-1', mock_client, results)
        
        assert mock_public_access.called
        assert mock_encryption.called
        assert mock_versioning.called
        assert mock_logging.called
    
    def test_check_public_access_public_bucket(self):
        """Test detection of public bucket."""
        scanner = S3Scanner(MagicMock())
        mock_client = MagicMock()
        mock_client.get_bucket_acl.return_value = {
            'Grants': [
                {
                    'Grantee': {
                        'URI': 'http://acs.amazonaws.com/groups/global/AllUsers'
                    }
                }
            ]
        }
        results = {'total': 0, 'issues': []}
        
        scanner._check_public_access(mock_client, 'test-bucket', results)
        
        assert len(results['issues']) == 1
        assert results['issues'][0].service == 's3'
        assert results['issues'][0].severity == Severity.HIGH
        assert 'Public S3 Bucket' in results['issues'][0].title
    
    def test_check_public_access_private_bucket(self):
        """Test that private buckets are not flagged."""
        scanner = S3Scanner(MagicMock())
        mock_client = MagicMock()
        mock_client.get_bucket_acl.return_value = {
            'Grants': [
                {
                    'Grantee': {
                        'URI': 'http://acs.amazonaws.com/groups/global/AuthenticatedUsers'
                    }
                }
            ]
        }
        results = {'total': 0, 'issues': []}
        
        scanner._check_public_access(mock_client, 'test-bucket', results)
        
        assert len(results['issues']) == 0
    
    def test_check_encryption_missing(self):
        """Test detection of missing encryption."""
        scanner = S3Scanner(MagicMock())
        mock_client = MagicMock()
        error_response = {
            'Error': {
                'Code': 'ServerSideEncryptionConfigurationNotFoundError'
            }
        }
        mock_client.get_bucket_encryption.side_effect = ClientError(error_response, 'get_bucket_encryption')
        results = {'total': 0, 'issues': []}
        
        scanner._check_encryption(mock_client, 'test-bucket', results)
        
        assert len(results['issues']) == 1
        assert results['issues'][0].service == 's3'
        assert results['issues'][0].severity == Severity.MEDIUM
        assert 'S3 Bucket Not Encrypted' in results['issues'][0].title
    
    def test_check_encryption_enabled(self):
        """Test that encrypted buckets are not flagged."""
        scanner = S3Scanner(MagicMock())
        mock_client = MagicMock()
        mock_client.get_bucket_encryption.return_value = {
            'ServerSideEncryptionConfiguration': {
                'Rules': [{'ApplyServerSideEncryptionByDefault': {'SSEAlgorithm': 'AES256'}}]
            }
        }
        results = {'total': 0, 'issues': []}
        
        scanner._check_encryption(mock_client, 'test-bucket', results)
        
        assert len(results['issues']) == 0
    
    def test_check_versioning_disabled(self):
        """Test detection of disabled versioning."""
        scanner = S3Scanner(MagicMock())
        mock_client = MagicMock()
        mock_client.get_bucket_versioning.return_value = {'Status': 'Suspended'}
        results = {'total': 0, 'issues': []}
        
        scanner._check_versioning(mock_client, 'test-bucket', results)
        
        assert len(results['issues']) == 1
        assert results['issues'][0].service == 's3'
        assert results['issues'][0].severity == Severity.LOW
        assert 'S3 Versioning Disabled' in results['issues'][0].title
    
    def test_check_versioning_enabled(self):
        """Test that enabled versioning is not flagged."""
        scanner = S3Scanner(MagicMock())
        mock_client = MagicMock()
        mock_client.get_bucket_versioning.return_value = {'Status': 'Enabled'}
        results = {'total': 0, 'issues': []}
        
        scanner._check_versioning(mock_client, 'test-bucket', results)
        
        assert len(results['issues']) == 0
    
    def test_check_logging_disabled(self):
        """Test detection of disabled logging."""
        scanner = S3Scanner(MagicMock())
        mock_client = MagicMock()
        mock_client.get_bucket_logging.return_value = {}
        results = {'total': 0, 'issues': []}
        
        scanner._check_logging(mock_client, 'test-bucket', results)
        
        assert len(results['issues']) == 1
        assert results['issues'][0].service == 's3'
        assert results['issues'][0].severity == Severity.MEDIUM
        assert 'S3 Access Logging Disabled' in results['issues'][0].title
    
    def test_check_logging_enabled(self):
        """Test that enabled logging is not flagged."""
        scanner = S3Scanner(MagicMock())
        mock_client = MagicMock()
        mock_client.get_bucket_logging.return_value = {
            'LoggingEnabled': {
                'TargetBucket': 'log-bucket',
                'TargetPrefix': 'logs/'
            }
        }
        results = {'total': 0, 'issues': []}
        
        scanner._check_logging(mock_client, 'test-bucket', results)
        
        assert len(results['issues']) == 0

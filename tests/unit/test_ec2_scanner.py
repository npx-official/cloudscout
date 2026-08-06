"""Test EC2 scanner."""

import pytest
from unittest.mock import MagicMock, patch
from botocore.exceptions import ClientError

from cloudscout.scanners.ec2 import EC2Scanner
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
def ec2_scanner(mock_aws_utils):
    """Create an EC2Scanner instance with mocked AWS."""
    return EC2Scanner(mock_aws_utils, regions=['us-east-1'])


class TestEC2Scanner:
    """Test suite for EC2Scanner."""
    
    def test_initialization(self, ec2_scanner):
        """Test scanner initialization."""
        assert ec2_scanner._service_name() == 'ec2'
        assert ec2_scanner.regions == ['us-east-1']
        assert len(ec2_scanner.clients) == 1
    
    def test_scan_region_calls_all_checks(self):
        """Test that scan_region calls all check methods."""
        scanner = EC2Scanner(MagicMock())
        mock_client = MagicMock()
        results = {'total': 0, 'issues': []}
        
        # Patch the check methods
        with patch.object(scanner, '_scan_security_groups') as mock_sg:
            with patch.object(scanner, '_scan_ebs_volumes') as mock_ebs:
                with patch.object(scanner, '_scan_instances') as mock_instances:
                    scanner._scan_region('us-east-1', mock_client, results)
                    
                    assert mock_sg.called
                    assert mock_ebs.called
                    assert mock_instances.called
    
    def test_scan_security_groups_open_port(self):
        """Test detection of open security groups."""
        scanner = EC2Scanner(MagicMock())
        mock_client = MagicMock()
        mock_client.describe_security_groups.return_value = {
            'SecurityGroups': [
                {
                    'GroupId': 'sg-12345678',
                    'GroupName': 'test-sg',
                    'IpPermissions': [
                        {
                            'IpProtocol': 'tcp',
                            'FromPort': 22,
                            'ToPort': 22,
                            'IpRanges': [
                                {'CidrIp': '0.0.0.0/0'}
                            ]
                        }
                    ]
                }
            ]
        }
        results = {'total': 0, 'issues': []}
        
        scanner._scan_security_groups(mock_client, 'us-east-1', results)
        
        assert len(results['issues']) == 1
        assert results['issues'][0].service == 'ec2'
        assert results['issues'][0].severity == Severity.HIGH
        assert 'Open Security Group' in results['issues'][0].title
        assert 'tcp:22' in results['issues'][0].description
    
    def test_scan_security_groups_no_open_ports(self):
        """Test that security groups without open ports are not flagged."""
        scanner = EC2Scanner(MagicMock())
        mock_client = MagicMock()
        mock_client.describe_security_groups.return_value = {
            'SecurityGroups': [
                {
                    'GroupId': 'sg-12345678',
                    'GroupName': 'test-sg',
                    'IpPermissions': [
                        {
                            'IpProtocol': 'tcp',
                            'FromPort': 22,
                            'ToPort': 22,
                            'IpRanges': [
                                {'CidrIp': '192.168.1.0/24'}
                            ]
                        }
                    ]
                }
            ]
        }
        results = {'total': 0, 'issues': []}
        
        scanner._scan_security_groups(mock_client, 'us-east-1', results)
        
        assert len(results['issues']) == 0
    
    def test_scan_ebs_volumes_unencrypted(self):
        """Test detection of unencrypted EBS volumes."""
        scanner = EC2Scanner(MagicMock())
        mock_client = MagicMock()
        mock_client.describe_volumes.return_value = {
            'Volumes': [
                {
                    'VolumeId': 'vol-12345678',
                    'Encrypted': False
                }
            ]
        }
        results = {'total': 0, 'issues': []}
        
        scanner._scan_ebs_volumes(mock_client, 'us-east-1', results)
        
        assert len(results['issues']) == 1
        assert results['issues'][0].service == 'ec2'
        assert results['issues'][0].severity == Severity.MEDIUM
        assert 'Unencrypted EBS Volume' in results['issues'][0].title
    
    def test_scan_ebs_volumes_encrypted(self):
        """Test that encrypted EBS volumes are not flagged."""
        scanner = EC2Scanner(MagicMock())
        mock_client = MagicMock()
        mock_client.describe_volumes.return_value = {
            'Volumes': [
                {
                    'VolumeId': 'vol-12345678',
                    'Encrypted': True
                }
            ]
        }
        results = {'total': 0, 'issues': []}
        
        scanner._scan_ebs_volumes(mock_client, 'us-east-1', results)
        
        assert len(results['issues']) == 0
    
    def test_scan_instances_stopped(self):
        """Test detection of stopped EC2 instances."""
        scanner = EC2Scanner(MagicMock())
        mock_client = MagicMock()
        mock_client.describe_instances.return_value = {
            'Reservations': [
                {
                    'Instances': [
                        {
                            'InstanceId': 'i-12345678',
                            'State': {'Name': 'stopped'}
                        }
                    ]
                }
            ]
        }
        results = {'total': 0, 'issues': []}
        
        scanner._scan_instances(mock_client, 'us-east-1', results)
        
        assert len(results['issues']) == 1
        assert results['issues'][0].service == 'ec2'
        assert results['issues'][0].severity == Severity.MEDIUM
        assert 'Stopped EC2 Instance' in results['issues'][0].title
    
    def test_scan_instances_running(self):
        """Test that running instances are not flagged."""
        scanner = EC2Scanner(MagicMock())
        mock_client = MagicMock()
        mock_client.describe_instances.return_value = {
            'Reservations': [
                {
                    'Instances': [
                        {
                            'InstanceId': 'i-12345678',
                            'State': {'Name': 'running'}
                        }
                    ]
                }
            ]
        }
        results = {'total': 0, 'issues': []}
        
        scanner._scan_instances(mock_client, 'us-east-1', results)
        
        assert len(results['issues']) == 0

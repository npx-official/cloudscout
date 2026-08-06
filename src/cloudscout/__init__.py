"""CloudScout - AWS Security Auditing Tool."""

__version__ = "0.2.0"
__author__ = "NIGHT PULSE X"

from .main import main
from .scanners.s3 import S3Scanner
from .scanners.iam import IAMScanner
from .scanners.ec2 import EC2Scanner
from .reporters.html import HTMLReporter
from .reporters.json import JSONReporter

__all__ = [
    "main",
    "S3Scanner",
    "IAMScanner",
    "EC2Scanner",
    "HTMLReporter",
    "JSONReporter",
]

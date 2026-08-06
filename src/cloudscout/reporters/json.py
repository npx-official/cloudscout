"""JSON report generator."""

import json
from typing import Dict, Any
from datetime import datetime
from pathlib import Path

class JSONReporter:
    """Generate JSON reports."""
    
    def __init__(self, results: Dict[str, Any]):
        self.results = results
    
    def generate(self, filename: str):
        """Generate JSON report."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'version': '0.2.0',
            'scans': {}
        }
        
        for service, data in self.results.items():
            report['scans'][service] = {
                'total': data.get('total', 0),
                'issues': [
                    {
                        'title': issue.title,
                        'severity': issue.severity.value,
                        'description': issue.description,
                        'resource': issue.resource_name
                    }
                    for issue in data.get('issues', [])
                ]
            }
        
        Path(filename).write_text(json.dumps(report, indent=2))

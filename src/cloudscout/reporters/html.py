"""HTML report generator."""

from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path

from ..models import Issue, Severity

class HTMLReporter:
    """Generate HTML reports."""
    
    def __init__(self, results: Dict[str, Any]):
        self.results = results
    
    def generate(self, filename: str):
        """Generate HTML report."""
        total_issues = sum(len(r.get('issues', [])) for r in self.results.values())
        total_resources = sum(r.get('total', 0) for r in self.results.values())
        
        # Count issues by severity
        severity_counts = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0,
            'info': 0
        }
        for service, data in self.results.items():
            for issue in data.get('issues', []):
                if issue.severity.value in severity_counts:
                    severity_counts[issue.severity.value] += 1
        
        html = self._generate_html_header()
        html += self._generate_summary(total_issues, total_resources, severity_counts)
        html += self._generate_issues_table()
        html += self._generate_region_details()
        html += self._generate_footer()
        
        Path(filename).write_text(html)
    
    def _generate_html_header(self) -> str:
        """Generate HTML header with NPX branding."""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CloudScout Security Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: #0a0a0f;
            color: #e0e5f0;
            padding: 2rem;
            line-height: 1.6;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        
        /* Header with NPX branding */
        .header {{
            text-align: center;
            padding: 2rem 0;
            border-bottom: 2px solid rgba(111, 255, 224, 0.1);
            margin-bottom: 2rem;
        }}
        .header .npx-text {{
            font-size: 1.2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #6fffe0, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 4px;
        }}
        .header .npx-text .star {{
            color: #6fffe0;
            -webkit-text-fill-color: #6fffe0;
        }}
        .header h1 {{
            font-size: 2.8rem;
            font-weight: 800;
            background: linear-gradient(135deg, #6fffe0, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0.5rem 0;
        }}
        .header .subtitle {{
            color: rgba(255,255,255,0.3);
            font-size: 1rem;
            letter-spacing: 2px;
        }}
        .header .badge {{
            display: inline-block;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            background: rgba(111, 255, 224, 0.1);
            border: 1px solid rgba(111, 255, 224, 0.2);
            color: #6fffe0;
            margin-top: 0.5rem;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }}
        .stat-card {{
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(111, 255, 224, 0.06);
            border-radius: 1rem;
            padding: 1.5rem;
            text-align: center;
            transition: all 0.3s ease;
        }}
        .stat-card:hover {{
            border-color: #6fffe0;
            transform: translateY(-2px);
        }}
        .stat-card .number {{
            font-size: 2.5rem;
            font-weight: 700;
            color: #6fffe0;
        }}
        .stat-card .label {{
            color: rgba(255,255,255,0.4);
            font-size: 0.8rem;
            margin-top: 0.3rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .section-title {{
            font-size: 1.5rem;
            color: #6fffe0;
            margin: 2.5rem 0 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid rgba(111, 255, 224, 0.05);
        }}
        
        .issue-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            background: rgba(255,255,255,0.02);
            border-radius: 1rem;
            overflow: hidden;
        }}
        .issue-table th {{
            background: rgba(111, 255, 224, 0.05);
            color: #6fffe0;
            padding: 0.8rem 1.2rem;
            text-align: left;
            font-weight: 600;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .issue-table td {{
            padding: 0.8rem 1.2rem;
            border-bottom: 1px solid rgba(255,255,255,0.03);
        }}
        .issue-table tr:hover td {{
            background: rgba(111, 255, 224, 0.02);
        }}
        
        .badge {{
            display: inline-block;
            padding: 0.2rem 0.8rem;
            border-radius: 20px;
            font-size: 0.65rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .badge-critical {{ background: rgba(255,0,0,0.15); color: #ff0000; }}
        .badge-high {{ background: rgba(255,107,107,0.15); color: #ff6b6b; }}
        .badge-medium {{ background: rgba(255,217,61,0.15); color: #ffd93d; }}
        .badge-low {{ background: rgba(107,203,119,0.15); color: #6bcb77; }}
        .badge-info {{ background: rgba(111,255,224,0.1); color: #6fffe0; }}
        
        .no-issues {{
            text-align: center;
            padding: 3rem;
            color: rgba(255,255,255,0.3);
        }}
        .no-issues .icon {{
            font-size: 3rem;
            display: block;
            margin-bottom: 1rem;
        }}
        
        .footer {{
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid rgba(111, 255, 224, 0.06);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }}
        .footer .brand {{
            color: rgba(255,255,255,0.2);
            font-size: 0.8rem;
        }}
        .footer .brand a {{
            color: #6fffe0;
            text-decoration: none;
        }}
        .footer .brand a:hover {{
            text-decoration: underline;
        }}
        .footer .social {{
            display: flex;
            gap: 1.5rem;
        }}
        .footer .social a {{
            color: rgba(255,255,255,0.2);
            text-decoration: none;
            font-size: 0.8rem;
            transition: 0.3s;
        }}
        .footer .social a:hover {{
            color: #6fffe0;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 2rem; }}
            .summary {{ grid-template-columns: 1fr 1fr; }}
            .footer {{ flex-direction: column; text-align: center; }}
        }}
        @media (max-width: 480px) {{
            .summary {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="npx-text">✦ NIGHT PULSE X ✦</div>
            <h1>☁️ CloudScout</h1>
            <div class="subtitle">AWS Security Audit Report</div>
            <div class="badge">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
"""
    
    def _generate_summary(self, total_issues: int, total_resources: int, severity_counts: Dict[str, int]) -> str:
        """Generate summary statistics."""
        html = """
        <div class="summary">
            <div class="stat-card">
                <div class="number">{len(self.results)}</div>
                <div class="label">Services Scanned</div>
            </div>
            <div class="stat-card">
                <div class="number">{total_resources}</div>
                <div class="label">Resources Scanned</div>
            </div>
            <div class="stat-card">
                <div class="number" style="color: {'#6bcb77' if total_issues == 0 else '#ff6b6b'}">{total_issues}</div>
                <div class="label">Issues Found</div>
            </div>
        </div>
        
        <div class="summary">
            <div class="stat-card">
                <div class="number" style="color: #ff0000">{severity_counts['critical']}</div>
                <div class="label">Critical</div>
            </div>
            <div class="stat-card">
                <div class="number" style="color: #ff6b6b">{severity_counts['high']}</div>
                <div class="label">High</div>
            </div>
            <div class="stat-card">
                <div class="number" style="color: #ffd93d">{severity_counts['medium']}</div>
                <div class="label">Medium</div>
            </div>
            <div class="stat-card">
                <div class="number" style="color: #6bcb77">{severity_counts['low']}</div>
                <div class="label">Low</div>
            </div>
            <div class="stat-card">
                <div class="number" style="color: #6fffe0">{severity_counts['info']}</div>
                <div class="label">Info</div>
            </div>
        </div>
"""
        return html
    
    def _generate_issues_table(self) -> str:
        """Generate detailed issues table."""
        all_issues = []
        for service, data in self.results.items():
            for issue in data.get('issues', []):
                all_issues.append({
                    'service': service.upper(),
                    'title': issue.title,
                    'severity': issue.severity.value,
                    'description': issue.description,
                    'recommendation': issue.recommendation
                })
        
        if not all_issues:
            return """
            <h2 class="section-title">📋 Detailed Findings</h2>
            <div class="no-issues">
                <span class="icon">✅</span>
                No security issues found!<br>
                <span style="font-size: 0.9rem; color: rgba(255,255,255,0.2);">Your AWS environment is secure.</span>
            </div>
            """
        
        html = """
        <h2 class="section-title">📋 Detailed Findings</h2>
        <table class="issue-table"><thead><tr>
            <th>Service</th>
            <th>Issue</th>
            <th>Recommendation</th>
            <th>Severity</th>
        </tr></thead><tbody>
"""
        for issue in all_issues:
            html += f"""
            <tr>
                <td><strong>{issue['service']}</strong></td>
                <td>{issue['title']}</td>
                <td style="color: rgba(255,255,255,0.5); font-size: 0.9rem;">{issue['recommendation']}</td>
                <td><span class="badge badge-{issue['severity']}">{issue['severity'].upper()}</span></td>
            </tr>"""
        html += "</tbody></table>"
        return html
    
    def _generate_region_details(self) -> str:
        """Generate region-specific details."""
        html = """
        <h2 class="section-title">🌍 Region Details</h2>
        <table class="issue-table"><thead><tr>
            <th>Service</th>
            <th>Region</th>
            <th>Resources</th>
            <th>Issues</th>
        </tr></thead><tbody>
"""
        for service, data in self.results.items():
            # Get region from issues metadata if available
            regions_found = set()
            for issue in data.get('issues', []):
                if 'region' in issue.metadata:
                    regions_found.add(issue.metadata['region'])
            
            if not regions_found:
                # Fallback to 'N/A'
                html += f"""
            <tr>
                <td><strong>{service.upper()}</strong></td>
                <td>N/A</td>
                <td>{data.get('total', 0)}</td>
                <td>{len(data.get('issues', []))}</td>
            </tr>"""
            else:
                for region in sorted(regions_found):
                    html += f"""
            <tr>
                <td><strong>{service.upper()}</strong></td>
                <td>{region}</td>
                <td>{data.get('total', 0)}</td>
                <td>{len(data.get('issues', []))}</td>
            </tr>"""
        html += "</tbody></table>"
        return html
    
    def _generate_footer(self) -> str:
        """Generate footer with NPX branding and social links."""
        return f"""
        <div class="footer">
            <div class="brand">
                🌙 <a href="https://github.com/npx-official">NIGHT PULSE X</a> · 
                <a href="https://github.com/npx-official/cloudscout">CloudScout v0.2.0</a>
            </div>
            <div class="social">
                <a href="https://github.com/npx-official">🐙 GitHub</a>
                <a href="https://app.hackthebox.com/users/2207141">🎯 HTB</a>
                <a href="https://tryhackme.com/p/npx.off">🛡️ THM</a>
            </div>
        </div>
    </div>
</body>
</html>
"""

#!/usr/bin/env python3
"""Main entry point for CloudScout."""

import sys
import click
from colorama import init, Fore, Style

from .scanners.s3 import S3Scanner
from .scanners.iam import IAMScanner
from .scanners.ec2 import EC2Scanner
from .reporters.html import HTMLReporter
from .reporters.json import JSONReporter
from .utils.aws import AWSUtils

init(autoreset=True)

# ASCII Art Logo
LOGO = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ███╗   ██╗██████╗ ██╗  ██╗    ██████╗██╗   ██╗██╗       ║
║   ████╗  ██║██╔══██╗╚██╗██╔╝   ██╔════╝██║   ██║██║       ║
║   ██╔██╗ ██║██████╔╝ ╚███╔╝    ██║     ██║   ██║██║       ║
║   ██║╚██╗██║██╔═══╝  ██╔██╗    ██║     ██║   ██║██║       ║
║   ██║ ╚████║██║     ██╔╝ ██╗   ╚██████╗╚██████╔╝███████╗  ║
║   ╚═╝  ╚═══╝╚═╝     ╚═╝  ╚═╝    ╚═════╝ ╚═════╝ ╚══════╝  ║
║                                                              ║
║         ☁️  CloudScout - AWS Security Audit Tool            ║
║                  by NIGHT PULSE X                           ║
║              https://github.com/npx-official                ║
╚══════════════════════════════════════════════════════════════╝
"""

BETA_WARNING = f"""
{Fore.YELLOW}{Style.BRIGHT}⚠️  Status: Beta / Under Development
{Fore.YELLOW}🚧  This tool is currently in active development and testing phase.
{Fore.YELLOW}🐛  Please report issues at: https://github.com/npx-official/cloudscout/issues
{Style.RESET_ALL}
"""

def print_help_with_logo(ctx, param, value):
    """Print help with logo."""
    if value and not ctx.resilient_parsing:
        no_logo = ctx.params.get('no_logo', False)
        if not no_logo:
            click.echo(Fore.CYAN + LOGO)
            click.echo()
        click.echo(ctx.get_help())
        ctx.exit()

@click.command()
@click.option('--profile', default='default', help='AWS profile name')
@click.option('--services', default='all', help='Services: s3,iam,ec2')
@click.option('--output', '-o', default='report', help='Output file name')
@click.option('--format', '-f', default='html', type=click.Choice(['html', 'json']), help='Report format')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--no-logo', is_flag=True, help='Hide logo')
@click.option('--help', '-h', is_flag=True, is_eager=True, expose_value=False, callback=print_help_with_logo, help='Show this message and exit.')
def main(profile, services, output, format, verbose, no_logo):
    """CloudScout - AWS Security Auditing Tool."""
    
    if not no_logo:
        print(Fore.CYAN + LOGO)
    
    # عرض تحذير BETA
    print(BETA_WARNING)
    
    print(f"{Fore.CYAN}{Style.BRIGHT}📡  CloudScout v0.2.0")
    print(f"{Fore.CYAN}{'═' * 55}{Style.RESET_ALL}\n")
    
    try:
        # AWS setup
        aws = AWSUtils(profile)
        account_id = aws.get_account_id()
        region = aws.get_region()
        
        print(f"{Fore.GREEN}✅ Account: {account_id}")
        print(f"{Fore.GREEN}✅ Region: {region}")
        print(f"{Fore.GREEN}✅ Profile: {profile}")
        print()
        
        # Parse services
        if services == 'all':
            services_list = ['s3', 'iam', 'ec2']
        else:
            services_list = [s.strip() for s in services.split(',')]
        
        results = {}
        
        # Run scanners
        for service in services_list:
            if service == 's3':
                scanner = S3Scanner(aws)
            elif service == 'iam':
                scanner = IAMScanner(aws)
            elif service == 'ec2':
                scanner = EC2Scanner(aws)
            else:
                continue
            
            print(f"{Fore.CYAN}▶ Scanning {service.upper()}...")
            results[service] = scanner.scan()
            print(f"{Fore.GREEN}  ✓ {results[service]['total']} resources scanned")
            print(f"{Fore.YELLOW}  ⚠ {len(results[service].get('issues', []))} issues found")
            print()
        
        # Generate report
        if format == 'html':
            reporter = HTMLReporter(results)
            output_file = f"{output}.html"
        else:
            reporter = JSONReporter(results)
            output_file = f"{output}.json"
        
        reporter.generate(output_file)
        
        print(f"{Fore.GREEN}✅ Scan complete! Report saved to: {output_file}")
        print(f"{Fore.CYAN}📊 Open with: firefox {output_file}")
        print()
        print(f"{Fore.MAGENTA}🔗 https://github.com/npx-official/cloudscout")
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

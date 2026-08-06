<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=28&duration=3000&pause=1000&color=6FFFE0&center=true&vCenter=true&width=600&lines=☁️+CloudScout;AWS+Security+Auditing+Tool;Find+Misconfigurations+Before+Attackers" alt="Typing SVG" />
</p>

<p align="center">
  <a href="https://github.com/npx-official/cloudscout/stargazers">
    <img src="https://img.shields.io/github/stars/npx-official/cloudscout?style=for-the-badge&logo=github&color=6fffe0&logoColor=white" alt="Stars" />
  </a>
  <a href="https://github.com/npx-official/cloudscout/network/members">
    <img src="https://img.shields.io/github/forks/npx-official/cloudscout?style=for-the-badge&logo=github&color=a78bfa&logoColor=white" alt="Forks" />
  </a>
  <a href="https://github.com/npx-official/cloudscout/issues">
    <img src="https://img.shields.io/github/issues/npx-official/cloudscout?style=for-the-badge&logo=github&color=ff6b6b&logoColor=white" alt="Issues" />
  </a>
  <a href="https://github.com/npx-official/cloudscout/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/npx-official/cloudscout?style=for-the-badge&logo=github&color=6bcb77&logoColor=white" alt="License" />
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.8+-6fffe0?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  </a>
  <a href="https://aws.amazon.com/">
    <img src="https://img.shields.io/badge/AWS-Security-a78bfa?style=for-the-badge&logo=amazon-aws&logoColor=white" alt="AWS" />
  </a>
</p>

<br>

<p align="center">
  <img src="https://github.com/npx-official/cloudscout/raw/main/docs/assets/demo.gif" alt="CloudScout Demo" width="800" style="border-radius: 16px; border: 1px solid rgba(111, 255, 224, 0.1);" />
</p>

<br>

---

## ⚡ **Quick Start**

```bash
# Clone the repository
git clone https://github.com/npx-official/cloudscout.git
cd cloudscout

# Install dependencies
pip install -r requirements.txt

# Run a scan
./cloudscout --profile default --services all
```

---

## 🎯 **What CloudScout Does**

| Service | Checks | Risk Level |
|---------|--------|------------|
| <img src="https://img.shields.io/badge/-S3-6fffe0?style=flat-square&logo=amazon-s3&logoColor=white" alt="S3" /> | Public buckets, open ACLs, missing encryption, no logging | <img src="https://img.shields.io/badge/-High-ff6b6b?style=flat-square" alt="High" /> / <img src="https://img.shields.io/badge/-Medium-ffd93d?style=flat-square" alt="Medium" /> |
| <img src="https://img.shields.io/badge/-IAM-a78bfa?style=flat-square&logo=aws-iam&logoColor=white" alt="IAM" /> | Missing MFA, old access keys, excessive permissions | <img src="https://img.shields.io/badge/-High-ff6b6b?style=flat-square" alt="High" /> / <img src="https://img.shields.io/badge/-Medium-ffd93d?style=flat-square" alt="Medium" /> |
| <img src="https://img.shields.io/badge/-EC2-6bcb77?style=flat-square&logo=amazon-ec2&logoColor=white" alt="EC2" /> | Open security groups (0.0.0.0/0), exposed ports | <img src="https://img.shields.io/badge/-High-ff6b6b?style=flat-square" alt="High" /> |

---

## 📊 **Reports**

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=18&duration=3000&pause=1000&color=6FFFE0&center=true&vCenter=true&width=400&lines=📄+HTML+Reports;📋+JSON+Reports" alt="Reports" />
</p>

```bash
# HTML Report
./cloudscout --profile default --services all --output report --format html

# JSON Report
./cloudscout --profile default --services all --output report --format json
```

---

## 🏗️ **Architecture**

```bash
cloudscout/
├── src/cloudscout/
│   ├── main.py          # Entry point
│   ├── models.py         # Data models
│   ├── scanners/         # AWS service scanners
│   │   ├── s3.py         # S3 bucket scanner
│   │   ├── iam.py        # IAM user scanner
│   │   └── ec2.py        # EC2 security group scanner
│   ├── reporters/        # Report generators
│   │   ├── html.py       # HTML report
│   │   └── json.py       # JSON report
│   └── utils/
│       └── aws.py        # AWS utilities
├── tests/                # Test suite
├── docs/                 # Documentation
└── data/                 # Data files
```

---

## 🚀 **Usage Examples**

| Command | Description |
|---------|-------------|
| `./cloudscout --profile default --services all` | Scan all services |
| `./cloudscout --profile default --services s3,iam` | Scan specific services |
| `./cloudscout --profile default --services all --output audit --format html` | Generate HTML report |
| `./cloudscout --profile default --services all --output audit --format json` | Generate JSON report |
| `./cloudscout --profile default --services all --verbose` | Verbose output |
| `./cloudscout --profile default --services all --no-logo` | Hide logo |

---

## 🛠️ **Requirements**

- <img src="https://img.shields.io/badge/-Python_3.8+-6fffe0?style=flat-square&logo=python&logoColor=white" alt="Python" />
- <img src="https://img.shields.io/badge/-AWS_CLI-a78bfa?style=flat-square&logo=amazon-aws&logoColor=white" alt="AWS CLI" />
- <img src="https://img.shields.io/badge/-IAM_Permissions-6bcb77?style=flat-square" alt="IAM Permissions" />

### Required IAM Permissions:
- `s3:ListAllMyBuckets`
- `s3:GetBucketAcl`
- `s3:GetBucketPolicy`
- `iam:ListUsers`
- `iam:ListAccessKeys`
- `ec2:DescribeSecurityGroups`

---

## 📝 **Sample Output**

```bash
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

📡  CloudScout v0.2.0
══════════════════════════════════════════════════

✅ Account: 123456789012
✅ Region: us-east-1
✅ Profile: default

▶ Scanning S3...
  📦 Found 15 buckets
  ✓ 15 resources scanned
  ⚠ 3 issues found

▶ Scanning IAM...
  👤 Found 8 users
  ✓ 8 resources scanned
  ⚠ 2 issues found

▶ Scanning EC2...
  🔒 Found 4 security groups
  ✓ 4 resources scanned
  ⚠ 1 issues found

✅ Scan complete! Report saved to: report.html
📊 Open with: firefox report.html

🔗 https://github.com/npx-official/cloudscout
```

---

## 🤝 **Contributing**

Contributions are welcome!

```bash
# Setup development environment
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Format code
black src/ tests/
```

---

## 📄 **License**

MIT License - see [LICENSE](LICENSE) file for details.

---

<br>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=20&duration=3000&pause=1000&color=6FFFE0&center=true&vCenter=true&width=600&lines=⭐+Star+this+repo+if+you+find+it+useful;🛡️+Secure+your+AWS+environment;🚀+Made+with+❤️+by+NIGHT+PULSE+X" alt="Footer" />
</p>

<p align="center">
  <a href="https://github.com/npx-official">
    <img src="https://img.shields.io/badge/GitHub-npx--official-181717?style=for-the-badge&logo=github&logoColor=6fffe0" alt="GitHub" />
  </a>
  <a href="https://www.linkedin.com/in/night-pulse-x-337a89275">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
</p>

<br>

<p align="center">
  <img src="https://raw.githubusercontent.com/npx-official/npx-official/main/assets/images/cyber-grid.png" width="800" style="opacity: 0.1;" />
</p>

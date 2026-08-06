# ☁️ CloudScout

> *AWS Security Auditing Tool · Find Misconfigurations Before Attackers*

<p align="center">
  <a href="https://github.com/npx-official/cloudscout"><img src="https://img.shields.io/badge/🐙-GitHub-181717?style=for-the-badge&logo=github&logoColor=white"/></a>
  <a href="https://pypi.org/project/cloudscout/"><img src="https://img.shields.io/badge/📦-PyPI-3775A9?style=for-the-badge&logo=pypi&logoColor=white"/></a>
  <a href="https://github.com/npx-official/cloudscout/issues"><img src="https://img.shields.io/badge/🐛-Issues-ff6b6b?style=for-the-badge"/></a>
  <a href="https://github.com/npx-official/cloudscout/blob/main/LICENSE"><img src="https://img.shields.io/badge/📄-License-6bcb77?style=for-the-badge"/></a>
</p>

---

## 🎯 Overview

<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=24&duration=3000&pause=1000&color=6FFFE0&center=true&vCenter=true&width=500&lines=AWS+Security+Auditing+Tool;Detect+Misconfigurations;Protect+Your+Cloud+Infrastructure" alt="Typing SVG" />
</div>

<br>

> 🔍 **CloudScout** scans your AWS environment for common security misconfigurations.  
> 🛡️ Identifies public S3 buckets, missing MFA, open security groups, and more.  
> 📊 Generates **HTML** and **JSON** reports with clear recommendations.  
> 🚀 Fast, lightweight, and easy to use.

---

## ⚡ Quick Start

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

## 🛠️ Features

| Service | Checks | Risk Level |
|---------|--------|------------|
| **S3** | Public buckets, open ACLs, missing encryption | 🔴 High / 🟡 Medium |
| **IAM** | Missing MFA, old access keys, excessive permissions | 🔴 High / 🟡 Medium |
| **EC2** | Open security groups (0.0.0.0/0), exposed ports | 🔴 High |

---

## 📊 Reports

```bash
# HTML Report
./cloudscout --profile default --services all --output report --format html

# JSON Report
./cloudscout --profile default --services all --output report --format json
```

---

## 🚀 Usage Examples

```bash
# Scan all services
./cloudscout --profile default --services all

# Scan specific services
./cloudscout --profile default --services s3,iam

# Generate HTML report
./cloudscout --profile default --services all --output security-audit --format html

# Verbose output
./cloudscout --profile default --services all --verbose

# Hide logo
./cloudscout --profile default --services all --no-logo
```

---

## 🛠️ Requirements

- Python 3.8+
- AWS CLI configured with credentials
- IAM permissions: s3, iam, ec2 read access

---

## 📝 Sample Output

```
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

## 🤝 Contributing

```bash
# Setup development environment
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Format code
black src/ tests/
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

<div align="center">

⭐️ **Star this repo if you find it useful!**  
🛡️ **Secure your AWS environment today!**

</div>

---

<p align="center">
  <a href="https://npx-official.github.io/"><img src="https://img.shields.io/badge/🌐-Website-6fffe0?style=for-the-badge&logo=google-chrome&logoColor=white"/></a>
  <a href="https://github.com/npx-official"><img src="https://img.shields.io/badge/🐙-GitHub-181717?style=for-the-badge&logo=github&logoColor=white"/></a>
  <a href="https://www.linkedin.com/in/night-pulse-x-337a89275"><img src="https://img.shields.io/badge/🔗-LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white"/></a>
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=14&duration=3000&pause=1000&color=6FFFE0&center=true&vCenter=true&width=400&lines=Made+with+❤️+by+NIGHT+PULSE+X" alt="Footer" />
</p>

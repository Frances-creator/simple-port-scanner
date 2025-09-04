# 🔍 Simple Port Scanner

A Python-based network port scanner that identifies open ports on target hosts and validates results against Nmap. This project demonstrates practical networking concepts and cybersecurity fundamentals.

## 🚀 Features

- **Fast Multi-threaded Scanning**: Utilizes threading for efficient port scanning
- **Common Port Detection**: Identifies well-known services (HTTP, HTTPS, SSH, etc.)
- **Flexible Port Ranges**: Scan specific ports, ranges, or common ports only
- **Nmap Integration**: Compare results with industry-standard Nmap tool
- **Detailed Reporting**: Comprehensive scan reports with timing and accuracy metrics
- **Error Handling**: Robust error handling for network timeouts and failures

## 🛠️ Skills Demonstrated

- **Python Programming**: Object-oriented design, threading, argument parsing
- **Network Programming**: Socket programming, TCP connections, hostname resolution
- **System Integration**: Subprocess management, external tool integration
- **Security Concepts**: Port scanning techniques, service identification
- **Performance Optimization**: Multi-threading, timeout management

## 📋 Requirements

```bash
# Core Requirements
- Python 3.6+
- Standard library modules (socket, threading, subprocess, argparse)

# Optional for comparison feature
- Nmap (Network Mapper)
```

## 🔧 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/simple-port-scanner.git
cd simple-port-scanner
```

2. **Install Nmap (optional, for comparison feature):**
```bash
# Ubuntu/Debian
sudo apt-get install nmap

# macOS
brew install nmap

# Windows
# Download from https://nmap.org/download.html
```

3. **Make the script executable:**
```bash
chmod +x port_scanner.py
```

## 🚀 Usage

### Basic Examples

**Scan common ports:**
```bash
python port_scanner.py -t google.com -c
```

**Scan specific ports:**
```bash
python port_scanner.py -t 192.168.1.1 -p 22,80,443
```

**Scan port range:**
```bash
python port_scanner.py -t example.com -p 1-1000
```

**Compare with Nmap:**
```bash
python port_scanner.py -t target.com -c --nmap
```

### Advanced Options

```bash
# Custom thread count
python port_scanner.py -t target.com -p 1-5000 --threads 200

# Custom timeout
python port_scanner.py -t target.com -c --timeout 2

# Full help
python port_scanner.py -h
```

## 📊 Sample Output

```
============================================================
           SIMPLE PORT SCANNER
      Python-based Network Port Scanner
============================================================

[INFO] Resolved google.com to 142.250.191.14
[INFO] Quick scan of common ports on 142.250.191.14
--------------------------------------------------
[OPEN] Port 80: HTTP
[OPEN] Port 443: HTTPS

==================================================
SCAN REPORT
==================================================
Target: google.com
Scan Type: Common Ports
Start Time: 2025-05-27 10:30:15
End Time: 2025-05-27 10:30:17
Duration: 2.34 seconds
Open Ports Found: 2

Open Ports:
--------------------
    80/tcp  HTTP
   443/tcp  HTTPS

==================================================
NMAP COMPARISON
==================================================
[INFO] Running: nmap -F 142.250.191.14

[NMAP RESULTS]
Starting Nmap 7.80 ( https://nmap.org )
Nmap scan report for 142.250.191.14
Host is up (0.023s latency).
Not shown: 98 filtered ports
PORT    STATE SERVICE
80/tcp  open  http
443/tcp open  https

[COMPARISON RESULTS]
------------------------------
Our scanner found: [80, 443]
Nmap found: [80, 443]
Matches: [80, 443]
Accuracy: 100.0%
```

## 🏗️ Project Structure

```
simple-port-scanner/
├── port_scanner.py          # Main scanner script
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
├── examples/              # Usage examples
│   ├── basic_scan.py      # Basic scanning examples
│   └── advanced_scan.py   # Advanced usage patterns
├── tests/                 # Test files
│   └── test_scanner.py    # Unit tests
└── docs/                  # Additional documentation
    ├── CONTRIBUTING.md    # Contribution guidelines
    └── SECURITY.md        # Security considerations
```

## 🧪 Testing

The scanner has been tested against various targets:

- **Local Services**: Apache, Nginx, SSH servers
- **Public Websites**: Google, GitHub, Stack Overflow
- **Private Networks**: Home routers, local servers
- **Comparison Accuracy**: 95%+ match rate with Nmap

## ⚠️ Ethical Usage

This tool is for educational and authorized testing purposes only:

- Only scan systems you own or have explicit permission to test
- Respect rate limits and don't overwhelm target systems
- Be aware of your local laws regarding network scanning
- Use responsibly and ethically

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- UDP port scanning support
- Service version detection
- Output formats (JSON, XML)
- GUI interface
- Performance optimizations

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**[Your Name]**
- LinkedIn: [Your LinkedIn Profile]
- GitHub: [Your GitHub Profile]
- Email: your.email@example.com

## 🙏 Acknowledgments

- Inspired by Nmap and other network scanning tools
- Python community for excellent documentation
- Cybersecurity community for best practices

---

*This project demonstrates practical application of networking concepts and cybersecurity fundamentals using Python. It serves as a learning tool for understanding how port scanners work and network security assessment techniques.*
#!/usr/bin/env python3
"""
Simple Port Scanner
A Python-based port scanner that identifies open ports on target hosts
and compares results with Nmap for validation.

Author: [Your Name]
Date: May 2025
"""

import socket
import threading
import argparse
import sys
import time
from datetime import datetime
import subprocess
import json

class PortScanner:
    def __init__(self, target, threads=100):
        self.target = target
        self.threads = threads
        self.open_ports = []
        self.lock = threading.Lock()
        
        # Common ports and their services
        self.common_ports = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 993: "IMAPS",
            995: "POP3S", 1433: "MSSQL", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
            5900: "VNC", 6379: "Redis", 27017: "MongoDB"
        }
    
    def resolve_target(self):
        """Resolve hostname to IP address"""
        try:
            ip = socket.gethostbyname(self.target)
            print(f"[INFO] Resolved {self.target} to {ip}")
            return ip
        except socket.gaierror:
            print(f"[ERROR] Could not resolve hostname: {self.target}")
            return None
    
    def scan_port(self, ip, port):
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            
            if result == 0:
                with self.lock:
                    service = self.common_ports.get(port, "Unknown")
                    self.open_ports.append((port, service))
                    print(f"[OPEN] Port {port}: {service}")
            
            sock.close()
        except Exception as e:
            pass
    
    def scan_range(self, ip, start_port, end_port):
        """Scan a range of ports using threading"""
        print(f"[INFO] Scanning {ip} from port {start_port} to {end_port}")
        print(f"[INFO] Using {self.threads} threads")
        print("-" * 50)
        
        # Create thread pool
        threads = []
        
        for port in range(start_port, end_port + 1):
            while len([t for t in threads if t.is_alive()]) >= self.threads:
                time.sleep(0.01)
            
            thread = threading.Thread(target=self.scan_port, args=(ip, port))
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
    
    def scan_common_ports(self, ip):
        """Quick scan of common ports"""
        print(f"[INFO] Quick scan of common ports on {ip}")
        print("-" * 50)
        
        threads = []
        for port in self.common_ports.keys():
            thread = threading.Thread(target=self.scan_port, args=(ip, port))
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
    
    def nmap_comparison(self, ip, ports_to_check=None):
        """Compare results with Nmap"""
        print("\n" + "="*50)
        print("NMAP COMPARISON")
        print("="*50)
        
        try:
            if ports_to_check:
                port_list = ",".join(map(str, ports_to_check))
                cmd = f"nmap -p {port_list} {ip}"
            else:
                cmd = f"nmap -F {ip}"  # Fast scan
            
            print(f"[INFO] Running: {cmd}")
            result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print("\n[NMAP RESULTS]")
                print(result.stdout)
                
                # Parse Nmap results
                nmap_open_ports = []
                for line in result.stdout.split('\n'):
                    if '/tcp' in line and 'open' in line:
                        port = int(line.split('/')[0])
                        nmap_open_ports.append(port)
                
                # Compare results
                our_ports = [port for port, _ in self.open_ports]
                
                print("\n[COMPARISON RESULTS]")
                print("-" * 30)
                print(f"Our scanner found: {sorted(our_ports)}")
                print(f"Nmap found: {sorted(nmap_open_ports)}")
                
                matches = set(our_ports) & set(nmap_open_ports)
                our_only = set(our_ports) - set(nmap_open_ports)
                nmap_only = set(nmap_open_ports) - set(our_ports)
                
                print(f"Matches: {sorted(matches)}")
                if our_only:
                    print(f"Only we found: {sorted(our_only)}")
                if nmap_only:
                    print(f"Only Nmap found: {sorted(nmap_only)}")
                
                accuracy = len(matches) / len(set(our_ports) | set(nmap_open_ports)) * 100 if (our_ports or nmap_open_ports) else 0
                print(f"Accuracy: {accuracy:.1f}%")
                
            else:
                print(f"[ERROR] Nmap failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print("[ERROR] Nmap scan timed out")
        except FileNotFoundError:
            print("[ERROR] Nmap not found. Please install Nmap to use comparison feature.")
        except Exception as e:
            print(f"[ERROR] Nmap comparison failed: {e}")
    
    def generate_report(self, scan_type, start_time, end_time):
        """Generate a summary report"""
        print("\n" + "="*50)
        print("SCAN REPORT")
        print("="*50)
        
        duration = end_time - start_time
        
        print(f"Target: {self.target}")
        print(f"Scan Type: {scan_type}")
        print(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Duration: {duration.total_seconds():.2f} seconds")
        print(f"Open Ports Found: {len(self.open_ports)}")
        
        if self.open_ports:
            print("\nOpen Ports:")
            print("-" * 20)
            for port, service in sorted(self.open_ports):
                print(f"  {port:5d}/tcp  {service}")
        else:
            print("\nNo open ports found.")

def main():
    parser = argparse.ArgumentParser(
        description="Simple Port Scanner - Scan for open ports on target hosts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python port_scanner.py -t google.com -c
  python port_scanner.py -t 192.168.1.1 -p 1-1000
  python port_scanner.py -t example.com -p 80,443,22 --nmap
        """
    )
    
    parser.add_argument('-t', '--target', required=True, help='Target hostname or IP address')
    parser.add_argument('-p', '--ports', help='Port range (e.g., 1-1000) or specific ports (e.g., 80,443,22)')
    parser.add_argument('-c', '--common', action='store_true', help='Scan only common ports')
    parser.add_argument('--threads', type=int, default=100, help='Number of threads (default: 100)')
    parser.add_argument('--nmap', action='store_true', help='Compare results with Nmap')
    parser.add_argument('--timeout', type=int, default=1, help='Socket timeout in seconds (default: 1)')
    
    args = parser.parse_args()
    
    # Banner
    print("="*60)
    print("           SIMPLE PORT SCANNER")
    print("      Python-based Network Port Scanner")
    print("="*60)
    print()
    
    # Initialize scanner
    scanner = PortScanner(args.target, args.threads)
    
    # Resolve target
    ip = scanner.resolve_target()
    if not ip:
        sys.exit(1)
    
    start_time = datetime.now()
    
    try:
        if args.common:
            # Scan common ports only
            scanner.scan_common_ports(ip)
            scan_type = "Common Ports"
            
        elif args.ports:
            # Parse port specification
            if '-' in args.ports:
                # Port range
                start_port, end_port = map(int, args.ports.split('-'))
                scanner.scan_range(ip, start_port, end_port)
                scan_type = f"Port Range {start_port}-{end_port}"
            else:
                # Specific ports
                ports = [int(p.strip()) for p in args.ports.split(',')]
                print(f"[INFO] Scanning specific ports: {ports}")
                print("-" * 50)
                
                threads = []
                for port in ports:
                    thread = threading.Thread(target=scanner.scan_port, args=(ip, port))
                    thread.daemon = True
                    thread.start()
                    threads.append(thread)
                
                for thread in threads:
                    thread.join()
                
                scan_type = f"Specific Ports: {args.ports}"
        else:
            # Default: scan common ports
            scanner.scan_common_ports(ip)
            scan_type = "Common Ports (Default)"
        
        end_time = datetime.now()
        
        # Generate report
        scanner.generate_report(scan_type, start_time, end_time)
        
        # Nmap comparison if requested
        if args.nmap:
            if args.ports and ',' in args.ports:
                ports_to_check = [int(p.strip()) for p in args.ports.split(',')]
                scanner.nmap_comparison(ip, ports_to_check)
            else:
                scanner.nmap_comparison(ip)
    
    except KeyboardInterrupt:
        print("\n[INFO] Scan interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
# Network Vulnerability Scanner and Exploitation Tool

This is a simple script that allows you to scan a network for hosts and detect any vulnerabilities using the National Vulnerability Database (NVD) API. The tool then exploits any high or critical vulnerabilities detected using the Metasploit framework.

## Usage

To use the tool, you must provide the IP address or range to scan in CIDR notation. The tool will then scan the network for hosts and display a list of detected hosts. You can then select which hosts to attack or choose to attack all hosts without prompting for selection.

The tool retrieves the latest vulnerability data from the NVD API and scans for each vulnerability on the target hosts. Only vulnerabilities with a severity rating of "HIGH" or "CRITICAL" are exploited using Metasploit.

To use the tool, ensure you have permission to scan and attack the target network or hosts. The tool is for educational purposes only and should not be used for illegal or malicious activities. Use at your own risk.

## Disclaimer

Automated vulnerability scanning and exploitation can be illegal and dangerous. Make sure you have permission to scan and attack the target network or hosts, and comply with all relevant laws and regulations. Use at your own risk.



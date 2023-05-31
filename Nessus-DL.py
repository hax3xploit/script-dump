# Author: Abdullah Khawaja
# Date: 30-5-2023
# Version: 2.0
# Tested on: Windows 11

import os
import requests
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

nessus_url = "https://your-nessus-server"
access_key = "your-access-key"
secret_key = "your-secret-key"

session = requests.session()

headers = {
    'X-ApiKeys': f'accessKey={access_key}; secretKey={secret_key}',
    'Content-Type': 'application/json'
}

# Get the list of available scans
scans_url = f'{nessus_url}/scans'
response = requests.get(scans_url, headers=headers, verify=False)

if response.status_code == 200:
    scans = response.json()['scans']
    scan_names_windows = ["Windows Servers", "System Team - SERVERS", 
                         "Infrastructure Server", "Infrastructure Servers-2",
                         "DMZ Infrastructure Server", "Windows Servers - HR",
                         "SCM Team - Server", "MDM Server"]  # Add more scan names here
    scan_names_linux =  ["Linux Servers"]
    scan_names_vis =    ["Virtual Infrastructure Servers"]
    scan_names_cisco =  ["Network Devices"]

    for scan in scans:
        scan_id = scan['id']
        scan_name = scan['name']

        if scan_name in scan_names_windows:
            folder_name = 'Windows'
        elif scan_name in scan_names_linux:
            folder_name = 'Linux'
        elif scan_name in scan_names_vis:
            folder_name = 'VIS(ESXI)'
        elif scan_name in scan_names_cisco:
            folder_name = 'Cisco'
        else:
            continue

        # Generate report in CSV format
        report_url = f'{nessus_url}/scans/{scan_id}/export'
        report_data = {
            'format': 'csv',
            'chapters': 'vuln_by_host',
        }
        report_response = requests.post(report_url, headers=headers, json=report_data, verify=False)

        if report_response.status_code == 200:
            download_token = report_response.json()['token']
            while True:
                # Check report status
                token_status_url = f'{nessus_url}/tokens/{download_token}/status'
                status_response = requests.get(token_status_url, headers=headers, verify=False)
                status_data = status_response.json()

                if status_data['status'] == 'ready':
                    break  # Report is ready for download

                time.sleep(5)  # Wait and check again

            # Download the report
            download_url = f'{nessus_url}/tokens/{download_token}/download'
            report_file = f'{scan_name}.csv'
            download_response = requests.get(download_url, headers=headers, verify=False)

            if download_response.status_code == 200:
                # Create folder if it doesn't exist
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)

                file_path = os.path.join(folder_name, report_file)

                with open(file_path, 'wb') as file:
                    file.write(download_response.content)
                print(f"[+] Report downloaded for scan '{scan_name}' and saved in '{folder_name}' folder.")
            else:
                print(f"[-] Failed to download report for scan '{scan_name}'")
        else:
            print(f"[-] Failed to generate report for scan '{scan_name}':",
                  report_response.json().get('error', 'Unknown error'))
else:
    print('[-] Failed to retrieve scans:', response.json().get('error', 'Unknown error'))

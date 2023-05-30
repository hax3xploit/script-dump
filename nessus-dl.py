import requests
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

nessus_url = "https://you-nessus-server"
username = "your-nessus-username"
password = "your-nessus-password"

session = requests.session()


login_url = f"{nessus_url}/session"
login_data = {
    "username": username,
    "password": password
}
response = session.post(login_url, json=login_data, verify=False)


if response.status_code == 200:
    session_token = response.json()['token']
    headers = {
        'X-Cookie': f'token={session_token}',
        'Content-Type': 'application/json'
    }

    # Get the list of available scans
    scans_url = f'{nessus_url}/scans'
    response = requests.get(scans_url, headers=headers, verify=False)

    if response.status_code == 200:
        scans = response.json()['scans']
        scan_names = ["Windows Servers", "Linux Scan", "Public Servers" ]  # Add more scan names here

        for scan in scans:
            if scan['name'] in scan_names:
                scan_id = scan['id']
                scan_name = scan['name']

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
                        with open(report_file, 'wb') as file:
                            file.write(download_response.content)
                        print(f"[+] Report downloaded for scan '{scan_name}'")
                    else:
                        print(f"[-] Failed to download report for scan '{scan_name}'")
                else:
                    print(f"[-] Failed to generate report for scan '{scan_name}':", report_response.json().get('error', 'Unknown error'))
    else:
        print('[-] Failed to retrieve scans:', response.json().get('error', 'Unknown error'))
else:
    print('[-] Login failed:', response.json().get('error', 'Unknown error'))

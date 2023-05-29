# Author: Abdullah Khawaja
# Date: 25-5-2023
# Version: 3.0
# Tested on: Windows 11

from shareplum import Site
from requests_ntlm import HttpNtlmAuth
import pandas as pd
import urllib3
import time
import logging

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Configure logging
logging.basicConfig(
    filename='log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

sharepoint_url = "https://your-share-point"
list_name = "your-List-Name"
username = "your-AD-user"
password = "your-AD-pass"

auth = HttpNtlmAuth(username, password)
site = Site(sharepoint_url, auth=auth, verify_ssl=False)
sp_list = site.List(list_name)

data = sp_list.GetListItems('All Items')

excel_file_path = "AntiMalwarefile.xlsx"
sheet_name = "2022-2023"
data_frame = pd.read_excel(excel_file_path, sheet_name=sheet_name)

existing_data = set()

for item in data:
    username = item.get("Username", "")
    status = item.get("Status", "")
    description = item.get("Description of Event", "")
    event_type = item.get("Event Type", "")
    affected_cis = item.get("Affected CI(s)", "")
    event_date = item.get("Event Reporting Date & Time", "")
    reported_by = item.get("Reported By(Name of the Person)", "")
    department = item.get("Department(of the Person Reporting)", "")
    affected_services = item.get("Affected Service(s)", "")
    affected_departments = item.get("Affected Department(s)", "")
    assigned_to = item.get("Assigned To", "")
    assignee_department = item.get("Assignee's Department", "")
    response_date = item.get("Event Response Date & Time", "")
    source_of_evidence = item.get("Source of Evidence", "")
    closure_date = item.get("Event Closure or Upgradation Date", "")
    initial_assessment = item.get("Initial Assessment", "")

    existing_data.add((
        status, description, username,
        event_type, affected_cis, event_date,
        reported_by, department, affected_services,
        affected_departments, assigned_to, assignee_department,
        response_date, source_of_evidence, closure_date,
        initial_assessment
    ))  # Add more fields as per your SharePoint list schema

for _, row in data_frame.iterrows():
    item_id = row.get("ID")
    if pd.isnull(item_id):
        item_data = {
            "Status": row["Status"],
            "Description of Event": str(row["Description of Event"]),  
            "Username": row["Username"],
            "Event Type": row["Event Type"],
            "Affected CI(s)": row["Affected CI(s)"],
            "Event Reporting Date & Time": str(row["Event Reporting Date & Time"]),
            "Reported By(Name of the Person)": row["Reported By(Name of the Person)"],
            "Department(of the Person Reporting)": row["Department(of the Person Reporting)"],
            "Affected Service(s)": row["Affected Service(s)"],
            "Affected Department(s)": row["Affected Department(s)"],
            "Assigned To": row["Assigned To"],
            "Assignee's Department": row["Assignee's Department"],
            "Event Response Date & Time": str(row["Event Response Date & Time"]),
            "Source of Evidence": row["Source of Evidence"],
            "Event Closure or Upgradation Date": str(row["Event Closure or Upgradation Date"]),
            "Initial Assessment": row["Initial Assessment"]
        }
        # Check if the item data already exists in SharePoint
        if (item_data["Status"], item_data["Description of Event"], item_data["Username"], item_data["Event Type"], item_data["Affected CI(s)"], item_data["Event Reporting Date & Time"], item_data["Reported By(Name of the Person)"], item_data["Department(of the Person Reporting)"], item_data["Affected Service(s)"], item_data["Affected Department(s)"], item_data["Assigned To"], item_data["Assignee's Department"], item_data["Event Response Date & Time"], item_data["Source of Evidence"], item_data["Event Closure or Upgradation Date"], item_data["Initial Assessment"]) not in existing_data:
            sp_list.UpdateListItems(data=[item_data], kind='New')
            print("Item inserted successfully.")
        else:
            print("Skipping duplicate item.")
            logging.info('\r\n'+'------Skiped items----------'+'\n\r'+'Status: ' + str(item_data['Status']) +'\n\r'+'Description of Event: ' + str(item_data['Description of Event']) + '\n\r'+'Username: ' + str(item_data['Username'])+'\r\n'+'Event Type: ' + str(item_data['Event Type'])+'\r\n' + 'Affected CI(s): ' + str(item_data['Affected CI(s)']) +'\n\r'+ 'Event Reporting Date & Time: ' + str(item_data['Event Reporting Date & Time']) +'\n\r'+ '----------------')
            print("Skipped item:", item_data)


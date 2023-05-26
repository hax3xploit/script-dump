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
        item["ID"], status, description, username,
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
        if (item["ID"], item["Status"], item["Description of Event"], item["Username"], item["Event Type"], item["Affected CI(s)"], item["Event Reporting Date & Time"], item["Reported By(Name of the Person)"], item["Department(of the Person Reporting)"], item["Affected Service(s)"], item["Affected Department(s)"], item["Assigned To"], item["Assignee's Department"], item["Event Response Date & Time"], item["Source of Evidence"], item["Event Closure or Upgradation Date"], item["Initial Assessment"]) not in existing_data:
            sp_list.UpdateListItems(data=[item_data], kind='New')
            print("Item inserted successfully.")
        else:
            print("Skipping duplicate item.")
            logging.info('\r\n'+'------Skiped items----------'+'\n\r'+item+'\r\n'+'----------------')
            print("Skipped item:", item)


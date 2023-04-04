# Author: Abdullah Khawaja
# Date: 19-1-2023
# Version: 3.4
# Tested on: Windows 11


import extract_msg
from colorama import Fore, Back, Style
from datetime import date, datetime
import sys, threading
import logging
import glob
import csv
import os
import re
import time





GREEN =  '\033[32m' # Green Text
RED =  '\033[31m' # Red Text
RESET = '\033[m' # reset to the defaults

print(Fore.RED+r"""

          ___    .                         +
*  .      \  \     _ _       *        ,---------------------------,
           \**\ ___\/ \...............|        @hax_3xploit       | .
   .     X*######*+~\__\              `---------------------------'
      +    o/\  \           .           *      .
              \__\                     .                  .
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
              _   _ _              _   _   _                 _ 
             | | | (_)_ __ ___  __| | | | | | __ _ _ __   __| |
             | |_| | | '__/ _ \/ _` | | |_| |/ _` | '_ \ / _` |
             |  _  | | | |  __/ (_| | |  _  | (_| | | | | (_| |
             |_| |_|_|_|  \___|\__,_| |_| |_|\__,_|_| |_|\__,_|
                                                               
                        [*] Parse Emails on FLY!✈️
            """,RESET)



top_header = ['ID', 'Status', 'Description of Event', 'Username', 'Event Type', 'Affected CI(s)', 'Event Reporting Date & Time', 'Reported By(Name of the Person)', 'Department(of the Person Reporting)', 'Affected Service(s)', 'Affected Department(s)', 'Assigned To', 'Assignee\'s Department', 'Event Response Date & Time', 'Source of Evidence', 'Event Closure or Upgradation Date', 'Initial Assessment' ]


id_var = ''
reported_by = 'Khawaja Abdullah'
rpt_department = 'InfoSec'
affected_service = 'Desktop Service'
affected_department = ''
assigned_to = 'Muhammad Sarwar'
assignee_department = 'NOS'



date_rgx = '((1[0-2]|0?[1-9])/(3[01]|[12][0-9]|0?[1-9])/(?:[0-9]{2})?[0-9]{2})|((Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s+\d{1,2},\s+\d{4})' 
time_rgx = '(?:1[0-2]|0?[0-9]):[0-5][0-9]:[0-5][0-9] ([AaPp][Mm])'


out_file_name =  str(date.today())+'.csv'


log_file_name = str(datetime.now())
err_log_file_name = str(datetime.now())


msg_file_path = str(input("Enter Path to MSG file(s): "))   # e.g: D:\InsoSecSS\IncidentHadling\script_testing\
out_file_location = str(input("Enter Output folder: "))     # e.g: D:\InsoSecSS\IncidentHadling\script_testing\



print("\n")

print("Loading:")
animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]

for i in range(len(animation)):
    time.sleep(0.2)
    sys.stdout.write("\r"+Fore.CYAN+ animation[i % len(animation)]+RESET)
    sys.stdout.flush()

print("\n")


file_path = str(out_file_location+out_file_name)




logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', filename='logs.log', filemode='w',level=logging.INFO)



# open the file in the write mode
f = glob.glob(msg_file_path+'\*.msg')
    

with open(file_path, 'w', encoding='utf-8', newline='') as l:
    writer = csv.writer(l)
    #write the header
    writer.writerow(top_header)


    for filename in f:
        msg = extract_msg.Message(filename)
        msg_sender = msg.sender
        msg_date = msg.date
        msg_subj = msg.subject
        msg_message = msg.body

        if re.search('Warning: Legitimate software', msg_subj):
            if re.search('Type:', msg_message):
                arr = msg_message.split('\r\n')

                description = arr[0]

                event_name_extract = re.findall('"([^"]*)"', description)

                event_name = 'Legitimate software'

                result_description = arr[1]

                event_type_parse = arr[2].split(':')

                event_type = event_type_parse[1]

                trojan_name = arr[3]

                username = arr[4]

                username_regx = re.findall('(\S+)',username)

                user_name = username_regx[1]

                object_name = arr[5].replace('Object:', '')

                date_time = re.search(date_rgx, description).group(0)

                computer_name = description.split('on computer')[1].split(' ')[1]

                if re.search('Trojan', event_type):
                    event_type = event_type.replace('Trojan','Malware Identified')
                elif re.search('Virus', event_type):
                    event_type = event_type.replace('Virus','Malware Identified')
                elif re.search('Adware', event_type):
                    event_type = event_type.replace('Adware','Adware Identified')
                elif re.search('Contains adware', event_type):
                    event_type = event_type.replace('Adware','Adware Identified')


                print('File Name: '+filename)
                print(Fore.GREEN+'[+] '+Fore.RESET+'Success.')

                writer.writerow([id_var, 'In Progress', event_name+' - '+object_name, user_name, event_type, computer_name, date_time, reported_by, rpt_department, affected_service, affected_department, assigned_to, assignee_department, date_time])

                
                #logging.info('File Name: '+filename+'\r\n'+'User Name: '+user_name+'\r\n'+'Computer Name: '+computer_name+'\r\n'+'Event Name: '+event_name+'\r\n'+'Object Name: '+object_name+'\r\n'+'----------------')
                logging.info(msg_message+'\r\n'+'----------------')
                print (f'<================================================================>')


            if not re.search('Type:', msg_message):
                arr = msg_message.split('\r\n')

                description = arr[0]

                event_name_extract = re.findall('"([^"]*)"', description)

                event_name = 'Legitimate software'

                result_description = arr[1]
                
                username = arr[2]

                username_regx = re.findall('(\S+)',username)

                user_name = username_regx[1]

                object_name = arr[3].replace('Object:', '')

                date_time = re.search(date_rgx, description).group(0)

                computer_name = description.split('on computer')[1].split(' ')[1]

                if re.search('Trojan', event_type):
                    event_type = event_type.replace('Trojan','Malware Identified')
                elif re.search('Virus', event_type):
                    event_type = event_type.replace('Virus','Malware Identified')
                elif re.search('Adware', event_type):
                    event_type = event_type.replace('Adware','Adware Identified')
                elif re.search('Contains adware', event_type):
                    event_type = event_type.replace('Adware','Adware Identified') 

                print('File Name: '+filename)
                print(Fore.GREEN+'[+] '+Fore.RESET+'Success.')

                writer.writerow([id_var, 'In Progress', event_name+' - '+object_name, user_name, event_type, computer_name, date_time, reported_by, rpt_department, affected_service, affected_department, assigned_to, assignee_department, date_time])

                #logging.info('File Name: '+filename+'\r\n'+'User Name: '+user_name+'\r\n'+'Computer Name: '+computer_name+'\r\n'+'Event Name: '+event_name+'\r\n'+'Object Name: '+object_name+'\r\n'+'----------------')

                logging.info(msg_message+'\r\n'+'----------------')
                print (f'<================================================================>')

        elif re.search('Critical: Disinfection impossible', msg_subj):
            if re.search('Type:', msg_message):
                arr = msg_message.split('\r\n')

                description = arr[0]

                event_name_extract = re.findall('"([^"]*)"', description)

                event_name = 'Disinfection impossible'

                result_description = arr[1]

                event_type_parse = arr[2].split(':')

                event_type = event_type_parse[1]

                trojan_name = arr[3]

                username = arr[4]

                username_regx = re.findall('(\S+)',username)

                user_name = username_regx[1]

                object_name = arr[5].replace('Object:', '')

                date_time = re.search(date_rgx, description).group(0)

                computer_name = description.split('on computer')[1].split(' ')[1]

                if re.search('Trojan', event_type):
                    event_type = event_type.replace('Trojan','Malware Identified')
                elif re.search('Virus', event_type):
                    event_type = event_type.replace('Virus','Malware Identified')
                elif re.search('Adware', event_type):
                    event_type = event_type.replace('Adware','Adware Identified')
                elif re.search('Contains adware', event_type):
                    event_type = event_type.replace('Adware','Adware Identified')

                print('File Name: '+filename)
                print(Fore.GREEN+'[+] '+Fore.RESET+'Success.')

                writer.writerow([id_var, 'In Progress', event_name+' - '+object_name, user_name, event_type, computer_name, date_time, reported_by, rpt_department, affected_service, affected_department, assigned_to, assignee_department, date_time])

                logging.info(msg_message+'\r\n'+'----------------')

                print (f'<================================================================>')

        elif re.search('Critical: Disinfection not possible', msg_subj):
            if re.search('User:', msg_message):
                arr = msg_message.split('\r\n')
                description = arr[0]

                event_name_extract = re.findall('"([^"]*)"', description)

                event_name = 'Disinfection not possible'

                result_description = arr[1]
                
                username = arr[2]

                username_regx = re.findall('(\S+)',username)

                user_name = username_regx[1]

                object_name = arr[3].replace('Object:', '')

                date_time = re.search(date_rgx, description).group(0)

                computer_name = description.split('on computer')[1].split(' ')[1]


                print('File Name: '+filename)
                
                print(Fore.GREEN+'[+] '+Fore.RESET+'Success.')

                writer.writerow([id_var, 'In Progress', event_name+' - '+object_name, user_name, event_type, computer_name, date_time, reported_by, rpt_department, affected_service, affected_department, assigned_to, assignee_department, date_time])

                #logging.info('File Name: '+filename+'\r\n'+'User Name: '+user_name+'\r\n'+'Computer Name: '+computer_name+'\r\n'+'Event Name: '+event_name+'\r\n'+'Object Name: '+object_name+'\r\n'+'----------------')
                logging.info(msg_message+'\r\n'+'----------------')
                print (f'<================================================================>')

        elif re.search('Critical: Object not disinfected', msg_subj):

            arr = msg_message.split('\r\n')

            description = arr[0]

            event_name_extract = re.findall('"([^"]*)"', description)

            event_name = 'Object not disinfectede'

            result_description = arr[1]
                           
            username_regx = re.findall('(\S+)',username)

            user_name = username_regx[1]

            object_name = arr[2].replace('Object:', '')

            computer_name = description.split('on computer')[1].split(' ')[1]

            date_time = re.search(date_rgx, description).group(0)


            print('File Name: '+filename)

            print(Fore.GREEN+'[+] '+Fore.RESET+'Success.')

            writer.writerow([id_var, 'In Progress', event_name+' - '+object_name, user_name, event_type, computer_name, date_time, reported_by, rpt_department, affected_service, affected_department, assigned_to, assignee_department, date_time])

            #logging.info('File Name: '+filename+'\r\n'+'User Name: '+user_name+'\r\n'+'Computer Name: '+computer_name+'\r\n'+'Event Name: '+event_name+'\r\n'+'Object Name: '+object_name+'\r\n'+'----------------')

            logging.info(msg_message+'\r\n'+'----------------')
            print (f'<================================================================>')

        else:
            
            print (f'------------->'+Fore.RED+ 'Can\'t Parse, Invalid Format'+Fore.RESET+' <---------')

            print('File Name: '+filename)

            print(Fore.RED+'[-] '+Fore.RESET+'Failed.')

            logging.error('File Name: '+filename+'----------------')

            print (f'-------------------------------------------------------')









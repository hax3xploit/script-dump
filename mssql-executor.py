import os
import pymssql
import threading


HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def execute_sql(sql, conn, sql_file_path):
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
        conn.commit()
        print(f"{OKGREEN}[+] Executed {ENDC} {sql_file_path}")
    except pymssql.Error as e:
        print(f"{FAIL}[-] {ENDC}Error executing {sql_file_path}: {e}")

def execute_sql_files_in_directory(directory_path, conn):
    threads = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".sql"):
                sql_file_path = os.path.join(root, file)
                with open(sql_file_path, "r") as f:
                    sql = f.read()
                thread = threading.Thread(target=execute_sql, args=(sql, conn, sql_file_path))
                thread.start()
                threads.append(thread)
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    server = "your_server_name"
    username = "your_username"
    password = "your_password"
    database = "your_database_name"
    
    try:
        conn = pymssql.connect(server=server, user=username, password=password, database=database)
        conn.ping()
        print(f"{OKGREEN}[+]{ENDC} Database connection test succeeded.")
    except pymssql.Error as e:
        print(f"{FAIL}[-] {ENDC} Database connection test failed: {e}")
        exit(1)
        
    execute_sql_files_in_directory(f"path/to/directory", conn)
    conn.close()

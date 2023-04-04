import os
import concurrent.futures



HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


folder_path = input("Please enter folder location: ")
sql_folder = input("Please enter output folder location: ")
code_extensions = [".py", ".php", ".java", ".cpp", ".c", ".h", ".js", ".html", ".css", ".rb", ".pl", ".sh", ".m", ".swift", ".kt", ".scala", ".cs", ".vb", ".aspx", ".jsp", ".xml", ".json", ".yaml", ".yml", ".ini", ".conf", ".md", ".txt"]


def get_code_files(folder_path):
    code_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            for ext in code_extensions:
                if file.endswith(ext):
                    file_path = os.path.join(root, file)
                    code_files.append(file_path)
    return code_files


def write_sql_query(file_path, sql_folder):
    try:
        with open(file_path, "r") as f:
            source_code = f.read()
            source_code = source_code.replace("'", "").replace('"', '')
            filename = os.path.basename(file_path)
            sql_query = f"INSERT INTO cs_fp (filename, source_code) VALUES ('{filename}', '{source_code}');"
            sql_file_path = os.path.join(sql_folder, f"{filename}.sql")
            with open(sql_file_path, "w", encoding="utf8") as sql_file:
                sql_file.write(sql_query)
                print(f"{OKGREEN}[+]{ENDC} Wrote SQL query for {filename}")
    except Exception as e:
        print(f"{WARNING}[*]{ENDC} Error processing {file_path}: {e}")


code_files = get_code_files(folder_path)
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for file_path in code_files:
        futures.append(executor.submit(write_sql_query, file_path, sql_folder))
    for future in concurrent.futures.as_completed(futures):
        try:
            future.result()
        except Exception as e:
            print(f"{FAIL}[-] Error: {ENDC} {e}")

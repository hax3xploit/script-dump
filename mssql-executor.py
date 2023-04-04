import os
import pymssql
import threading

def execute_sql(sql, conn, sql_file_path):
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
        conn.commit()
        print(f"Executed {sql_file_path}")
    except pymssql.Error as e:
        print(f"Error executing {sql_file_path}: {e}")

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
        print("Database connection test succeeded.")
    except pymssql.Error as e:
        print(f"Database connection test failed: {e}")
        exit(1)
        
    execute_sql_files_in_directory("path/to/directory", conn)
    conn.close()

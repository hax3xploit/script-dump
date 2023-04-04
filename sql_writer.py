import os
import concurrent.futures
from colorama import Fore, Back, Style



folder_path = input("Please enter folder location: ")
sql_folder = input("Please enter output folder location: ")
code_extensions = [".aspx", ".au", ".bak", ".baml", ".c", ".cache", ".cd", ".coffee", ".Compressed Files", ".cpp", ".cs", ".cshtml", ".csproj", ".css", ".Databases", ".disco", ".discomap", ".Dockerfile", ".Docs", ".dtproj", ".edmx", ".edr", ".ent", ".env", ".eot", ".ep", ".epgz", ".epz", ".er1", ".fd", ".fdt", ".fdx", ".feature", ".filters", ".flow", ".fmb", ".fnc", ".fnt", ".FOT", ".GID", ".glb", ".gmk", ".go", ".gradle", ".Graphics", ".gyp", ".gypi", ".h", ".hlf", ".hpp", ".htc", ".html", ".java", ".jfif", ".jfm", ".jks", ".jmconfig", ".jmx", ".jnlp", ".jpa", ".jpr", ".js", ".json", ".json5", ".jsonc", ".jsp", ".jst", ".jsx", ".ko", ".kt", ".launch", ".layout", ".less", ".m", ".m4", ".manifest", ".map", ".markdown", ".Master", ".mdx", ".Misc", ".mobileprovision", ".modulemap", ".node", ".nupkg", ".nuspec", ".patch", ".pbd", ".pbl", ".pblx", ".pbr", ".pbt", ".pbtx", ".pcf", ".pdb", ".php", ".pkb", ".pks", ".plist", ".pp", ".prc", ".prefs", ".projdata", ".properties", ".props", ".psd1", ".pubxml", ".py", ".pyc", ".R", ".resources", ".resx", ".rnn", ".rpt", ".SCC", ".scss", ".Setups", ".sh", ".shfbproj", ".sitemap", ".sl", ".sln", ".snap", ".snk", ".so", ".spc", ".spl", ".srd", ".sru", ".storyboard", ".strings", ".suo", ".svc", ".svcinfo", ".svclog", ".svcmap", ".swift", ".t", ".targets", ".tdr", ".template", ".toml", ".tps", ".transform", ".trdx", ".trg", ".trx", ".ts", ".tsx", ".tt", ".ttf", ".tv", ".UDF", ".user", ".vb", ".vbproj", ".vcproj", ".vcxproj", ".vdproj", ".Videos", ".VIW", ".vspscc", ".vw", ".webinfo", ".wixproj", ".woff", ".woff2", ".wsdl", ".xaml", ".xcconfig", ".xcscheme", ".xdt", ".xib", ".xlsm", ".xml", ".xsd", ".xsl", ".xslt", ".xss", ".xsx", ".yaml", ".yml", ".zip"]



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
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            source_code = f.read()
            source_code = source_code.replace("'", "").replace('"', '')
            filename = os.path.basename(file_path)
            file_extension = os.path.splitext(filename)[1][1:]
            sql_query = f"INSERT INTO {file_extension} (filename, source_code) VALUES ('{filename}', '{source_code}');"
            sql_file_path = os.path.join(sql_folder, f"{filename}.sql")
            with open(sql_file_path, "w", encoding="utf8", errors='ignore') as sql_file:
                sql_file.write(sql_query)
                print(f"{Fore.GREEN}[+]{Fore.RESET} Wrote SQL query for {filename}")
    except Exception as e:
        print(f"{Fore.YELLOW}[*]{Fore.RESET} Error processing {file_path}: {e}")


code_files = get_code_files(folder_path)
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for file_path in code_files:
        futures.append(executor.submit(write_sql_query, file_path, sql_folder))
    for future in concurrent.futures.as_completed(futures):
        try:
            future.result()
        except Exception as e:
            print(f"{Fore.RED}[-] Error: {Fore.RESET} {e}")

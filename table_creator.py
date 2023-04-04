import pyodbc

# Create a connection to MSSQL server
server = '<your_server_name>'
database = '<your_database_name>'
username = '<your_username>'
password = '<your_password>'

try:
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    print("Connection established successfully.")
except pyodbc.Error as ex:
    print("Error connecting to MSSQL server:")
    print(ex)
    exit()


tables = ["aspx", "au", "bak", "baml", "c", "cache", "cd", "coffee", "cpp", "cs", "cshtml", "csproj", "css", "Databases", "disco", "discomap", "Dockerfile", "Docs", "dtproj", "edmx", "edr", "ent", "env", "eot", "ep", "epgz", "epz", "er1", "fd", "fdt", "fdx", "feature", "filters", "flow", "fmb", "fnc", "fnt", "FOT", "GID", "glb", "gmk", "go", "gradle", "Graphics", "gyp", "gypi", "h", "hlf", "hpp", "htc", "html", "java", "jfif", "jfm", "jks", "jmconfig", "jmx", "jnlp", "jpa", "jpr", "js", "json", "json5", "jsonc", "jsp", "jst", "jsx", "ko", "kt", "launch", "layout", "less", "m", "m4", "manifest", "map", "markdown", "Master", "mdx", "Misc", "mobileprovision", "modulemap", "node", "nupkg", "nuspec", "patch", "pbd", "pbl", "pblx", "pbr", "pbt", "pbtx", "pcf", "pdb", "php", "pkb", "pks", "plist", "pp", "prc", "prefs", "projdata", "properties", "props", "psd1", "pubxml", "py", "pyc", "R", "resources", "resx", "rnn", "rpt", "SCC", "scss", "Setups", "sh", "shfbproj", "sitemap", "sl", "sln", "snap", "snk", "so", "spc", "spl", "srd", "sru", "storyboard", "strings", "suo", "svc", "svcinfo", "svclog", "svcmap", "swift", "t", "targets", "tdr", "template", "toml", "tps", "transform", "trdx", "trg", "trx", "ts", "tsx", "tt", "ttf", "tv", "UDF", "user", "vb", "vbproj", "vcproj", "vcxproj", "vdproj", "Videos", "VIW", "vspscc", "vw", "webinfo", "wixproj", "woff", "woff2", "wsdl", "xaml", "xcconfig", "xcscheme", "xdt", "xib", "xlsm", "xml", "xsd", "xsl", "xslt", "xss", "xsx", "yaml", "yml", "zip"]


for table_name in tables:
    cursor = cnxn.cursor()
    cursor.execute(f"CREATE TABLE {table_name} (filename VARCHAR(200), source_code VARCHAR](MAX))")
    cursor.commit()
    print(f"Table {table_name} created successfully.")


cnxn.close()

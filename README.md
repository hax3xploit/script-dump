## Nessus-DL.py
> This code authenticates with a Nessus server using API keys. It retrieves a list of available scans and filters them based on predefined scan names. For each filtered scan, it generates a CSV report and waits for the report to be ready. Once ready, it downloads the report and saves it in separate folders based on the scan type (Windows, Linux, VIS, or Cisco). The code utilizes the requests library for making API requests and handles error scenarios.

## Sharepoint.py
> This script interacts with SharePoint to insert new items from an Excel file into a specific list. It uses the shareplum library for SharePoint integration and the pandas library for reading Excel data. The script establishes a connection to SharePoint using NTLM authentication and retrieves the target list. It then reads data from the Excel file and compares it with existing data in SharePoint to avoid duplicates. If a new item is found, it is added to the SharePoint list, and the script logs the skiped item's details. Duplicate items are skipped.

## mssql-executor.py
> This code reads in SQL queries from a directory of .sql files and executes them on a Microsoft SQL Server database using the pymssql library. The updated version of the code uses threading to execute each query in a separate thread, allowing for faster execution. The code also includes error handling for database connection issues and SQL execution errors.

## query-executor.py
> This Python script executes all SQL files in a specified directory and its subdirectories for a MSSQL database with error handling and database connection check, using the pyodbc library for database connectivity.

## sql-writer.py
> This Python script finds all code files with specific extensions in the input folder, and writes SQL queries for each code file into the output folder concurrently using multithreading.

## table_creator.py
> This script creates tables in MSSQL from a list of table names using the pyodbc library in Python.

## filter.py
> This Python code sorts files in a directory by extension and removes duplicate files using MD5 hashing, and generates a file containing the hashes of the remaining files.

## threader.py
> This code removes duplicate files in a directory using MD5 hashing and writes the hashes and corresponding file paths to a text file.

## exe2reg.py
> This Python script modifies the Windows Registry to white-list the execution of specified executable files, as defined in a user-provided text file.

## HH3.4.py
> This is a Python script that extracts information from MSG files in a specified directory, parses the information to fill in a CSV template, and saves the output to a specified location. The script logs information to a file, and includes regular expressions to extract information from the messages.





## mssql-executor.py

> This code reads in SQL queries from a directory of .sql files and executes them on a Microsoft SQL Server database using the pymssql library. The updated version of the code uses threading to execute each query in a separate thread, allowing for faster execution. The code also includes error handling for database connection issues and SQL execution errors.

## filter.py

> This Python code sorts files in a directory by extension and removes duplicate files using MD5 hashing, and generates a file containing the hashes of the remaining files.

## sql-writer.py

> This Python script finds all code files with specific extensions in the input folder, and writes SQL queries for each code file into the output folder concurrently using multithreading.

## exe2reg.py
> This Python script modifies the Windows Registry to white-list the execution of specified executable files, as defined in a user-provided text file.

## HH3.4.py
> This is a Python script that extracts information from MSG files in a specified directory, parses the information to fill in a CSV template, and saves the output to a specified location. The script logs information to a file, and includes regular expressions to extract information from the messages.

## threader.py
> This code removes duplicate files in a directory using MD5 hashing and writes the hashes and corresponding file paths to a text file.

## query-executor.py
> This Python script executes all SQL files in a specified directory and its subdirectories for a MSSQL database with error handling and database connection check, using the pyodbc library for database connectivity.

## table_creator.py
> This script creates tables in MSSQL from a list of table names using the pyodbc library in Python.

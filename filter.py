import os
import shutil
import hashlib
import string
import random


HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'



def sort_files_by_extension(root_directory):
    skipped_files = []  # to store names of files that are skipped
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:

            N = 7
            res = ''.join(random.choices(string.ascii_uppercase +
                                         string.digits, k=N))
            extension = os.path.splitext(filename)[1]

            new_file_name = os.path.splitext(filename)[0]+'-'+str(res)+extension

            if extension:
                destination_folder = os.path.join(root_directory, extension[1:])
                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)
                source_file = os.path.join(dirpath, filename)
                destination_file = os.path.join(destination_folder, new_file_name)
                try:
                    shutil.move(source_file, destination_file)
                    print(f"{OKGREEN}[+]{ENDC}Moved file: {source_file} to {destination_file}")
                except Exception as e:
                    skipped_files.append(filename)
                    print(f"{FAIL}[-]{ENDC}Error occurred while moving file: {source_file}")
                    print(e)

    # create and write skipped files to a text file
    if skipped_files:
        with open(os.path.join(root_directory, "skipped_files.txt"), 'a') as f:
            for file_name in skipped_files:
                f.write(f"{file_name}\n")


def remove_duplicates(dir_path):
    # dictionary to store hash values and corresponding file paths
    hash_dict = {}

    # recursively traverse the directory and its subdirectories
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            # get the full file path
            file_path = os.path.join(root, file)

            # calculate the hash of the file
            with open(file_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()

            # check if the hash value is already in the dictionary
            if file_hash in hash_dict:
                # if yes, remove the file
                os.remove(file_path)
                print(f"{FAIL}[-]{ENDC} {file_path} removed due to duplicate hash")
            else:
                # if no, add the hash value and file path to the dictionary
                hash_dict[file_hash] = file_path
                print(f"{OKGREEN}[+]{ENDC} {file_path} added to hash dictionary")

    output_file = os.path.join(dir_path, "MD5_hashes.txt")
    with open(output_file, 'w') as f:
        for file_path, file_hash in hash_dict.items():
            f.write(f"{file_hash}  {file_path}\n")

    return output_file


if __name__ == '__main__':
    directory = input("Enter directory path to sort files: ")
    sort_files_by_extension(directory)
    remove_duplicates(directory)

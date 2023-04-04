import os
import shutil
import hashlib
import string
import random
from concurrent.futures import ThreadPoolExecutor, as_completed


def hash_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
        return file_hash, file_path
    except Exception as e:
        print(f"{FAIL}[-]{ENDC} Error hashing file {file_path}: {e}")
        return None


def remove_duplicates(dir_path):
    hash_dict = {}

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = []
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                futures.append(executor.submit(hash_file, file_path))

        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                file_hash, file_path = result
                if file_hash in hash_dict:
                    try:
                        os.remove(file_path)
                        print(f"{FAIL}[-]{ENDC} {file_path} removed due to duplicate hash")
                    except Exception as e:
                        print(f"{FAIL}[-]{ENDC} Error removing file {file_path}: {e}")
                else:
                    hash_dict[file_hash] = file_path
                    print(f"{OKGREEN}[+]{ENDC} {file_path} added to hash dictionary")

    output_file = os.path.join(dir_path, "MD5_hashes.txt")
    try:
        with open(output_file, 'w') as f:
            for file_path, file_hash in hash_dict.items():
                f.write(f"{file_hash}  {file_path}\n")
    except Exception as e:
        print(f"{FAIL}[-]{ENDC} Error writing to file {output_file}: {e}")

    return output_file


if __name__ == '__main__':
    directory = input("Enter directory path to sort files: ")
    try:
        remove_duplicates(directory)
    except Exception as e:
        print(f"{FAIL}[-]{ENDC} Error removing duplicates: {e}")

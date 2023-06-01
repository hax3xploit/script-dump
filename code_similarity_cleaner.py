import os
from difflib import SequenceMatcher
from shutil import copy2, SameFileError


GREEN = '\033[32m'  # Green Text
RED = '\033[31m'  # Red Text
RESET = '\033[m'  # reset to the defaults
BGreen = '\033[1;32m'  # Green
BYellow = '\033[1;33m'  # Yellow
BBlue = '\033[1;34m'  # Blue
BPurple = "\033[1;35m"  # Purple
BCyan = "\033[1;36m"  # Cyan
BWhite = "\033[1;37m"  # White
BRIGHT = '\033[1m'


def load_code_files(directory):
    code_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            code_files.append(os.path.join(root, file))
    return code_files


def compare_similarity(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        code1 = f1.readlines()
        code2 = f2.readlines()
        similarity_ratio = SequenceMatcher(None, code1, code2).ratio()
        return similarity_ratio


def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"{RED}[-]{RESET} Deleting file: {BWhite}{os.path.basename(file_path)}{RESET}")
    except Exception as e:
        print(f"{RED}[-]{RESET} Error: An unexpected error occurred while deleting the file: {str(e)}")


def create_similar_data_set(directory, similarity_threshold):
    code_files = load_code_files(directory)
    total_files = len(code_files)
    output_directory = os.path.join(directory, 'Similar_Data_Set')
    os.makedirs(output_directory, exist_ok=True)

    for i in range(total_files):
        file1 = code_files[i]
        extension1 = os.path.splitext(file1)[1]
        subdirectory = os.path.join(output_directory, extension1.strip('.'))
        os.makedirs(subdirectory, exist_ok=True)

        for j in range(i + 1, total_files):
            file2 = code_files[j]
            extension2 = os.path.splitext(file2)[1]

            if extension1 == extension2:
                similarity = compare_similarity(file1, file2)
                if similarity >= similarity_threshold:
                    file1_size = os.path.getsize(file1)
                    file2_size = os.path.getsize(file2)
                    if file1_size > file2_size:
                        larger_file = file1
                        smaller_file = file2
                    else:
                        larger_file = file2
                        smaller_file = file1

                    try:
                        copy2(larger_file, subdirectory)
                        print(f"{GREEN}[+]{RESET} Similarity between {BWhite}{os.path.basename(file1)}{RESET} and {BWhite}{os.path.basename(file2)}{RESET}:{GREEN} {similarity * 100:.2f}%{RESET}")
                        print(f"{BPurple}[+]{RESET} Copied larger file: {BWhite}{os.path.basename(larger_file)}{RESET}")
                        delete_file(larger_file)
                        delete_file(smaller_file)
                    except SameFileError:
                        print(f"{RED}[-]{RESET} Error: The files {BWhite}'{file1}'{RESET} and {BWhite}'{file2}'{RESET} are the same file. Skipped copying.")
                    except Exception as e:
                        print(f"{RED}[-]{RESET} Error: An unexpected error occurred while copying files: {str(e)}")
                elif 0.3 <= similarity < similarity_threshold:  # between 30% and 70%
                    file1_name = os.path.basename(file1)
                    file2_name = os.path.basename(file2)
                    print(f"{BYellow}[*]{RESET} Moderate similarity between {BWhite} {file1_name} {RESET} and {BWhite} {file2_name} {RESET}:{BYellow} {similarity * 100:.2f}%{RESET}")
                    delete_file(file1)
                    delete_file(file2)
                else:
                    file1_name = os.path.basename(file1)
                    file2_name = os.path.basename(file2)
                    print(f"{RED}[-]{RESET} Low similarity between {BWhite} {file1_name} {RESET} and {BWhite} {file2_name} {RESET}:{RED} {similarity * 100:.2f}%{RESET}")

    print(f"{BBlue}[+]{RESET} Comparison completed. {BRIGHT}Similar files are stored in the{RESET} {BCyan}'Similar_Data_Set'{RESET} {BWhite}directory.{RESET}")


directory = '/path/to/code/'
similarity_threshold = 0.7

create_similar_data_set(directory, similarity_threshold)

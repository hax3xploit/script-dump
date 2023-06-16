import requests
import os
import uuid
from datetime import datetime, timedelta

BASE_URL = 'https://api.github.com'

ACCESS_TOKEN = ''

SEARCH_QUERY = 'language:JavaScript'
SEARCH_SORT = 'stars'
SEARCH_ORDER = 'desc'

OUTPUT_DIR = 'downloaded_files'

def search_github_repos(query, sort, order, created_start_date, created_end_date):
    headers = {'Authorization': f'token {ACCESS_TOKEN}'}
    page = 1
    items = []

    while True:
        search_url = f'{BASE_URL}/search/repositories?q={query}+created:>={created_start_date}+created:<={created_end_date}&sort={sort}&order={order}&page={page}'
        response = requests.get(search_url, headers=headers)
        response_json = response.json()

        if 'items' in response_json:
            items += response_json['items']
            page += 1
        else:
            break

    return items


def download_javascript_files(repo_url):
    headers = {'Authorization': f'token {ACCESS_TOKEN}'}

    try:
        response = requests.get(repo_url, headers=headers)
        response_json = response.json()

        if 'name' in response_json:
            file_name = response_json['name']
            files_url = response_json['contents_url'].replace('{+path}', '')

            file_response = requests.get(files_url, headers=headers)
            if file_response.status_code == 200:
                file_response_content = file_response.json()

                for file in file_response_content:
                    if file['type'] == 'file' and file['name'].endswith('.js'):
                        file_url = file['download_url']
                        file_extension = os.path.splitext(file['name'])[1]
                        unique_number = str(uuid.uuid4())[:8]
                        file_name = f"file-{unique_number}{file_extension}"

                        if not os.path.exists(OUTPUT_DIR):
                            os.makedirs(OUTPUT_DIR)
                        file_response = requests.get(file_url, headers=headers)
                        with open(os.path.join(OUTPUT_DIR, file_name), 'wb') as f:
                            f.write(file_response.content)
                        print(f'Downloaded: {file_name}')

                    elif file['type'] == 'dir':
                        folder_url = file['url']
                        download_files_in_folder(folder_url)

            else:
                print(f"Error occurred while fetching files from {repo_url}: {file_response.content.decode('utf-8')}")
        else:
            print(f"Invalid response from {repo_url}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def download_files_in_folder(folder_url):
    headers = {'Authorization': f'token {ACCESS_TOKEN}'}

    try:
        response = requests.get(folder_url, headers=headers)
        response_json = response.json()

        if 'name' in response_json:
            files_url = response_json['url']
            file_response = requests.get(files_url, headers=headers)
            if file_response.status_code == 200:
                file_response_content = file_response.json()

                for file in file_response_content:
                    if file['type'] == 'file' and file['name'].endswith('.cs'):
                        file_url = file['download_url']
                        file_extension = os.path.splitext(file['name'])[1]
                        unique_number = str(uuid.uuid4())[:8]
                        file_name = f"file-{unique_number}{file_extension}"

                        if not os.path.exists(OUTPUT_DIR):
                            os.makedirs(OUTPUT_DIR)
                        file_response = requests.get(file_url, headers=headers)
                        with open(os.path.join(OUTPUT_DIR, file_name), 'wb') as f:
                            f.write(file_response.content)
                        print(f'Downloaded: {file_name}')

                    elif file['type'] == 'dir':
                        subfolder_url = file['url']
                        download_files_in_folder(subfolder_url)

            else:
                print(f"Error occurred while fetching files from {folder_url}: {file_response.content.decode('utf-8')}")
        else:
            print(f"Invalid response from {folder_url}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def recursive_search_and_download():
    try:
        start_year = 2013
        end_year = 2023

        date_ranges = []

        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                first_day = datetime(year, month, 1)
                last_day = first_day + timedelta(days=6)
                date_ranges.append((first_day.strftime('%Y-%m-%dT%H:%M:%SZ'), last_day.strftime('%Y-%m-%dT%H:%M:%SZ')))

        for start_date, end_date in date_ranges:
            repos = search_github_repos(SEARCH_QUERY, SEARCH_SORT, SEARCH_ORDER, start_date, end_date)

            for repo in repos:
                repo_url = repo['url']
                download_javascript_files(repo_url)
                if repo['forks_count'] > 0:
                    forks_url = f'{repo_url}/forks'
                    forks = search_github_repos(SEARCH_QUERY, SEARCH_SORT, SEARCH_ORDER, start_date, end_date)
                    for fork in forks:
                        fork_url = fork['url']
                        download_javascript_files(fork_url)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


recursive_search_and_download()

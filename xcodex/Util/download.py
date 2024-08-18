from concurrent.futures import ThreadPoolExecutor
from getpass import getpass
from os import makedirs, getcwd
from os.path import join, exists, expanduser
from time import sleep

import requests
from tqdm.notebook import tqdm

from xcodex.Util.create_dodsrc import create_dodsrc
from xcodex.Util.create_netrc import create_netrc


def download(links: list):
    """
    This method downloads .nc4 files from the provided links and saves them to the specified path.
    """
    home_dir = expanduser("~")
    netrc_path = join(home_dir, ".netrc")
    dodsrc_path = join(home_dir, ".dodsrc")

    if not exists(netrc_path) or not exists(dodsrc_path):
        print("Insert your Earthdata credentials:\n")
        username = input("Username: ")
        password = getpass("Password: ")
        if not username or not password:
            raise Exception("Please insert your authentication in order to continue")
        else:
            create_netrc(username=username, password=password)
            create_dodsrc()

    # Check if the specified directory exists and create it if it doesn't
    path = join(getcwd(), "downloaded_data")
    makedirs(path, exist_ok=True)

    # Filter .nc4 links and calculate total size
    nc4_links = [link for link in links if link.endswith('.nc4')]
    total_size = 0
    for link in nc4_links:
        response = requests.head(link)
        total_size += int(response.headers.get("content-length", 0))

    # Initialize the general progress bar
    with tqdm(total=total_size, unit='B', unit_scale=True, desc="Total Progress") as pbar:
        with ThreadPoolExecutor() as executor:
            for link in nc4_links:
                executor.submit(download_file_with_progress, link, pbar)


def download_file_with_progress(url: str, pbar):
    """
    Download a file from the internet and update the general progress bar.
    :param url: The URL of the file to download
    :param pbar: The general progress bar
    :return: None
    """
    filename = url.split("/")[-1]
    file_path = join("downloaded_data", filename)

    # Check if the file already exists
    if exists(file_path):
        return

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.3'
    }

    retries = 0
    max_retries = 10
    backoff_factor = 0.3

    while retries < max_retries:
        try:
            with requests.Session() as session:
                response = session.get(url, headers=headers, stream=True)

                # Check if the request was successful
                if response.status_code == 503:
                    retries += 1
                    sleep(backoff_factor * (2 ** retries))
                    continue
                response.raise_for_status()
                total_size = int(response.headers.get("content-length", 0))

                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
                            pbar.update(len(chunk))
            break
        except requests.exceptions.RequestException:
            retries += 1
            sleep(backoff_factor * (2 ** retries))
    else:
        pass  # Suppress the error message

from concurrent.futures import ThreadPoolExecutor
from getpass import getpass
from os import makedirs, getcwd
from os.path import expanduser, join, exists
from time import sleep

import requests
from tqdm import tqdm
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

    # Filter .nc4 links
    nc4_links = [link for link in links if link.endswith('.nc4')]

    # Calculate total size for progress bar
    total_size = len(nc4_links) * 3.20 * 1024 * 1024  # 3.20 MB per file

    # Check if all files are already downloaded
    all_downloaded = all(exists(join(path, link.split("/")[-1])) for link in nc4_links)

    with tqdm(total=total_size, unit='B', unit_scale=True, desc="Total Progress") as pbar:
        if all_downloaded:
            pbar.update(total_size)  # Complete the progress bar if all files are already downloaded
        else:
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(download_file_with_progress, link, pbar) for link in nc4_links]
                for future in futures:
                    future.result()


def download_file_with_progress(url: str, pbar):
    """
    Download a file from the internet and update the progress bar.
    :param url: The URL of the file to download
    :param pbar: The tqdm progress bar to update
    :return: None
    """
    filename = url.split("/")[-1]
    file_path = join("downloaded_data", filename)

    # Check if the file already exists
    if exists(file_path):
        file_size = 3.20 * 1024 * 1024  # Approximate size of the file in bytes
        pbar.update(file_size)
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
        print(f"Failed to download {filename} after {max_retries} attempts.")

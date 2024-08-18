from os.path import join, exists
from time import sleep

import requests
from tqdm.notebook import tqdm


def download_file_with_progress(url: str):
    """
    Download a file from the internet and show a progress bar.
    :param url: The URL of the file to download
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
                downloaded_size = 0

                with open(file_path, "wb") as file, tqdm(
                        total=total_size, unit='B', unit_scale=True, desc=filename
                ) as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
                            downloaded_size += len(chunk)
                            pbar.update(len(chunk))
            break
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            retries += 1
            sleep(backoff_factor * (2 ** retries))
    else:
        print("Failed to download the file after several retries.")

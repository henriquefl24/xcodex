def download(links: list):
    """
    This method downloads files from the provided links and saves them to the specified path.
    """
    from os.path import join
    from os import getcwd, makedirs
    from concurrent.futures import ThreadPoolExecutor
    from Util.download_file_progress import download_file_with_progress

    # Check if the specified directory exists and create it if it doesn't
    path = join(getcwd(), "downloaded_data")
    makedirs(path, exist_ok=True)

    with ThreadPoolExecutor() as executor:
        for link in links:
            executor.submit(download_file_with_progress, link)

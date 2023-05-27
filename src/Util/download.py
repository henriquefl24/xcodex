def download(links: list):
    """
    This method downloads files from the provided links and saves them to the specified path.
    """
    from os.path import join, exists, expanduser
    from os import getcwd, makedirs
    from concurrent.futures import ThreadPoolExecutor
    from Util.create_dodsrc import create_dodsrc
    from Util.create_netrc import create_netrc
    from Util.download_file_progress import download_file_with_progress

    # Check if the specified directory exists and create it if it doesn't
    path = join(getcwd(), "downloaded_data")
    makedirs(path, exist_ok=True)

    # Check the existence for the .netrc and .dodsrc files

    home_dir = expanduser("~")
    netrc_path = join(home_dir, '.netrc')
    dodsrc_path = join(home_dir, '.dodsrc')

    if not exists(netrc_path) and not exists(dodsrc_path):
        create_dodsrc()
        create_netrc(username=str(input("Username: ")), password=str(input("Password: ")))
        pass

    with ThreadPoolExecutor() as executor:
        for link in links:
            executor.submit(download_file_with_progress, link)

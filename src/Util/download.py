def download(links: list):
    """
    This method downloads files from the provided links and saves them to the specified path.
    """
    from os.path import join, exists, expanduser
    from os import getcwd, makedirs
    from getpass import getpass
    from concurrent.futures import ThreadPoolExecutor
    from Util.create_dodsrc import create_dodsrc
    from Util.create_netrc import create_netrc
    from Util.download_file_progress import download_file_with_progress
    from Util.credential import test_credentials

    home_dir = expanduser("~")
    netrc_path = join(home_dir, ".netrc")
    dodsrc_path = join(home_dir, ".dodsrc")

    if not exists(netrc_path) and not exists(dodsrc_path):
        create_dodsrc()
        username = input("Username: ")
        password = getpass("Password: ")
        if not username or not password:
            raise Exception("Please insert your EARTHDATA LOGIN authentication in order to continue")
        elif not test_credentials(username, password):
            raise Exception("Invalid EARTHDATA LOGIN credentials")
        else:
            create_netrc(username=username, password=password)

    # Check if the specified directory exists and create it if it doesn't
    path = join(getcwd(), "downloaded_data")
    makedirs(path, exist_ok=True)

    with ThreadPoolExecutor() as executor:
        for link in links:
            executor.submit(download_file_with_progress, link)

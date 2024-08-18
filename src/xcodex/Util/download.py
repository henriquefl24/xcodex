def download(links: list):
    """
    This method downloads files from the provided links and saves them to the specified path.
    """
    from os.path import join, exists, expanduser
    from os import getcwd, makedirs
    from getpass import getpass
    from concurrent.futures import ThreadPoolExecutor
    from src.xcodex.Util.create_dodsrc import create_dodsrc
    from src.xcodex.Util.create_netrc import create_netrc
    from src.xcodex.Util.download_file_progress import download_file_with_progress

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

    with ThreadPoolExecutor() as executor:
        for link in links:
            executor.submit(download_file_with_progress, link)

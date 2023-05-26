from concurrent.futures import ThreadPoolExecutor
from datetime import time
from os import getcwd, makedirs
from os.path import expanduser, join, exists

import requests
from Util.date import calendar_days


def create_netrc(username: str, password: str):
    """
    This method creates a .netrc file with the provided Earthdata credentials.
    """
    # Determine the path to the user's home directory
    home_dir = expanduser("~")

    # Create the .netrc file with the provided credentials
    with open(f"{home_dir}/.netrc", "w") as f:
        f.write(f"machine urs.earthdata.nasa.gov\n")
        f.write(f"login {username}\n")
        f.write(f"password {password}\n")


def create_dodsrc():
    """
    This method creates a .dodsrc file with the specified options.
    """
    # Determine the path to the user's home directory
    home_dir = expanduser("~")

    # Create the .dodsrc file with the specified options
    with open(f"{home_dir}/.dodsrc", "w") as f:
        f.write("check-certificate=off\n")


def generate_links(calendar_list: list):
    """
    This method generates downloadable links based on the calendar dates.
    """
    links_list = []
    for date in calendar_list:
        year_from_calendar = str(date.year)
        month_from_calendar = str(date.month).zfill(2)
        day_from_calendar = str(date.day).zfill(2)

        link = "https://oco2.gesdisc.eosdis.nasa.gov/data/OCO2_DATA/OCO2_GEOS_L3CO2_DAY.10r/" + \
               year_from_calendar + "/oco2_GEOS_L3CO2_day_" + year_from_calendar + month_from_calendar + day_from_calendar + "_B10206Ar.nc4"

        links_list.append(link)

    return links_list


def download(links: list):
    """
    This method downloads files from the provided links and saves them to the specified path.
    """

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


def download_file(start: str, end: int) -> None:
    """
    This method will effectively download .nc4 files from NASA
    Args:
        start: start date (i.e.: "1st of January, 2015")
        end: amount of days (i.e.: 365 days)

    Returns: None

    """
    date_list = calendar_days(start, end)
    links = generate_links(date_list)
    download(links)


def download_file_with_progress(url: str):
    """
    This method downloads a file from the provided URL and displays download progress.
    """
    filename = url.split("/")[-1]
    file_path = join("downloaded_data", filename)

    # Check if the file already exists
    if exists(file_path):
        print(f"File {filename} already exists.")
        return

    start_time = time()

    # Download the file using requests library
    with requests.Session() as session:
        response = session.get(url, stream=True)

        # Check if the request was successful
        if response.status_code == 200:
            total_size = int(response.headers.get("content-length", 0))
            downloaded_size = 0

            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        progress = downloaded_size / total_size * 100
                        download_speed = downloaded_size / (time.time() - start_time) / 1024  # KB/s
                        print(f"Downloading: {filename} - {progress:.2f}% | "
                              f"Speed: {download_speed:.2f} KB/s", end="\r")

            print(f"\nFile download completed: {filename}")
        else:
            print(f"Error downloading file. Response status code: {response.status_code}")
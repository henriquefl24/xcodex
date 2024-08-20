import re
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from getpass import getpass
from glob import glob
from os import getcwd, makedirs
from os.path import expanduser, join, exists
from time import sleep
from typing import Any

import requests
from netCDF4 import Dataset
from numpy import where, isclose, array, nan
from pandas import DataFrame
from pandas.errors import ParserError
from tqdm import tqdm


def xco2_extract(path: list[str],
                 start: str,
                 end: str,
                 missing_data=False,
                 **kwargs: dict) -> DataFrame:
    r"""This method will extract daily XCO2 data from the netCDF4 files.

    Args:
        path (list[str]):    Path to directory containing files .nc4 (e.g. glob.glob(r"C:\user\...\*.nc4")
        start (str):         Indicates the first day of the collected data (e.g. "1st of January, 2015")
        end (str):           Indicates the last day of the collected data (e.g. "31st of January, 2015")
        missing_data (bool): Returns a txt file containing missing data links (Default = False)
        **kwargs (dict):     city=[lat: float(), lon: float()]

    Returns:
        DataFrame:           Dataframe containing values related to the .nc4 file

    Source citation:
                            Brad Weir, Lesley Ott and OCO-2 Science Team (2022), OCO-2 GEOS Level 3 daily,
                            0.5x0.625 assimilated CO2 V10r, Greenbelt, MD, USA, Goddard Earth Sciences Data
                            and Information Services Center (GES DISC), Accessed: 10/31/2022,
                            doi: 10.5067/Y9M4NM9MPCGH

    Script authorship:
        - Henrique F. Laurito (henrique.f.laurito@unesp.br)
        - Group of Agrometeorological Studies (GAS) [FCAV/Unesp]
    """

    city, lat, lat_index, lon, lon_index, XCO2_values, XCO2PREC_values, year, \
        year_test, month, month_test, day, day_test, jd, fmt = variables()

    calendar_list = calendar_days(start, end)

    links = generate_links(calendar_list)

    # Remove ordinal suffixes from start and end date strings
    start = re.sub(r'(st|nd|rd|th)', '', start)
    end = re.sub(r'(st|nd|rd|th)', '', end)

    # Convert start and end dates to datetime objects
    start_date = datetime.strptime(start, '%d of %B, %Y')
    end_date = datetime.strptime(end, '%d of %B, %Y')

    # Calculate the number of days between the start and end dates
    days_between = (end_date - start_date).days

    c = d = e = 0  # Declaration of counters used in the loop

    while c < len(path):  # Iterates the netCDF4 folder

        i = 0

        xco2_netCDF4 = Dataset(path[c])

        if check_date(calendar_list, xco2_netCDF4):
            c += 1
            pass
        else:

            for k, v in kwargs.items():

                # Saving municipalities and coordinates in deque

                city.append(k)
                lat.append(v[0])
                lon.append(v[1])

                # Assign calendar year, month, day and julians days for comparison

                year_test.append(datetime.strptime(str(calendar_list[e]), fmt).timetuple().tm_year)
                month_test.append(datetime.strptime(str(calendar_list[e]), fmt).timetuple().tm_mon)
                day_test.append(datetime.strptime(str(calendar_list[e]), fmt).timetuple().tm_mday)
                jd.append(datetime.strptime(str(calendar_list[e]), fmt).timetuple().tm_yday)

                # netCDF4 defined date

                year.append(str(xco2_netCDF4['time'].begin_date)[0:4])
                month.append(str(xco2_netCDF4['time'].begin_date)[4:6])
                day.append(str(xco2_netCDF4['time'].begin_date)[6:])

                # Comparison of calendar day with file day

                if int(day[d]) != day_test[d] or int(year[d]) != year_test[d]:

                    lat_index.append(nan)
                    lon_index.append(nan)
                    XCO2_values.append(nan)
                    XCO2PREC_values.append(nan)

                    day.pop()
                    day.append(str(day_test[d]))

                    month.pop()
                    month.append(str(month_test[d]))

                    year.pop()
                    year.append(str(year_test[d]))

                    d += 1
                    i += 1

                    if i >= len(kwargs.items()):  # This step will repeat the loop
                        c -= 1

                else:

                    # Defining the Lat and Lon Indexes to find values in the netCDF4 file

                    lat_index.append(
                        where(
                            isclose(
                                a=array(xco2_netCDF4['lat'][:]),
                                b=array(lat[i]),
                                atol=0.5 / 2)
                        )[0][0])

                    lon_index.append(
                        where(
                            isclose(
                                a=array(xco2_netCDF4['lon'][:]),
                                b=array(lon[i]),
                                atol=0.625 / 2)
                        )[0][0])

                    # Assigning the values of XCO2 and XCO2_PREC referring to the index found

                    try:
                        XCO2_values.append(xco2_netCDF4['XCO2'][0][lat_index[i]][lon_index[i]] * 10 ** 6)
                    except IndexError:
                        i += len(kwargs.items())
                        XCO2_values.append(xco2_netCDF4['XCO2'][0][lat_index[i]][lon_index[i]] * 10 ** 6)

                    # Error handling to check the existence of the XCO2_PREC value

                    try:
                        XCO2PREC_values.append(xco2_netCDF4['XCO2PREC'][0][lat_index[i]][lon_index[i]])
                    except IndexError:
                        XCO2PREC_values.append(nan)

                    i += 1
                    d += 1

            if i >= len(kwargs.items()):
                c += 1
                e += 1

            if e > days_between:
                break

    dataframe = make_dataframe(city, jd, day, month, year, lat, lon, lat_index,
                               lon_index, XCO2_values, XCO2PREC_values)

    if missing_data:
        new_subset(dataframe)

    # Padronizing values to float

    dataframe.set_index('location', inplace=True, drop=True)
    dataframe = dataframe.astype(float)
    dataframe.reset_index(inplace=True, drop=False)
    dataframe.to_csv("output_xco2_data.csv", sep=";")

    return dataframe


def check_date(calendar_list, xco2_netCDF4: Dataset) -> bool:
    """
    This routine will check if the calendar year matches with the current file
    """

    if str(calendar_list.year[0]) > str(xco2_netCDF4['time'].begin_date)[0:4]:
        flag = True

    else:
        if str(calendar_list.month[0]) > str(xco2_netCDF4['time'].begin_date)[4:6].lstrip("0"):
            flag = True
        else:
            if str(calendar_list.day[0]) > str(xco2_netCDF4['time'].begin_date)[6:].lstrip("0"):
                flag = True
            else:
                flag = False

    return flag


def download_file(start: str, end: str) -> None:
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


def create_dodsrc():
    """
    Create a .dodsrc file in the user's home directory.
    """
    home_dir = expanduser("~")
    dodsrc_path = join(home_dir, ".dodsrc")
    with open(dodsrc_path, "w") as f:
        f.write("HTTP.COOKIEJAR = ~/.urs_cookies\n")
        f.write("HTTP.NETRC = ~/.netrc\n")


def create_netrc(username: str, password: str):
    """
    Create a .netrc file in the user's home directory with the provided EARTHDATA LOGIN credentials.
    """
    home_dir = expanduser("~")
    netrc_path = join(home_dir, ".netrc")
    with open(netrc_path, "w") as f:
        f.write(f"machine urs.earthdata.nasa.gov login {username} password {password}\n")


def calendar_days(start: str, end: str):
    """
    This method will create a union of calendar dates for further comparison.
    The main advantage of this method is to consider the leap years.
    :param start: str: i.e.: "1st of january, 2015"
    :param end: str: i.e.: "31st of january, 2015"
    :return: Union of calendar days. 01/01/2015 to 01/01/2016
    """
    from pandas import to_datetime, date_range
    try:
        start_date = to_datetime(start)  # Defines the start date of data collection
        end_date = to_datetime(end)  # Defines the end date of data collection
        calendar_list = date_range(start_date, end_date)
        return calendar_list
    except (ValueError, ParserError):
        print('\033[31m' + 'WARNING! Please, insert a valid date' + '\033[0m')
        return None


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
    file_path = join("../downloaded_data", filename)

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


def make_dataframe(city, jd, day, month, year, lat, lon, lat_index, lon_index, XCO2_values,
                   XCO2PREC_values) -> DataFrame:
    """
    This method will create the output dataframe
    Args:
        city: Pandas series
        jd: Pandas series
        day: Pandas series
        month: Pandas series
        year: Pandas series
        lat: Pandas series
        lon: Pandas series
        lat_index: Pandas series
        lon_index: Pandas series
        XCO2_values: Pandas series
        XCO2PREC_values: Pandas series

    Returns: Dataframe

    """

    dataframe = DataFrame()

    # Assigning List Values to the Dataframe

    dataframe['location'] = city
    dataframe['jd'] = jd
    dataframe['day'] = day
    dataframe['month'] = month
    dataframe['year'] = year
    dataframe['lat'] = lat
    dataframe['lon'] = lon
    dataframe['lat_index'] = lat_index
    dataframe['lon_index'] = lon_index
    dataframe['XCO2'] = XCO2_values
    dataframe['XCO2_prec'] = XCO2PREC_values

    # Organizing the dataframe

    dataframe.sort_values(by=['location', 'year'], inplace=True)
    dataframe.reset_index(inplace=True, drop=True)

    return dataframe


def new_subset(dataframe: DataFrame) -> None:
    """
    Creating a new_subset.txt based on the NaN values of the main DataFrame.
    The file will be saved on the current folder of the user
    :dataframe: Pandas.DataFrame. Takes the xco2_extract dataframe to identificate the NaN values.
    :return: None
    """
    dataframe = dataframe.loc[dataframe['XCO2'].isna()]
    dataframe.reset_index(inplace=True, drop=True)

    links_list = []
    for _, row in dataframe.iterrows():
        year = str(row.iloc[4])
        month = str(row.iloc[3]).zfill(2)
        day = str(row.iloc[2]).zfill(2)

        link = f"https://oco2.gesdisc.eosdis.nasa.gov/data/OCO2_DATA/OCO2_GEOS_L3CO2_DAY.10r/{year}/oco2_GEOS_L3CO2_day_{year}{month}{day}_B10206Ar.nc4"
        links_list.append(link)

    unique_links = list(set(links_list))

    with open('new_subset.txt', 'w') as f:
        f.write('\n'.join(unique_links))

    print(f"Number of missing days: {len(dataframe)}"
          f"\nNew subset created")


def variables() -> tuple[
    deque[Any], deque[Any], deque[Any], deque[Any], deque[Any], deque[Any], deque[Any], deque[Any], deque[Any],
    deque[
        Any], deque[Any], deque[Any], deque[Any], deque[Any], str]:
    """
    This method will pack all the variables used in the main method xco2_extract()
    along with the format

    :return: packed deque()
    """

    city = deque()
    lat = deque()
    lon = deque()
    lat_index = deque()
    lon_index = deque()
    XCO2_values = deque()
    XCO2PREC_values = deque()
    year = deque()
    month = deque()
    day = deque()
    jd = deque()
    day_test = deque()
    month_test = deque()
    year_test = deque()

    fmt = r'%Y-%m-%d %H:%M:%S'

    return city, lat, lat_index, lon, lon_index, XCO2_values, XCO2PREC_values, year, year_test, month, month_test, day, day_test, jd, fmt


#%%

# Setting historical serie

start_date = "1st of January, 2015"
end_date = "10th of January, 2015"

download_file(start_date, end_date)  # Downloading .nc4 files (Global)

#%%

arquive_folder = glob(
    join(getcwd(), "downloaded_data", "*.nc4"))  # Selecting the folder with nc4 files (Default location)

# Setting desired locations to build a time series XCO2 data

locations = dict(Mauna_loa=[19.479488, -155.602829],
                 New_York=[40.712776, -74.005974],
                 Paris=[48.856613, 2.352222])

#%%

df = xco2_extract(path=arquive_folder,
                  start=start_date,
                  end=end_date,
                  missing_data=True,
                  **locations)

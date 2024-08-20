from pandas import DataFrame
from netCDF4 import Dataset
from numpy import where, isclose, array, nan
from datetime import datetime
import re
from xcodex.Util.date import calendar_days
from xcodex.Util.missing import new_subset
from xcodex.Util.var_imp import variables
from xcodex.Util.make_Dataframe import make_dataframe
from xcodex.Util.check import check_date
from xcodex.Util.generate_links import generate_links


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

    # Patronizing values to float

    dataframe.set_index('location', inplace=True, drop=True)
    dataframe = dataframe.astype(float)
    dataframe.reset_index(inplace=True, drop=False)
    dataframe.to_csv("output_xco2_data.csv", sep=";")

    return dataframe


def download_file(start: str, end: str) -> None:
    """
    This method will effectively download .nc4 files from NASA
    Args:
        start: start date (i.e.: "1st of January, 2015")
        end: amount of days (i.e.: 365 days)

    Returns: None
    """
    from xcodex.Util.date import calendar_days
    from xcodex.Util.generate_links import generate_links
    from xcodex.Util.download import download

    date_list = calendar_days(start, end)
    links = generate_links(date_list)
    download(links)

from pandas import DataFrame
from netCDF4 import Dataset
from datetime import datetime
from numpy import where, isclose, array, NaN

from ..Util.date import calendar_days
from ..Util.make_Dataframe import make_df
from ..Util.missing import new_subset
from ..Util.var_imp import variables


def xco2_extract(path: list[str],
                 start: str,
                 end: int,
                 missing_data=False,
                 **kwargs: dict) -> DataFrame:
    r"""This method will extract daily XCO2 data from the netCDF4 files.

    Args:
        path (list[str]):    Path to directory containing files .nc4 (e.g. glob.glob(r"C:\user\...\*.nc4")
        start (str):         Indicates the first day of the collected data (e.g. "1st of January, 2015")
        end (str):           Number of days desired (e.g. 365)
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

    c = d = e = 0  # Declaration of counters used in the loop

    while c < len(path):  # Iterates the netCDF4 folder

        i = 0

        xco2_netCDF4 = Dataset(path[c])

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

            if int(day[d]) != day_test[d]:  # Comparison of calendar day with file day

                lat_index.append(NaN)
                lon_index.append(NaN)
                XCO2_values.append(NaN)
                XCO2PREC_values.append(NaN)

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

                XCO2_values.append(xco2_netCDF4['XCO2'][0][lat_index[i]][lon_index[i]] * 10 ** 6)

                # Error handling to check the existence of the XCO2_PREC value

                try:
                    XCO2PREC_values.append(xco2_netCDF4['XCO2PREC'][0][lat_index[i]][lon_index[i]])
                except IndexError:
                    XCO2PREC_values.append(NaN)

                i += 1
                d += 1

        if i >= len(kwargs.items()):
            c += 1
            e += 1

        if c >= len(path) or c >= end or e >= end:
            break

    df = make_df(city, jd, day, month, year, lat, lon, lat_index,
                 lon_index, XCO2_values, XCO2PREC_values)

    if missing_data:
        new_subset(df)

    print(f'Number of missing days: {e - c}')

    return df

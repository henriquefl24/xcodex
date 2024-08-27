from glob import glob
from ntpath import join
from os import getcwd, makedirs
from os.path import join
import pandas as pd
import xarray as xr
from numpy import nan
from xcodex.Util.date import calendar_days
from xcodex.Util.download import download
from xcodex.Util.generate_links import generate_links
from xcodex.Util.make_Dataframe import make_dataframe
from xcodex.Util.missing import new_subset
from xcodex.Util.var_imp import variables


def xco2_extract(start: str, end: str, missing_data=False, downloaded_data_path=None, **kwargs: dict) -> pd.DataFrame:
    """
    Extracts XCO2 data from the OCO-2 satellite for the specified date range and locations.
    :param start: The start date in the format 'YYYY-MM-DD'
    :param end: The end date in the format 'YYYY-MM-DD'
    :param missing_data: A boolean value to indicate if missing data should be filled
    :param downloaded_data_path: Path to the directory containing downloaded .nc4 files
    :param kwargs: A dictionary with locations and their corresponding latitude and longitude values
    :return: A pandas DataFrame containing the extracted XCO2 data
    """
    location, lat, lat_grid, lon, lon_grid, XCO2, XCO2PREC, year, month, day, jd, fmt = variables()

    date_list = calendar_days(start, end)
    links = generate_links(date_list)
    download(links, downloaded_data_path)

    if downloaded_data_path is None:
        downloaded_data_path = join(getcwd(), "downloaded_data")

    path = glob(join(downloaded_data_path, "*.nc4"))

    for file_path in path:
        xco2_netCDF4 = xr.open_dataset(file_path)
        file_date = pd.to_datetime(str(xco2_netCDF4['time'].begin_date))

        if not (pd.to_datetime(start) <= file_date <= pd.to_datetime(end)):
            continue

        for k, v in kwargs.items():
            if len(v) < 2:
                raise ValueError(f"Location data for {k} is incomplete. incomplete: {v}")

            location.append(k)
            lat.append(v[0])
            lon.append(v[1])

            file_date = pd.to_datetime(str(xco2_netCDF4['time'].begin_date))
            year.append(file_date.year)
            month.append(file_date.month)
            day.append(file_date.day)
            jd.append(file_date.timetuple().tm_yday)

            lat_grid.append(xco2_netCDF4['lat'].sel(lat=v[0], method='nearest').values)
            lon_grid.append(xco2_netCDF4['lon'].sel(lon=v[1], method='nearest').values)

            try:
                XCO2.append(xco2_netCDF4['XCO2'].sel(lat=v[0], lon=v[1], method='nearest').values * 10 ** 6)
            except IndexError:
                XCO2.append(nan)

            if 'XCO2PREC' in xco2_netCDF4.variables:
                try:
                    XCO2PREC.append(xco2_netCDF4['XCO2PREC'].sel(lat=v[0], lon=v[1], method='nearest').values)
                except IndexError:
                    XCO2PREC.append(nan)
            else:
                XCO2PREC.append(nan)

    dataframe = make_dataframe(location, jd, day, month, year, lat, lon, lat_grid, lon_grid, XCO2, XCO2PREC)

    if missing_data:
        new_subset(dataframe)

    dataframe.set_index('location', inplace=True, drop=True)
    dataframe = dataframe.astype(float)
    dataframe.reset_index(inplace=True, drop=False)

    # Create directory called 'outputs' to save the dataframe
    output_dir = join(getcwd(), "outputs")
    makedirs(output_dir, exist_ok=True)
    path_save = join(output_dir, "XCO2_data.csv")
    dataframe.to_csv(path_save, index=False)

    return dataframe

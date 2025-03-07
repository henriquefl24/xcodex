from glob import glob
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


def xco2_extract(start: str, end: str, missing_data=False, downloaded_data_path=None, method="requests",**kwargs: dict) -> pd.DataFrame:
    """
    This method extracts XCO2 data from the specified date range and locations.
    :param start: Start date in the format "DD of Month, YYYY"
    :param end: End date in the format "DD of Month, YYYY"
    :param missing_data: Fill missing data if True
    :param downloaded_data_path: Path to the directory where the downloaded files are saved
    :param method: Method to use for downloading the files. Options are "requests" and "aria2c"
    :param kwargs: Dictionary of locations with latitude and longitude
    :return: DataFrame with extracted data
    """
    # Initialize variables
    (location, lat, lat_grid, lon, lon_grid, XCO2, XCO2PREC, year, month, day, jd, fmt) = variables()

    # Generate a list of dates between the start and end dates
    date_list = calendar_days(start, end)

    # Generate download links for the specified date range
    links = generate_links(date_list)

    # Download the data
    download(links, downloaded_data_path, method)

    # If downloaded data path is not provided, use "downloaded_data" directory in current working directory as default
    if downloaded_data_path is None:
        downloaded_data_path = join(getcwd(), "downloaded_data")

        # Get all the .nc4 files in the directory
    path = glob(join(downloaded_data_path, "*.nc4"))

    # Iterate through the .nc4 files
    for file_path in path:

        # Open the .nc4 file
        xco2_netCDF4 = xr.open_dataset(file_path)

        # Get the date of the file
        file_date = pd.to_datetime(str(xco2_netCDF4['time'].begin_date))

        # Continue with the next iteration if file date is not within specified date range
        if not (pd.to_datetime(start) <= file_date <= pd.to_datetime(end)):
            continue

        # Iterate through the locations
        for k, v in kwargs.items():

            # Raise error if latitude and longitude of location are not provided
            if len(v) < 2:
                raise ValueError(f"Location data for {k} is incomplete. incomplete: {v}")

            # Append location data
            location.append(k)
            lat.append(v[0])
            lon.append(v[1])

            # Get file date again and append date information
            file_date = pd.to_datetime(str(xco2_netCDF4['time'].begin_date))
            year.append(file_date.year)
            month.append(file_date.month)
            day.append(file_date.day)
            jd.append(file_date.timetuple().tm_yday)

            # Append lat and lon grid values
            lat_grid.append(xco2_netCDF4['lat'].sel(lat=v[0], method='nearest').values)
            lon_grid.append(xco2_netCDF4['lon'].sel(lon=v[1], method='nearest').values)

            # Try to append XCO2 value, append NaN if not available
            try:
                XCO2.append(xco2_netCDF4['XCO2'].sel(lat=v[0], lon=v[1], method='nearest').values * 10 ** 6)
            except IndexError:
                XCO2.append(nan)

            # Check if the XCO2PREC variable is available
            if 'XCO2PREC' in xco2_netCDF4.variables:
                # Try to append XCO2PREC value, append NaN if not available
                try:
                    XCO2PREC.append(xco2_netCDF4['XCO2PREC'].sel(lat=v[0], lon=v[1], method='nearest').values)
                except IndexError:
                    XCO2PREC.append(nan)
            else:
                XCO2PREC.append(nan)

    # Create a DataFrame from the extracted data
    dataframe = make_dataframe(location, jd, day, month, year, lat, lon, lat_grid, lon_grid, XCO2, XCO2PREC)

    # Fill missing data if required
    if missing_data:
        new_subset(dataframe)

    # Set dataframe index to location
    dataframe.set_index('location', inplace=True, drop=True)
    dataframe = dataframe.astype(float)
    dataframe.reset_index(inplace=True, drop=False)

    # Save dataframe to csv in `outputs` directory
    output_dir = join(getcwd(), "outputs")
    makedirs(output_dir, exist_ok=True)
    path_save = join(output_dir, "XCO2_data.csv")
    dataframe.to_csv(path_save, index=False)

    # Return dataframe
    return dataframe

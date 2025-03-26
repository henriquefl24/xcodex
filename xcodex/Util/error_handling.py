import os
from datetime import datetime

def validate_inputs(start: str, end: str, downloaded_data_path: str, method: str, output_format: str,
                    display_variables: list,**kwargs: dict):
    """
    Validate the inputs for the xco2_extract function.
    :param start: Start date in the format "DD of Month, YYYY"
    :param end: End date in the format "DD of Month, YYYY"
    :param downloaded_data_path: Path to the directory where the downloaded files are saved
    :param method: Method to use for downloading the files. Options are "requests" and "aria2c"
    :param output_format: Format to save the output file. Options are "csv", "excel", "json", "parquet", and "hdf5"
    :param display_variables: List of variables to display in the final DataFrame
    :param kwargs: Dictionary of locations with latitude and longitude
    :return: None
    """
    # Validate start and end dates
    try:
        start_date = datetime.strptime(start, "%d of %B, %Y")
    except ValueError:
        raise ValueError(f"Start date '{start}' does not match format 'DD of Month, YYYY'")

    try:
        end_date = datetime.strptime(end, "%d of %B, %Y")
    except ValueError:
        raise ValueError(f"End date '{end}' does not match format 'DD of Month, YYYY'")

    if start_date > end_date:
        raise ValueError("Start date must be before end date")

    # Validate downloaded_data_path
    if downloaded_data_path is not None and not os.path.isdir(downloaded_data_path):
        raise ValueError(f"Downloaded data path '{downloaded_data_path}' is not a valid directory")

    # Validate method
    if method not in ["requests", "aria2c"]:
        raise ValueError(f"Method '{method}' is not valid. Options are 'requests' and 'aria2c'")

    # Validate output_format
    if output_format not in ["csv", "excel", "json", "parquet", "hdf5"]:
        raise ValueError(f"Output format '{output_format}' is not valid. Options are 'csv', 'excel', 'json', 'parquet', and 'hdf5'")

    # Validate display_variables
    valid_variables = ['location', 'lat', 'lon', 'lat_grid', 'lon_grid', 'XCO2', 'XCO2PREC', 'year', 'month', 'day', 'jd']
    if display_variables is not None:
        for var in display_variables:
            if var not in valid_variables:
                raise ValueError(f"Display variable '{var}' is not valid. Options are {valid_variables}")

    # Validate kwargs
    for k, v in kwargs.items():
        if not isinstance(v, (list, tuple)) or len(v) != 2:
            raise ValueError(f"Location data for '{k}' is invalid. It must be a list or tuple with two elements (latitude and longitude)")

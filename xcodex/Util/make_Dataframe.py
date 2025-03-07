from pandas import DataFrame


def make_dataframe(location, jd, day, month, year, lat, lon, lat_grid, lon_grid, XCO2, XCO2PREC) -> DataFrame:
    """
    This method will create the output dataframe
    Args:
        location: Pandas series
        jd: Pandas series
        day: Pandas series
        month: Pandas series
        year: Pandas series
        lat: Pandas series
        lon: Pandas series
        lat_grid: Pandas series
        lon_grid: Pandas series
        XCO2: Pandas series
        XCO2PREC: Pandas series

    Returns: Dataframe

    """

    dataframe = DataFrame()

    # Assigning List Values to the Dataframe

    dataframe['location'] = location
    dataframe['jd'] = jd
    dataframe['day'] = day
    dataframe['month'] = month
    dataframe['year'] = year
    dataframe['lat'] = lat
    dataframe['lon'] = lon
    dataframe['lat_grid'] = lat_grid
    dataframe['lon_grid'] = lon_grid
    dataframe['XCO2'] = XCO2
    dataframe['XCO2PREC'] = XCO2PREC

    # Organizing the dataframe

    dataframe.sort_values(by=['location', 'year'], inplace=True)
    dataframe.reset_index(inplace=True, drop=True)

    return dataframe

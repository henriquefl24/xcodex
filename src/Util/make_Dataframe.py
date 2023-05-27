from pandas import DataFrame


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

    dataframe['city'] = city
    dataframe['jd'] = jd
    dataframe['day'] = day
    dataframe['month'] = month
    dataframe['year'] = year
    dataframe['lat'] = lat
    dataframe['lon'] = lon
    dataframe['lat_index'] = lat_index
    dataframe['lon_index'] = lon_index
    dataframe['xco2'] = XCO2_values
    dataframe['xco2_prec'] = XCO2PREC_values

    # Organizing the dataframe

    dataframe.sort_values(by=['city', 'year'], inplace=True)
    dataframe.reset_index(inplace=True, drop=True)

    return dataframe

def make_df(city, jd, day, month, year, lat, lon, lat_index, lon_index, XCO2_values, XCO2PREC_values):
    from pandas import DataFrame

    df = DataFrame()

    # Assigning List Values to the Dataframe

    df['city'] = city
    df['jd'] = jd
    df['day'] = day
    df['month'] = month
    df['year'] = year
    df['lat'] = lat
    df['lon'] = lon
    df['lat_index'] = lat_index
    df['lon_index'] = lon_index
    df['xco2'] = XCO2_values
    df['xco2_prec'] = XCO2PREC_values

    # Organizing the dataframe

    df.sort_values(by=['city', 'year'], inplace=True)
    df.reset_index(inplace=True, drop=True)

    # Padronizing values to float

    df.set_index('city', inplace=True, drop=True)
    df = df.astype(float)
    df.reset_index(inplace=True, drop=False)

    return df

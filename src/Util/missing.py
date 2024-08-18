from pandas import DataFrame


def new_subset(dataframe: DataFrame) -> None:
    """
    Creating a new_subset.txt based on the NaN values of the main DataFrame.
    The file will be saved on the current folder of the user
    :dataframe: Pandas.DataFrame. Takes the xco2_extract dataframe to identificate the NaN values.
    :return: None
    """
    dataframe = dataframe.loc[dataframe['XCO2'].isna()]
    dataframe.reset_index(inplace=True , drop=True)

    links_list = []
    for _, row in dataframe.iterrows():
        year = str(row.iloc[4])
        month = str(row.iloc[3]).zfill(2)
        day = str(row.iloc[2]).zfill(2)

        link = f"https://oco2.gesdisc.eosdis.nasa.gov/data/OCO2_DATA/OCO2_GEOS_L3CO2_DAY.10r/{year}/oco2_GEOS_L3CO2_day_{year}{month}{day}_B10206Ar.nc4"
        links_list.append(link)

    unique_links = list(set(links_list))

    with open('../new_subset.txt', 'w') as f:
        f.write('\n'.join(unique_links))

    print(f"Number of missing days: {len(dataframe)}"
          f"\nNew subset created")

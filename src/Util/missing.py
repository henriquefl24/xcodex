def new_subset(dataframe):
    from pandas import isna
    from os import remove

    dataframe = dataframe.loc[isna(dataframe.xco2)]
    dataframe.reset_index(inplace=True, drop=True)

    with open('outfile.txt', 'w') as f:
        for c in range(len(dataframe)):

            # These conditionals have the finality to concatenate strings to
            # create a new subset in the correct order

            if dataframe.iloc[:, 3][c] < '10':  # Month < 10
                if dataframe.iloc[:, 2][c] < '10':  # Day < 10
                    f.write("https://oco2.gesdisc.eosdis.nasa.gov/data/OCO2_DATA/OCO2_GEOS_L3CO2_DAY.10r/" +
                            str(dataframe.iloc[:, 4][0])[0:4] + "/oco2_GEOS_L3CO2_day_" +
                            str(dataframe.iloc[:, 4][0])[0:4] + "0" +
                            str(dataframe.iloc[:, 3][c])[0] + "0" +
                            str(dataframe.iloc[:, 2][c]) + "_B10206Ar.nc4\n")
                elif dataframe.iloc[:, 2][c] >= '10':  # Day >= 10
                    f.write("https://oco2.gesdisc.eosdis.nasa.gov/data/OCO2_DATA/OCO2_GEOS_L3CO2_DAY.10r/" +
                            str(dataframe.iloc[:, 4][c])[0:4] + "/oco2_GEOS_L3CO2_day_" +
                            str(dataframe.iloc[:, 4][c])[0:4] + "0" +
                            str(dataframe.iloc[:, 3][c])[0] +
                            str(dataframe.iloc[:, 2][c]) + "_B10206Ar.nc4\n")

            if dataframe.iloc[:, 3][c] >= '10':  # Month >=10
                if dataframe.iloc[:, 2][c] < '10':  # Day < 10
                    f.write("https://oco2.gesdisc.eosdis.nasa.gov/data/OCO2_DATA/OCO2_GEOS_L3CO2_DAY.10r/" +
                            str(dataframe.iloc[:, 4][0])[0:4] + "/oco2_GEOS_L3CO2_day_" +
                            str(dataframe.iloc[:, 4][0])[0:4] +
                            str(dataframe.iloc[:, 3][c])[0:2] + "0" +
                            str(dataframe.iloc[:, 2][c]) + "_B10206Ar.nc4\n")
                elif dataframe.iloc[:, 2][c] >= '10':  # Day >= 10
                    f.write("https://oco2.gesdisc.eosdis.nasa.gov/data/OCO2_DATA/OCO2_GEOS_L3CO2_DAY.10r/" +
                            str(dataframe.iloc[:, 4][0])[0:4] + "/oco2_GEOS_L3CO2_day_" +
                            str(dataframe.iloc[:, 4][0])[0:4] +
                            str(dataframe.iloc[:, 3][c])[0:2] +
                            str(dataframe.iloc[:, 2][c]) + "_B10206Ar.nc4\n")

    f.close()

    lines_seen = set()  # holds lines already seen
    outfile = open('../new_subset.txt', "w")

    for line in open('outfile.txt', "r"):
        if line not in lines_seen:  # not a duplicate
            outfile.write(line)
            lines_seen.add(line)

    remove('outfile.txt')
    f.close()

    print(f"Number of missing days: {len(dataframe)}"
          f"\nNew subset created")


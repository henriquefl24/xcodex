def new_subset(df):
    from pandas import isna
    from os import remove

    df = df.loc[isna(df.xco2)]
    df.reset_index(inplace=True, drop=True)

    with open('outfile.txt', 'w') as f:
        for c in range(len(df)):

            # These conditionals have the finality to concatenate strings to
            # create a new subset in the correct order

            if int(df.iloc[:, 3][c]) < 10:
                if int(df.iloc[:, 2][c]) < 10:
                    f.write("https://oco2.gesdisc.eosdis.nasa.gov/data/OCO2_DATA/OCO2_GEOS_L3CO2_DAY.10r/" +
                            df.iloc[:, 4][c] + "/oco2_GEOS_L3CO2_day_" + df.iloc[:, 4][c] + "0" +
                            df.iloc[:, 3][c] + "0" + df.iloc[:, 2][c] + "_B10206Ar.nc4\n")
                elif len(df.iloc[:, 2][c]) >= 2:
                    f.write("https://oco2.gesdisc.eosdis.nasa.gov/data/OCO2_DATA/OCO2_GEOS_L3CO2_DAY.10r/" +
                            df.iloc[:, 4][c] + "/oco2_GEOS_L3CO2_day_" + df.iloc[:, 4][c] + "0" +
                            df.iloc[:, 3][c] + df.iloc[:, 2][c] + "_B10206Ar.nc4\n")

            if int(df.iloc[:, 3][c]) >= 10:
                if int(df.iloc[:, 2][c]) < 10:
                    f.write("https://oco2.gesdisc.eosdis.nasa.gov/data/OCO2_DATA/OCO2_GEOS_L3CO2_DAY.10r/" +
                            df.iloc[:, 4][c] + "/oco2_GEOS_L3CO2_day_" + df.iloc[:, 4][c] + df.iloc[:, 3][
                                c] + "0" + df.iloc[:, 2][c] + "_B10206Ar.nc4\n")
                elif len(df.iloc[:, 2][c]) >= 2:
                    f.write("https://oco2.gesdisc.eosdis.nasa.gov/data/OCO2_DATA/OCO2_GEOS_L3CO2_DAY.10r/" +
                            df.iloc[:, 4][c] + "/oco2_GEOS_L3CO2_day_" + df.iloc[:, 4][c] + df.iloc[:, 3][
                                c] + df.iloc[:, 2][c] + "_B10206Ar.nc4\n")

    f.close()

    lines_seen = set()  # holds lines already seen
    outfile = open('new_subset.txt', "w")

    for line in open('outfile.txt', "r"):
        if line not in lines_seen:  # not a duplicate
            outfile.write(line)
            lines_seen.add(line)

    remove('outfile.txt')
    f.close()

    return print('New subset created')

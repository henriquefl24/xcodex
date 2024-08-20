def generate_links(calendar_list: list):
    """
    This method generates downloadable links based on the calendar dates.
    """
    links_list = []
    for date in calendar_list:
        year_from_calendar = str(date.year)
        month_from_calendar = str(date.month).zfill(2)
        day_from_calendar = str(date.day).zfill(2)

        link = ("https://oco2.gesdisc.eosdis.nasa.gov/data/OCO2_DATA/OCO2_GEOS_L3CO2_DAY.10r/" +
                year_from_calendar + "/oco2_GEOS_L3CO2_day_" + year_from_calendar + month_from_calendar +
                day_from_calendar + "_B10206Ar.nc4")

        links_list.append(link)

    return links_list

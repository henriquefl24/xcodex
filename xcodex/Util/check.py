from netCDF4 import Dataset


def check_date(calendar_list, xco2_netCDF4: Dataset) -> bool:
    """
    This routine will check if the calendar year matches with the current file
    """
    try:
        begin_date = str(xco2_netCDF4['time'].begin_date)
        year = int(begin_date[0:4])
        month = int(begin_date[4:6].lstrip("0"))
        day = int(begin_date[6:].lstrip("0"))
    except (ValueError, IndexError):
        return False

    for date in calendar_list:
        if date.year > year:
            return False
        elif date.year == year:
            if date.month > month:
                return False
            elif date.month == month:
                if date.day > day:
                    return False
    return True

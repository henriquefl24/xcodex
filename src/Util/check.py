from netCDF4 import Dataset
def check_date(calendar_list:list, xco2_netCDF4:Dataset)->bool:
    """
    This routine will check if the calendar year matches with the current file
    """

    if str(calendar_list.year[0]) > str(xco2_netCDF4['time'].begin_date)[0:4]:
        flag = True

    else:
        if str(calendar_list.month[0]) > str(xco2_netCDF4['time'].begin_date)[4:6].lstrip("0"):
            flag = True
        else:
            if str(calendar_list.day[0]) > str(xco2_netCDF4['time'].begin_date)[6:].lstrip("0"):
                flag = True
            else:
                flag = False

    return flag

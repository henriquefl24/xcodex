def calendar_days(start: str, end: int):
    """
    This method will create a union of calendar dates for further comparison.
    The main advantage of this method is to consider the leap years.
    :param start: str: i.e.: "1st of january, 2015"
    :param end: int: i.e.: 365 days
    :return: Union of calendar days. 01/01/2015 to 01/01/2016
    """
    from pandas import to_datetime, to_timedelta
    from numpy import arange

    date = to_datetime(start)  # Defines the start date of data collection

    calendar_list = date + to_timedelta(arange(end), "D")

    return calendar_list

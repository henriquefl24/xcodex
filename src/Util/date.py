def calendar_days(start: str, end: str):
    """
    This method will create a union of calendar dates for further comparison.
    The main advantage of this method is to consider the leap years.
    :param start: str: i.e.: "1st of january, 2015"
    :param end: str: i.e.: "31st of january, 2015"
    :return: Union of calendar days. 01/01/2015 to 01/01/2016
    """
    from pandas import to_datetime, date_range

    start_date = to_datetime(start)  # Defines the start date of data collection
    end_date = to_datetime(end)  # Defines the end date of data collection

    calendar_list = date_range(start_date, end_date)

    return calendar_list


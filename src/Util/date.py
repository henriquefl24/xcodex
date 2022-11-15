def calendar_days(start, end):

    from pandas import to_datetime, to_timedelta
    from numpy import arange

    date = to_datetime(start)  # Defines the start date of data collection

    calendar_list = date + to_timedelta(arange(end), "D")

    return calendar_list

from collections import deque
from typing import Any


def variables() -> tuple[
    deque[Any], deque[Any], deque[Any], deque[Any], deque[Any], deque[Any], deque[Any], deque[Any], deque[Any], deque[
        Any], deque[Any], deque[Any], deque[Any], deque[Any], str]:
    """
    This method will pack all the variables used in the main method xco2_extract()
    along with the format

    :return: packed deque()
    """

    city = deque()
    lat = deque()
    lon = deque()
    lat_index = deque()
    lon_index = deque()
    XCO2_values = deque()
    XCO2PREC_values = deque()
    year = deque()
    month = deque()
    day = deque()
    jd = deque()
    day_test = deque()
    month_test = deque()
    year_test = deque()

    fmt = r'%Y-%m-%d %H:%M:%S'

    return city, lat, lat_index, lon, lon_index, XCO2_values, XCO2PREC_values, year, year_test, month, month_test, day, day_test, jd, fmt

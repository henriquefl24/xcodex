from collections import deque
from typing import Any


def variables() -> tuple[
    deque[Any], deque[Any], deque[Any], deque[Any], deque[Any], deque[Any], deque[Any], deque[Any], deque[Any], deque[
        Any], deque[Any], str]:
    """
    This method will pack all the variables used in the main method xco2_extract()
    along with the format

    :return: packed deque()
    """
    location = deque()
    lat = deque()
    lat_grid = deque()
    lon = deque()
    lon_grid = deque()
    XCO2 = deque()
    XCO2PREC = deque()
    year = deque()
    month = deque()
    day = deque()
    jd = deque()

    fmt = r'%Y-%m-%d %H:%M:%S'

    return location, lat, lat_grid, lon, lon_grid, XCO2, XCO2PREC, year, month, day, jd, fmt

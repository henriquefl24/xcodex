def download_file(start: str, end: int) -> None:
    """
    This method will effectively download .nc4 files from NASA
    Args:
        start: start date (i.e.: "1st of January, 2015")
        end: amount of days (i.e.: 365 days)

    Returns: None
    """
    from Util.date import calendar_days
    from Util.generate_links import generate_links
    from Util.download import download

    date_list = calendar_days(start, end)
    links = generate_links(date_list)
    download(links)

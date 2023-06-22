def monitor_social_media(sources, interval):
    """
    Fetch social media data from multiple sources.

    Parameters:
    sources : list
        A list of social media sources.
    interval : int
        The scrape interval in seconds.

    Returns:
    list of pandas.DataFrame
        A list of DataFrames, each representing data from a source.
    """
    social_media_data = []
    for source in sources:
        data = monitor_source(source, interval)  # assuming monitor_source fetches data from a source
        social_media_data.append(data)
    
    return social_media_data

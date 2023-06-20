def shorten(text, limit = 80):
    """Shortens text"""
    indicator = ".."
    limit -= len(indicator)
    return text[:limit] + (text[limit:] and indicator)
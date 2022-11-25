def shorten(text, limit = 80):
    """Shortens text"""
    return text[:limit] + (text[limit:] and '..')
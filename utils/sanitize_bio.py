def sanitize_bio(bio: str) -> str:
    """
    Removes line breakers
    """
    return bio.replace("\r", "")
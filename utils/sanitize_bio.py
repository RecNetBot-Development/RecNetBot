def sanitize_bio(bio: str) -> str:
    """
    Removes breaking characters
    """

    # Removes line breakers
    bio = bio.replace("\r", "")

    # Removes ` so they don't break the embed
    bio = bio.replace("`", "")

    return bio
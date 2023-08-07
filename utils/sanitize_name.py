def sanitize_name(bio: str) -> str:
    """
    Removes breaking characters
    """

    # Removes line breakers
    bio = bio.replace("_", "\_")

    return bio
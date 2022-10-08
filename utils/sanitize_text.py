def sanitize_text(text: str) -> str:
    """
    Prevents Discord from formatting text
    """
    
    return text.replace("_", "\_").replace("*", "\*").replace("`", "\`").replace("~", "\~`")
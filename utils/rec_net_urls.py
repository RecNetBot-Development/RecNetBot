# So I don't need to write the url's in every use-case.
# Also, it's easier to change if needed

def img_url(image_name: str, crop_square: bool=False, resolution: int=720, raw: bool=False) -> str:
    """
    https://img.rec.net/{image_name}?width={resolution}&{'cropSquare=true&' if crop_square else ''}
    """
    if raw: return f"https://img.rec.net/{image_name}"
    return f"https://img.rec.net/{image_name}?width={resolution}&{'cropSquare=true&' if crop_square else ''}"

def post_url(post_id: int) -> str: 
    """
    https://rec.net/image/{post_id}
    """
    return f"https://rec.net/image/{post_id}"

def profile_url(username: str) -> str: 
    """
    https://rec.net/user/{username}
    """
    return f"https://rec.net/user/{username}"

def room_url(room_name: str) -> str:
    """
    https://rec.net/room/{room_name}
    """
    return f"https://rec.net/room/{room_name}"

def event_url(event_id: int) -> str:
    """
    https://rec.net/event/{event_id}
    """
    return f"https://rec.net/event/{event_id}"

def invention_url(invention_id: int) -> str:
    """
    https://rec.net/invention/{invention_id}
    """
    return f"https://rec.net/invention/{invention_id}"

def profile_posts_url(username: str) -> str: 
    """
    https://rec.net/user/{username}/photos
    """
    return f"https://rec.net/user/{username}/photos"
# So I don't need to write the url's in every use-case.
# Also, it's easier to change if needed

def img_url(image_name: str, crop_square: bool=False, resolution: int=720):
    return f"https://img.rec.net/{image_name}?width={resolution}&{'cropSquare=true&' if crop_square else ''}"

def post_url(post_id: int): 
    return f"https://rec.net/image/{post_id}"

def profile_url(username: str): 
    return f"https://rec.net/user/{username}"

def room_url(room_name: str):
    return f"https://rec.net/room/{room_name}"

def event_url(event_id: int):
    return f"https://rec.net/event/{event_id}"
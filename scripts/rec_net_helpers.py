def img_url(image_name: str, crop_square: bool=False, resolution: int=720):
    return f"https://img.rec.net/{image_name}?width={resolution}&{'cropSquare=true&' if crop_square else ''}"
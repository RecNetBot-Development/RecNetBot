from ..emojis import Emoji
from .resolve_platforms import resolve_platforms

def create_platforms_section(platform_mask: int = None, platform_names: list = None):
    platform_info = {
        'Steam': f'{Emoji.steam} [`Steam`](https://store.steampowered.com/app/471710/Rec_Room/)', 
        'Oculus': f'{Emoji.oculus} [`Oculus`](https://www.oculus.com/experiences/quest/2173678582678296/)', 
        'PlayStation': f'{Emoji.playstation} [`PlayStation`](https://store.playstation.com/en-us/product/EP2526-CUSA09539_00-RECROOM000000001)', 
        'Xbox': f'{Emoji.xbox} [`Xbox`](https://www.xbox.com/en-ZA/games/store/rec-room/9pgpqk0xthrz)',
        'iOS': f'{Emoji.ios} [`iOS`](https://apps.apple.com/us/app/rec-room/id1450306065)', 
        'Android': f'{Emoji.android} [`Android`](https://play.google.com/store/apps/details?id=com.AgainstGravity.RecRoom)'
    }
    
    if platform_names:
        platforms = platform_names
    elif platform_mask:
        platforms = resolve_platforms(platform_mask)
    else:
        return
    
    platform_text_list = []
    for platform in platforms:
        platform_text_list.append(platform_info.get(platform, ""))
    return ', '.join(platform_text_list)
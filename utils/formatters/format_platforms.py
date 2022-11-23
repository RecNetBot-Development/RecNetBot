from typing import List
from resources import get_emoji

PLATFORM_URLS = {
    'steam': "https://store.steampowered.com/app/471710/Rec_Room/", 
    'meta': "https://www.oculus.com/experiences/quest/2173678582678296/", 
    'playstation': "https://store.playstation.com/en-us/product/UP2662-CUSA08481_00-RECROOM000000001", 
    'xbox': "https://www.xbox.com/en-ZA/games/store/rec-room/9pgpqk0xthrz",
    'ios': "https://apps.apple.com/us/app/rec-room/id1450306065", 
    'android': "https://play.google.com/store/apps/details?id=com.AgainstGravity.RecRoom",
    'standalone': "https://rec.net/download",
    'pico': "https://www.picoxr.com/"
}

def format_platforms(platforms: List[str]) -> List[str]:
    """
    Formats platforms in a nice manner that contains links and icons
    """
    print(platforms)
    
    if not platforms: return []
    formatted = []
    for ele in platforms:
        formatted.append(f"{get_emoji(ele)} [`{ele}`](<{PLATFORM_URLS.get(ele.lower(), 'https://rec.net/download')}>)")
        
    return formatted
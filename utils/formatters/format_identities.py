from typing import List
from resources import get_emoji

IDENTITY_INFO = {
    'LGBTQIA': get_emoji('lgbtq'), 
    'Transgender': get_emoji('transgender'), 
    'Bisexual': get_emoji('bisexual'), 
    'Lesbian': get_emoji('lesbian'), 
    'Pansexual': get_emoji('pansexual'), 
    'Asexual': get_emoji('asexual'), 
    'Intersex': get_emoji('intersex'), 
    'Genderqueer': get_emoji('genderqueer'), 
    'Nonbinary': get_emoji('nonbinary'), 
    'Aromantic': get_emoji('aromantic')
}

def format_identities(identities: List[str]) -> List[str]:
    """
    Formats identities in a nice manner that icons
    """
    
    if not identities: return []
    formatted = []
    for ele in identities:
        formatted.append(f"{IDENTITY_INFO.get(ele, get_emoji('unknown'))}\u00a0`{ele}`")
        
    return formatted
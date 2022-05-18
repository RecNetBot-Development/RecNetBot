from utility.emojis import get_emoji


def create_identity_section(identity_list):
    if not identity_list: return None
    
    identity_info = {
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

    identities = []
    for identity in identity_list:
        identities.append(f"{identity_info.get(identity, get_emoji('unknown'))} `{identity}`")
        
    return ' '.join(identities)
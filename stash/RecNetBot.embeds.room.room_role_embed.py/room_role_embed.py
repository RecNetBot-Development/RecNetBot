import profile
from embeds.base.embed import DefaultEmbed as Embed
from utility.emojis import get_emoji, get_icon
from utility.rec_net_helpers import room_url, profile_url
from embeds.headers.room_header import room_header

def room_role_embed(room):
    # Map out users with roles
    co_owners, dev_co_owners, moderators, hosts, unknown = [], [], [], [], []
    for user in room.roles:
        match user.role:
            case "owner":
                continue
            case "co-owner":
                co_owners.append(user)
            case "dev_co-owner":
                dev_co_owners.append(user)
            case "moderator":
                moderators.append(user)
            case "host":
                hosts.append(user)
            case _:
                unknown.append(user)
         
    em = Embed(
        title=f"Roles",
        description = 
        f"Owner: [`@{room.creator.username}` ({room.creator.display_name})]({profile_url(room.creator.username)})\n"
        f"Co-Owners: `{len(co_owners)}`\n"
        f"Dev Co-Owners: `{len(dev_co_owners)}`\n"
        f"Moderators: `{len(moderators)}`\n"
        f"Hosts: `{len(hosts)}`\n"
        f"Unknown: `{len(unknown)}`"
    )
    
    #if co_owners:
        #em.add_field(name=f"Co-Owners ({len(co_owners)})")
    
    em = room_header(room, em)
    
    return em
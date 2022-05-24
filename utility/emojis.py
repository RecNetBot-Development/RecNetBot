"""Emojis for RNB to use."""
class Emoji:
    # General
    cheer = "<:cheer:962027534747312168>"  # Room cheer, post cheer
    date = "<:date:962027535120625755>"  # Something created at (Time by Trident from NounProject.com)
    correct = "✅"  # "True"
    incorrect = "❌"  # "False"
    unknown = "<:unknown:962799809088086036>"  # "Unknown by Adrien Coquet from NounProject.com"
    link = "<:link:978703397035315230>" # Link by Тимур Минвалеев from NounProject.com
    default_link = "🔗"
    
    # Platforms
    walk = "<:walking:962792336725782608>"  # Walk locomotion icon  (Walking by Vectors Market from NounProject.com)
    teleport = "<:teleport:962728192026767361>"  # Teleport locomotion icon
    quest1 = "<:q1:962793550083420221>"  # Quest 1 icon
    quest2 = "<:q2:962793550234411089>"  # Quest 2 icon
    mobile = "<:mobile:962726376820047943>"  # General mobile icon (Phone by andriwidodo from NounProject.com)
    junior = "<:junior:962728467055669278>"  # Junior icon (Pacifier by Danishicon from NounProject.com)
    screen = "<:screen:962725264209629205>"  # Screenie icon (Screen by DinosoftLab from NounProject.com  )
    oculus = "<:oculus:962812488552939530>"  # Oculus icon
    playstation = "<:playstation:962813043094462556>"  # PlayStation icon
    steam = "<:steam:962810906478260264>"  # Steam icon
    xbox = "<:xbox:962813430761406464>"  # Xbox icon
    android = "<:android:962815093626785883>"  # Android icon
    ios = "<:apple:962815516127424532>"  # iOS icon
    
    # Profile Embed
    level = "<:level:962027535007354901>"  # Account level (Star by Elvn Sands from NounProject.com)
    subscribers = "<:subscribers:962027535095439371>"  # Account subscribers (Group Of People by Icon Box from NounProject.com)
    controller = "<:platforms:962027535053504633>"  # Account platforms (Controller by iconfield from NounProject.com)
    pronouns = "<:comment:962027534856359936>"
    identities = "<:flag:962804152319230043>" # (Flag by Melvin Poppelaars from NounProject.com)
    username = "<:id:962807935711465543>" # Id by Rockicon from NounProject.com
    
    # Image Embed
    comment = "<:comment:962027534856359936>"  # Image comments (Comment by Larea from NounProject.com)
    event = "<:event:962027535049293865>"  # Image taken during event (Event by Jugalbandi from NounProject.com)
    room = "<:room:962027535196098570>"  # Image room  (Compass by IronSV from NounProject.com)
    tagged = "<:tagged:962027535305146408>" # Image tagged (People by Doub.co from NounProject.com)
    image = "<:image:962808860433870998>" # Images by YANDI RS from NounProject.com
    
    # Room Embed
    hot = "<:hot:962723832643321876>"  # Room's hot placement (Fire by Diego Naive from NounProject.com)
    engagement = "<:trending:962724318037569686>"  # Room engagement (Trend by Adriansyah from NounProject.com)
    tag = "<:tag:962723300654600202>"  # Room tags (Tag by Julynn B. from NounProject.com)
    visitor = "<:visitor:962793028026777640>"  # Visitor (People by Adrien Coquet from NounProject.com)
    visitors = "<:visitors:962793039397552220>"  # Visitors (People by Adrien Coquet from NounProject.com)
    favorite = "<:level:962027535007354901>"  # Favorites (Star by Elvn Sands from NounProject.com)
    subrooms = "<:subrooms:962794308128354395>"  # Subrooms (Rooms by Smalllike from NounProject.com)
    limit = "<:subscribers:962027535095439371>"  # Player limit (Group Of People by Icon Box from NounProject.com)
        
    # Help Embed
    discord = "<:discord:963430619684163644>"
    questions = comment
    stats = engagement
    information = "<:info:963877676337201224>"  # (Info by rosannavergara5@gmail.com from NounProject.com)
    github = "<:github:963428573476192356>"
    
    category_api = "<:category_api:963878518960291903>"  # (Api by Larea from NounProject.com)
    category_event = event
    category_help = "<:category_help:963878068378800268>"  # (Help by Cayner Curitana from NounProject.com)
    category_image = image
    category_misc = "<:category_misc:963877141936746507>"  # (Other by Adrien Coquet from NounProject.com)
    category_random = "<:category_random:963876641883431013>"  # (Random by Ananth from NounProject.com)
    category_room = room
    category_user = visitor
        
    # Room Warnings
    spooky = "<:spooky:962798979509280838>"  # Spooky warning (Ghost by Andres Flores from NounProject.com)
    mature = "<:mature:962796110575964202>"  # Mature warning
    bright = "<:brightness:962796571710357615>"  # Bright lights warning (Brightness by Chinnaking from NounProject.com)
    motion = "<:motion:962799369134940210>"  # Fast motion warning (Roller Coaster Ride by Jose Dean from NounProject.com)
    gore = "<:gore:962797997387821136>" # Gore warning (Skull by James Smith from NounProject.com)
    
    # Image Browser
    next_bulk = "<:next_bulk:962044459913195540>" # (Arrow by iconix user from NounProject.com)
    prev_bulk = "<:prev_bulk:962044459904815204>" # (Arrow by iconix user from NounProject.com)
    next = "<:next:962044545418264646>" # (Arrow by Ghiyats Mujtaba from NounProject.com)
    prev = "<:prev:962044459867078677>" # (Arrow by Ghiyats Mujtaba from NounProject.com)
    first = "<:first:962045596930302033>" # (First by b farias from NounProject.com)
    last = "<:last:962045596783489034>" # (First by b farias from NounProject.com)
    random = "<:random:962046577936056421>" # (Random by Manohara from NounProject.com)
    
    # Identities
    aromantic = "<:aromantic:962801321768005702>"
    asexual = "<:asexual:962801321780596796>"
    bisexual = "<:bisexual:962801321830916096>"
    genderqueer = "<:genderqueer:962801321432477838>"
    lesbian = "<:lesbian:962801322267148308>"
    lgbtq = "<:lgbtq:962801321877078117>"
    nonbinary = "<:nonbinary:962801322241982594>"
    pansexual = "<:pansexual:962801321570877491>"
    transgender = "<:transgender:962801321990320238>"
    intersex = "<:intersex:962801322124521633>"

def get_emoji(emoji_name, client = None):
    if not emoji_name: return Emoji.unknown
    
    emoji = getattr(Emoji, emoji_name) if hasattr(Emoji, emoji_name) else Emoji.unknown
    
    if client and ":" in emoji:
        emoji_id = emoji.split(":")[-1].replace(">", "")
        if emoji_id.isdigit():
            return client.get_emoji(int(emoji_id))
    return emoji
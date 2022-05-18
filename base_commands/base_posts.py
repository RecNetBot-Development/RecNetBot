from utility import handle_filters
from rec_net.exceptions import APIFailure, AccountNotFound, NotFound, Error, RoomNotFound
from embeds import ImageUI

class Filter:
    def __init__(self, name, filter, readable_filter=None, handle=True):
        self.name = name
        handled_filters = handle_filters(filter) if handle else filter
        self.readable_filter = readable_filter if readable_filter else handled_filters
        self.filter = handled_filters

class MissingArguments(Error):
    """Raised when missing key arguments"""
    ...

async def base_posts(rec_net, ctx, type, username=None, sort=None, in_rooms=None, not_in_rooms=None, with_users=None, without_users=None, during_event=None, exclude_events=None, minimum_cheers=0, minimum_comments=0, raw=False):
    if not username and type == "Photos":
        raise MissingArguments("`username` argument is required for `/posts type:Photos`")
    if not with_users and not username and type == "Feed":
        raise MissingArguments("`username` OR `with_users` argument is required for `/posts type:Feed`")

    post_options = {
        "take": 2**16,
        #"includes": ["creator", "room"]           
    }

    async def get_user_and_posts(type, account, includes, options):
        if account.isdigit():
            user = await rec_net.account(id=int(account), includes=includes, options=options)
        else:
            user = await rec_net.account(name=account, includes=includes, options=options)
        
        if not user: raise AccountNotFound(account)
            
        return (user, user.posts) if type == "photos" else (user, user.feed)

    match type:
        case "Photos":
            includes = ["posts"]
            options = {"posts": post_options}
            user, posts = await get_user_and_posts("photos", username, includes, options)
        case "Feed":
            if username:
                account = username
            elif with_users:
                account = handle_filters(with_users)[0]
            includes = ["feed"]
            options = {"feed": post_options}
            user, posts = await get_user_and_posts("feed", account, includes, options)

    post_filter = {}
    if in_rooms:
        rooms = await rec_net.room(name=handle_filters(in_rooms))
        _in_rooms = [room.id for room in rooms]
        room_names = [room.name for room in rooms]
        post_filter["rooms"] = Filter("In room(s)", _in_rooms, room_names, False)
    if not_in_rooms: 
        rooms = await rec_net.room(name=handle_filters(not_in_rooms))
        _not_in_rooms = [room.id for room in rooms]
        room_names = [room.name for room in rooms]
        post_filter["not_rooms"] = Filter("Not in room(s)", _not_in_rooms, room_names, False)

    if with_users: 
        users = await rec_net.account(name=handle_filters(with_users))
        _with_users = [user.id for user in users]
        usernames = [user.username for user in users]
        post_filter["with_users"] = Filter("User(s) tagged", _with_users, usernames, False)
    if without_users: 
        users = await rec_net.account(name=handle_filters(without_users))
        _without_users = [user.id for user in users]
        usernames = [user.username for user in users]
        post_filter["without_users"] = Filter("User(s) not tagged", _without_users, usernames, False)
    
    if during_event: post_filter["during_event"] = Filter("During event", during_event, None, False)
    if exclude_events: post_filter["exclude_events"] = Filter("Not during event(s)", exclude_events, None)
    
    if minimum_cheers: post_filter["minimum_cheers"] = Filter("Minimum cheers", minimum_cheers, None, False)
    if minimum_comments: post_filter["minimum_comments"] = Filter("Minimum comments", minimum_comments, None, False)

    view, embeds = await ImageUI(ctx=ctx, user=user, posts=posts, raw=raw, post_filter=post_filter, interaction=ctx.interaction, sort=sort, rec_net=rec_net).start()
    return view, embeds


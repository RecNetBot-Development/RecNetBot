from ..funcs import date_to_unix

def filter_posts(posts, post_filter, sort):
    def room_filter(post):
        if post.room in post_filter["rooms"].filter:
            return True
        return False

    def exclude_room_filter(post):
        if post.room in post_filter["not_rooms"].filter:
            return False
        return True

    def tagged_filter(post):
        filter = post_filter["with_users"].filter
        for tag in filter:
            if int(tag) not in post.tagged: 
                return False
        return True
    
    def not_tagged_filter(post):
        filter = post_filter["without_users"].filter
        for tag in filter:
            if int(tag) in post.tagged: 
                return False
        return True

    def event_filter(post):
        filter = post_filter['during_event'].filter
        return post.event == filter

    def exclude_event_filter(post):
        filter = post_filter['exclude_events'].filter
        for event in filter:
            if int(event) == post.event: 
                return False
        return True

    def cheer_filter(post):
        filter = post_filter['minimum_cheers'].filter
        return post.cheer_count >= filter

    def comment_filter(post):
        filter = post_filter['minimum_comments'].filter
        return post.comment_count >= filter

    def bookmark_filter(post):
        for comment in post.comments:
            if "bookmark" in comment.comment:
                return True
        return False

    filtered_posts = posts
    
    def date_sort(post): return date_to_unix(post.created_at)
    def cheers_sort(post): return post.cheer_count
    def comments_sort(post): return post.comment_count
    match sort:
        case "Newest to Oldest":
            filtered_posts = filtered_posts.sort(key=date_sort, reverse=True)
        case "Oldest to Newest":
            filtered_posts = filtered_posts.sort(key=date_sort)
        case "Cheers: Highest to Lowest":
            filtered_posts = filtered_posts.sort(key=cheers_sort, reverse=True)
        case "Cheers: Lowest to Highest":
            filtered_posts = filtered_posts.sort(key=cheers_sort)
        case "Comments: Highest to Lowest":
            filtered_posts = filtered_posts.sort(key=comments_sort, reverse=True)
        case "Comments: Lowest to Highest":
            filtered_posts = filtered_posts.sort(key=comments_sort)
        case _:
            ...
        
    if not post_filter:  # Don't bother with anything if no filters set
        return posts

    filtered_posts = posts
    if "rooms" in post_filter:
        filtered_posts = filter(room_filter, filtered_posts)
    if "not_rooms" in post_filter:
        filtered_posts = filter(exclude_room_filter, filtered_posts)
    if "with_users" in post_filter:
        filtered_posts = filter(tagged_filter, filtered_posts)
    if "without_users" in post_filter:
        filtered_posts = filter(not_tagged_filter, filtered_posts)
    if "during_event" in post_filter:
        filtered_posts = filter(event_filter, filtered_posts)
    if "exclude_events" in post_filter:
        filtered_posts = filter(exclude_event_filter, filtered_posts)
    if "minimum_cheers" in post_filter:
        filtered_posts = filter(cheer_filter, filtered_posts)
    if "minimum_comments" in post_filter:
        filtered_posts = filter(comment_filter, filtered_posts)
    if "bookmarked" in post_filter:
        filtered_posts = filter(bookmark_filter, filtered_posts)

    return list(filtered_posts)

def handle_filters(filters):
    if type(filters) is not str: return [filters]
    pure_filters = list(filter(None, filters.split(" ")))
    return pure_filters
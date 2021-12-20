from ..base import Options

class AccountOptions(Options):
    def __init__(self, *args):
        super().__init__(*args)
        self.configurables = {
            "include_bio": self.manager.get_bio,
            "include_progress": self.manager.get_progress,
            "include_subs": self.manager.get_subscriber_count,
            "include_feed": self.manager.get_feed,
            "include_posts": self.manager.get_posts,
            "include_owned_rooms": self.manager.get_owned_rooms,
            "include_created_rooms": self.manager.get_created_rooms,
            "include_room_showcase": self.manager.get_room_showcase,
            "include_events": self.manager.get_events,
        }
import discord
from ....components.rec_net_link_button import RecNetLinkButton
from ....components.rec_net_post_button import RecNetPostButton
from ....components.rec_net_feed_button import RecNetFeedButton

class Profile(discord.ui.View):
    def __init__(self, ctx, user):
        super().__init__(
            timeout=None
        )
        self.add_item(RecNetLinkButton("user", user.username))
        #self.add_item(RecNetPostButton(ctx, user))
        #self.add_item(RecNetFeedButton(ctx, user))
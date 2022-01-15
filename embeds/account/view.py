import discord
from ..components.rec_net_link_button import RecNetLinkButton
from rec_net.managers.account import User

class Profile(discord.ui.View):
    def __init__(self, user: User):
        super().__init__()
        self.add_item(RecNetLinkButton("user", user.username))
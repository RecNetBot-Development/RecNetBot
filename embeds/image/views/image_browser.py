import discord
from ..image_embed import image_embed
from ...filter_embed import filter_embed
from ...raw_image_embed import raw_image_embed
from utility.rec_net_helpers import img_url
from utility.image.filter_posts import filter_posts
from rec_net.exceptions import Error
from random import randint
from utility.emojis import get_emoji
from utility.discord_helpers.helpers import edit_message

class BrowserSortSelect(discord.ui.Select):
    def __init__(self, browser):
        super().__init__(
            row=2, 
            placeholder="Sort", 
            custom_id="persistent:image_ui_sort_select", 
            options=
                [
                    discord.SelectOption(label="Newest to Oldest"),
                    discord.SelectOption(label="Oldest to Newest"),
                    discord.SelectOption(label="Cheers: Highest to Lowest"),
                    discord.SelectOption(label="Cheers: Lowest to Highest"),
                    discord.SelectOption(label="Comments: Highest to Lowest"),
                    discord.SelectOption(label="Comments: Lowest to Highest")
                ]
        )
        self.browser = browser

    async def callback(self, interaction):
        sort_chosen = self.values[0]
        self.browser.post_filter_embed = filter_embed(self.browser.post_filter, sort_chosen, len(self.browser.original_posts), self.browser.post_count) if self.browser.post_filter or self.browser._sort else None
        self.browser.posts = filter_posts(self.browser.posts, post_filter=None, sort=sort_chosen)

        self.browser.index = 0
        await self.browser.goto_index(interaction)

class BrowserButton(discord.ui.Button):
    def __init__(self, button_type, browser):
        super().__init__()
        self.button_type = button_type
        self.browser = browser
        
        match button_type:
            case "next":
                self.emoji = get_emoji('next')
                self.custom_id = "persistent:image_ui_next"
            case "prev":
                self.emoji = get_emoji('prev')
                self.custom_id = "persistent:image_ui_prev"
            case "next10":
                self.label = "10"
                self.emoji = get_emoji('next_bulk')
                self.custom_id = "persistent:image_ui_next10"
            case "prev10":
                self.label = "10"
                self.emoji = get_emoji('prev_bulk')
                self.custom_id = "persistent:image_ui_prev10"
            case "first":
                self.emoji = get_emoji('first')
                self.custom_id = "persistent:image_ui_first"
            case "last":
                self.emoji = get_emoji('last')
                self.custom_id = "persistent:image_ui_last"
            case "random":
                self.emoji = get_emoji('random')
                self.custom_id = "persistent:image_ui_random"
            case "indicator":
                self.custom_id = "persistent:image_ui_indicator"
                self.disabled = True
                
    async def callback(self, interaction):
        match self.button_type:
            case "first":
                self.browser.index = 0
            case "last":
                self.browser.index = self.browser.post_count-1
            case "random":
                self.browser.index = randint(0, self.browser.post_count-1)
            case "next":
                self.browser.index += 1
            case "prev":
                self.browser.index -= 1
            case "next10":
                self.browser.index += 10
            case "prev10":
                self.browser.index -= 10
            case _:
                return
            
        await self.browser.goto_index(interaction=interaction)

class ImageUI(discord.ui.View):
    def __init__(self, ctx, user, posts, interaction=None, is_component_interaction=False, raw=False, post_filter={}, sort="", original_embeds=[], start_index=0, rec_net = None):
        super().__init__(timeout=None)  
        self.ctx = ctx
        self.raw = raw
        self.interaction = interaction
        self.is_component_interaction = is_component_interaction
        self.user = user
        self.rec_net = rec_net
        
        # Instance cache
        self.cached_posts = {}
        self.cached_embeds = {}

        # Save for later
        self.post_filter = post_filter
        self._sort = sort
        self.original_posts = posts
        self.original_embeds = original_embeds

        filtered_posts = filter_posts(posts, self.post_filter, self._sort)
        self.post_filter_embed = filter_embed(self.post_filter, self._sort, len(self.original_posts), len(filtered_posts)) if self.post_filter else None
        self.posts = filtered_posts
        self.post_count = len(self.posts)
        
        self.index = start_index
        
        self.buttons = [
            [
                BrowserButton("prev10", browser=self),
                BrowserButton("prev", browser=self),
                BrowserButton("indicator", browser=self),
                BrowserButton("next", browser=self),
                BrowserButton("next10", browser=self),
            ],
            [
                BrowserButton("first", browser=self),
                BrowserButton("last", browser=self),
                BrowserButton("random", browser=self),
            ]
        ]
        self.update_items()
         
    def update_items(self):
        self.clear_items()
        for row, button_group in enumerate(self.buttons):
            for button in button_group:
                match button.button_type:
                    case "first" | "prev":
                        button.disabled = self.index <= 0
                    case "last" | "next":
                        button.disabled = self.index >= self.post_count-1
                    case "next10":
                        button.disabled = self.index+10 > self.post_count-1
                    case "prev10":
                        button.disabled = self.index-10 < 0
                    case "random":
                        button.disabled = self.post_count == 1
                    case "indicator":
                        button.label = f"{(self.index+1):,}/{self.post_count:,}"
                        
                button.row = row
                if row == 0: button.style = discord.ButtonStyle.primary
                else: button.style = discord.ButtonStyle.secondary
                
                self.add_item(button)
        self.add_item(BrowserSortSelect(self))

    async def start(self):
        if not self.posts: raise MissingPosts # No posts were found!
        post = await self.get_post()
        return self, await self.create_embed(post)
        
    async def goto_index(self, interaction):
        self.update_items()
        embeds = await self.create_embed(await self.get_post())
        await edit_message(self.ctx, interaction, embeds=embeds, view=self)

    async def create_embed(self, post):
        post_embed = None
        if post.id in self.cached_embeds: post_embed = self.cached_embeds[post.id]
            
        if self.raw:
            if not post_embed:
                post_embed = raw_image_embed(img_url(await self.get_post().image_name))
            embeds = [post_embed, self.post_filter_embed]
        else:       
            if self.post_filter_embed: 
                if not post_embed:
                    post_embed = image_embed(post).remove_footer()
                    post_embed.timestamp = discord.Embed.Empty
                embeds = [post_embed, self.post_filter_embed]
            else:
                embeds = [image_embed(post)]
                
        if post.id not in self.cached_embeds: self.cached_embeds[post.id] = post_embed
        return self.original_embeds + embeds
    
    async def patch_post_data(self, post):
        if post.id in self.cached_posts: return self.cached_posts[post.id]
            
        if self.rec_net:
            includes = []
            if not post.creator or type(post.creator) is int: includes.append("creator")
            if not post.event or type(post.event) is int: includes.append("event")
            if not post.room or type(post.room) is int: includes.append("room")
            if includes:
                post = await self.rec_net.image(id=post.id, includes=includes)
                if post.tagged: post.tagged = await self.rec_net.account(id=post.tagged)  # Patch in tagged users
                self.cached_posts[post.id] = post
                    
        return post
    
    async def get_post(self):
        assert self.posts, MissingPosts
        
        post = self.posts[self.index]
        return await self.patch_post_data(post)
    
    async def interaction_check(self, interaction):
        return self.ctx.user == interaction.user

class MissingPosts(Error):
    """Raised when no posts available when starting"""
    def __init__(self):
        super().__init__(
            "No posts found with the filters provided!"
        )
    

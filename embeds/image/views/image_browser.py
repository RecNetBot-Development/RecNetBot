import discord
from ..image_embed import image_embed
from ...filter_embed import filter_embed
from ...raw_image_embed import raw_image_embed
from ...error_embed import error_embed
from ...account.profile.profile_embed import profile_embed
from ...components.rec_net_link_button import RecNetLinkButton
#from ...account.view import Profile
from utility import img_url, filter_posts
from rec_net.exceptions import Error
from random import randint


class ImageUI(discord.ui.View):
    def __init__(self, ctx, user, posts, interaction=None, is_component_interaction=False, raw=False, post_filter={}, sort="", original_embeds=[], start_index=0, rec_net = None):
        super().__init__(timeout=None)  
        self.ctx = ctx
        self.index = start_index
        self.raw = raw
        self.interaction = interaction
        self.is_component_interaction = is_component_interaction
        self.user = user
        self.rec_net = rec_net
        
        # Instance cache
        self.cached_posts = {}

        # Save for later
        self.post_filter = post_filter
        self._sort = sort
        self.original_posts = posts
        self.original_embeds = original_embeds

        filtered_posts = filter_posts(posts, self.post_filter, self._sort)
        self.post_filter_embed = filter_embed(ctx, self.post_filter, self._sort, len(self.original_posts), len(filtered_posts)) if self.post_filter else None
        self.posts = filtered_posts

    async def start(self):
        if not self.posts:  # No posts were found!
            embed = error_embed(self.ctx, "No posts found under specified criteria!")
            
        post = await self.get_post()
        return self, await self.create_embed(post)
            #return await self.interaction.edit_original_message(embed=embed, ephermal=True)
        #if self.interaction: await self.handle_message(interaction=self.interaction, edit=True, is_component_interaction=self.is_component_interaction)
        #else: await self.handle_message(edit=False)
        
    """PRESET NAVIGATION BUTTONS"""
    @discord.ui.button(label="First", style=discord.ButtonStyle.primary, row=0, custom_id="persistent:image_ui_first")
    async def first(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.update_image(interaction, 0)

    @discord.ui.button(label="Last", style=discord.ButtonStyle.primary, row=0, custom_id="persistent:image_ui_last")
    async def last(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.update_image(interaction, len(self.posts))
        
    @discord.ui.button(label="Random", style=discord.ButtonStyle.primary, row=0, custom_id="persistent:image_ui_random")
    async def random(self, button: discord.ui.Button, interaction: discord.Interaction):
        random_index = randint(0, len(self.posts))
        await self.update_image(interaction, random_index, set=True)

    #["Newest to Oldest", "Oldest to Newest", "Cheers: Highest to Lowest", "Cheers: Lowest to Highest", "Comments: Highest to Lowest", "Comments: Lowest to Highest"]

    """SORT BUTTONS"""
    @discord.ui.select(row=2, placeholder="Sort", custom_id="persistent:image_ui_sort_select", options=
        [
            discord.SelectOption(label="Newest to Oldest"),
            discord.SelectOption(label="Oldest to Newest"),
            discord.SelectOption(label="Cheers: Highest to Lowest"),
            discord.SelectOption(label="Cheers: Lowest to Highest"),
            discord.SelectOption(label="Comments: Highest to Lowest"),
            discord.SelectOption(label="Comments: Lowest to Highest")
        ]
    )
    async def sort_posts(self, select: discord.ui.Select, interaction: discord.Interaction):
        sort_chosen = select.values[0]
        self.post_filter_embed = filter_embed(self.ctx, self.post_filter, sort_chosen, len(self.original_posts), len(self.posts)) if self.post_filter or self._sort else None
        self.posts = filter_posts(self.posts, post_filter=None, sort=sort_chosen)
        await self.update_image(interaction, 0)

    """NAVIGATION BUTTONS"""
    @discord.ui.button(label="<< 10", style=discord.ButtonStyle.secondary, row=1, custom_id="persistent:image_ui_previous_10")
    async def previous10(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.update_image(interaction, -10)

    @discord.ui.button(label="< 1", style=discord.ButtonStyle.secondary, row=1, custom_id="persistent:image_ui_previous")
    async def previous(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.update_image(interaction, -1)

    @discord.ui.button(label="1 >", style=discord.ButtonStyle.secondary, row=1, custom_id="persistent:image_ui_next")
    async def next(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.update_image(interaction, 1)

    @discord.ui.button(label="10 >>", style=discord.ButtonStyle.secondary, row=1, custom_id="persistent:image_ui_next_10")
    async def next10(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.update_image(interaction, 10)

    #@discord.ui.button(label="View profile", style=discord.ButtonStyle.red, row=3, custom_id="persistent:image_ui_view_profile")
    #async def profile(self, button: discord.ui.Button, interaction: discord.Interaction):
    #    embeds = [profile_embed(self.ctx, self.user)]
    #    view = Profile(self.ctx, self.user)
    #    await self.handle_message(interaction=interaction, edit=True, is_component_interaction=True, embeds=embeds, view=view)

    async def update_image(self, interaction, index_add, set=False):
        if not index_add:  # If it's 0, reset to first image
            self.index = 0
        else:
            if set:
                self.index = index_add
            else:
                self.index += index_add
            if self.index > len(self.posts)-1: self.index = len(self.posts)-1
            if self.index < 0: self.index = 0

        await self.handle_message(interaction=interaction, edit=True, is_component_interaction=True)

    async def handle_message(self, interaction=None, edit=False, is_component_interaction=False, embeds=[], view=None, content=""):
        if embeds == []: embeds = await self.create_embed(await self.get_post())
        if not view: view = self

        if edit: 
            if is_component_interaction:
                await interaction.response.edit_message(content=content, embeds=embeds, view=self)
            else:
                await interaction.edit_original_message(content=content, embeds=embeds, view=self)
        else:
            await self.ctx.respond(embeds=embeds, view=self)

        #self.add_item(RecNetLinkButton("user", self.user.username, 3))  # Profile link button
        #self.add_item(RecNetLinkButton("user", self.get_post().id, 3))  # Post link button

    async def create_embed(self, post):
        if self.raw:
            embeds = [raw_image_embed(self.ctx, img_url(await self.get_post().image_name)), self.post_filter_embed]
        else:       
            if self.post_filter_embed: 
                post_embed = image_embed(self.ctx, post).remove_footer()
                post_embed.timestamp = discord.Embed.Empty
                embeds = [post_embed, self.post_filter_embed]
            else:
                embeds = [image_embed(self.ctx, post)]
        return self.original_embeds + embeds
    
    async def patch_post_data(self, post):
        if post.id in self.cached_posts:
            return self.cached_posts[post.id]
        
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
        assert self.posts, MissingPosts("No posts found!")
        
        post = self.posts[self.index]
        return await self.patch_post_data(post)

class MissingPosts(Error):
    """Raised when no posts available when starting"""
    ...
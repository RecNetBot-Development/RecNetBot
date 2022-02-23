import discord
from ..image_embed import image_embed
from ...filter_embed import filter_embed
from ...raw_image_embed import raw_image_embed
from ...error_embed import error_embed
from ...account.profile_embed import profile_embed
from ...components.rec_net_link_button import RecNetLinkButton
#from ...account.view import Profile
from utility import img_url
from rec_net.exceptions import Error

class ImageUI(discord.ui.View):
    def __init__(self, ctx, user, posts, interaction=None, is_component_interaction=False, raw=False, post_filter={}, sort="", original_embeds=[]):
        super().__init__(timeout=None)  
        self.ctx = ctx
        self.index = 0
        self.raw = raw
        self.interaction = interaction
        self.is_component_interaction = is_component_interaction
        self.user = user

        # Save for later
        self.post_filter = post_filter
        self._sort = sort
        self.original_posts = posts
        self.original_embeds = original_embeds

        filtered_posts = self.filter_posts(posts, self.post_filter, self._sort)
        self.post_filter_embed = filter_embed(ctx, self.post_filter, self._sort, len(self.original_posts), len(filtered_posts)) if self.post_filter else None
        self.posts = filtered_posts

    async def start(self):
        if not self.posts:  # No posts were found!
            embed = error_embed(self.ctx, "No posts found under specified criteria!")
        return self, self.create_embed()
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
        self.posts = self.filter_posts(self.posts, post_filter=None, sort=sort_chosen)
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

    async def update_image(self, interaction, index_add):
        if not index_add:  # If it's 0, reset to first image
            self.index = 0
        else:
            self.index += index_add
            if self.index > len(self.posts)-1: self.index = len(self.posts)-1
            if self.index < 0: self.index = 0

        await self.handle_message(interaction=interaction, edit=True, is_component_interaction=True)

    async def handle_message(self, interaction=None, edit=False, is_component_interaction=False, embeds=[], view=None, content=""):
        if embeds == []: embeds = self.create_embed()
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

    def create_embed(self):
        if self.raw:
            embeds = [raw_image_embed(self.ctx, img_url(self.get_post().image_name)), self.post_filter_embed]
        else:
            if self.post_filter_embed: 
                post_embed = image_embed(self.ctx, self.get_post()).remove_footer()
                post_embed.timestamp = discord.Embed.Empty
                embeds = [post_embed, self.post_filter_embed]
            else:
                embeds = [image_embed(self.ctx, self.get_post())]
        return self.original_embeds + embeds
    
    def get_post(self):
        assert self.posts, MissingPosts("No posts found!")
        return self.posts[self.index]

    def filter_posts(self, posts, post_filter, sort):
        def room_filter(post):
            if str(post.room) in post_filter["rooms"].filter:
                return True
            return False

        def exclude_room_filter(post):
            if str(post.room) in post_filter["not_rooms"].filter:
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
            return post.event_id == filter

        def exclude_event_filter(post):
            filter = post_filter['exclude_events'].filter
            for event in filter:
                if int(event) == post.event_id: 
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
        match sort:
            case "Oldest to Newest":
                filtered_posts = filtered_posts.reverse()
            case "Cheers: Highest to Lowest":
                def cheers_sort(post):
                    return post.cheer_count

                filtered_posts = filtered_posts.sort(key=cheers_sort, reverse=True)
            case "Cheers: Lowest to Highest":
                def cheers_sort(post):
                    return post.cheer_count

                filtered_posts = filtered_posts.sort(key=cheers_sort)
            case "Comments: Highest to Lowest":
                def comments_sort(post):
                    return post.comment_count

                filtered_posts = filtered_posts.sort(key=comments_sort, reverse=True)
            case "Comments: Lowest to Highest":
                def comments_sort(post):
                    return post.comment_count

                filtered_posts = filtered_posts.sort(key=comments_sort)
            case _:  # Newest to Oldest
                pass

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

class MissingPosts(Error):
    """Raised when no posts available when starting"""
    ...
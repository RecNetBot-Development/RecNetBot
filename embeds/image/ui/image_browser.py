import discord
from ..image_embed import image_embed
from ...filter_embed import filter_embed
from ...raw_image_embed import raw_image_embed
from scripts import img_url

class ImageUI(discord.ui.View):
    def __init__(self, ctx, posts, interaction=None, raw=False, post_filter={}, sort=""):
        super().__init__()  
        self.ctx = ctx
        self.index = 0
        self.raw = raw
        self.interaction = interaction
        
        filtered_posts = self.filter_posts(posts, post_filter, sort)
        self.post_filter_embed = filter_embed(ctx, post_filter, sort, len(posts), len(filtered_posts)) if post_filter or sort else None
        self.posts = filtered_posts

    async def start(self):
        embed = self.create_embed()
        if self.interaction: await self.handle_message(interaction=self.interaction, edit=True)
        else: await self.handle_message(edit=False)
        
    """PRESET NAVIGATION BUTTONS"""
    @discord.ui.button(label="First", style=discord.ButtonStyle.red, row=0)
    async def first(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.update_image(interaction, 0)

    @discord.ui.button(label="Last", style=discord.ButtonStyle.red, row=0)
    async def last(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.update_image(interaction, len(self.posts))

    #["Newest to Oldest", "Oldest to Newest", "Cheers: Highest to Lowest", "Cheers: Lowest to Highest", "Comments: Highest to Lowest", "Comments: Lowest to Highest"]

    """SORT BUTTONS"""
    @discord.ui.select(row=2, placeholder="Sort", options=
        [
            discord.SelectOption(label="Newest to Oldest"),
            discord.SelectOption(label="Oldest to Newest"),
            discord.SelectOption(label="Cheers: Highest to Lowest"),
            discord.SelectOption(label="Cheers: Lowest to Highest"),
            discord.SelectOption(label="Comments: Highest to Lowest"),
            discord.SelectOption(label="Comments: Lowest to Highest")
        ]
    )
    async def sort(self, select: discord.ui.Select, interaction: discord.Interaction):
        self.posts = self.filter_posts(self.posts, post_filter=None, sort=select.values[0])
        await self.update_image(interaction, 0)


    """NAVIGATION BUTTONS"""
    @discord.ui.button(label="<< 10", style=discord.ButtonStyle.red, row=1)
    async def previous10(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.update_image(interaction, -10)

    @discord.ui.button(label="< 1", style=discord.ButtonStyle.red, row=1)
    async def previous(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.update_image(interaction, -1)

    @discord.ui.button(label="1 >", style=discord.ButtonStyle.red, row=1)
    async def next(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.update_image(interaction, 1)

    @discord.ui.button(label="10 >>", style=discord.ButtonStyle.red, row=1)
    async def next10(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.update_image(interaction, 10)

    async def update_image(self, interaction, index_add):
        if not index_add:  # If it's 0, reset to first image
            self.index = 0
        else:
            self.index += index_add
            if self.index > len(self.posts)-1: self.index = len(self.posts)-1
            if self.index < 0: self.index = 0

        await self.handle_message(interaction=interaction, edit=True, is_button_interaction=True)

    async def handle_message(self, interaction=None, edit=False, is_button_interaction=False):
        if self.raw:
            #content = img_url(self.get_post().image_name)
            content = f"{self.index+1:,}/{len(self.posts)}"
            embeds = [raw_image_embed(self.ctx, img_url(self.get_post().image_name))]
            if self.post_filter_embed: embeds.append(self.post_filter_embed)
        else:
            #content = None
            content = f"{self.index+1:,}/{len(self.posts)}"
            if self.post_filter_embed: 
                post_embed = self.create_embed().remove_footer()
                post_embed.timestamp = discord.Embed.Empty
                embeds = [post_embed, self.post_filter_embed]
            else:
                embeds = [self.create_embed()]

        if edit: 
            if is_button_interaction:
                await interaction.response.edit_message(content=content, embeds=embeds, view=self)
            else:
                await interaction.edit_original_message(content=content, embeds=embeds, view=self)
        else:
            await self.ctx.respond(content=content, embeds=embeds, view=self)

    def create_embed(self):
        embed = image_embed(self.ctx, self.get_post())
        return embed

    def get_post(self):
        return self.posts[self.index]

    def filter_posts(self, posts, post_filter, sort):
        def room_filter(post):
            if str(post.room_id) in post_filter["rooms"].filter:
                return True
            return False

        def exclude_room_filter(post):
            if str(post.room_id) in post_filter["not_rooms"].filter:
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

        return list(filtered_posts)

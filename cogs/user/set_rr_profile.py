import discord
from discord import ApplicationContext
from discord.commands import slash_command, Option
from exceptions import AccountNotFound, ConnectionAlreadyDone
from embeds import get_default_embed
from utils import post_url

@slash_command(
    name="set_profile",
    description="Link your Rec Room profile to your Discord!"
)
async def set_rr_profile(
    self, 
    ctx: ApplicationContext, 
    username: Option(str, "Enter RR username", required=True)
):
    await ctx.interaction.response.defer()
    
    # Check if RR account exists
    user = await self.bot.RecNet.accounts.get(username)
    if not user: raise AccountNotFound
    
    # Check if RR account is already linked
    check_rr = self.bot.cm.get_rec_room_connection(user.id)
    if check_rr: raise ConnectionAlreadyDone
    
    # Fetch cheers from verify post
    post = self.bot.verify_post
    cheer_list = await post.get_cheers(force=True)
    
    # Create connection if needed
    connection = self.bot.cm.get_discord_connection(ctx.author.id, require_done=False)
    if not connection or user.id != connection.rr_id:
        self.bot.cm.delete_connection(ctx.author.id)
        status = 2 if user.id in cheer_list else 1
        self.bot.cm.create_connection(ctx.author.id, user.id, 2 if user.id in cheer_list else status)
    else:
        status = connection.status
        
    # Check the status
    em = get_default_embed()
    match status:
        case 1:
            if user.id not in cheer_list:
                em.description = f"Cheer this [this post]({post_url(post.id)}) to verify yourself."
                return await ctx.respond(embed=em)
        case 2:
            if user.id in cheer_list:
                em.description = f"Uncheer from this [this post]({post_url(post.id)}) to verify yourself."
                return await ctx.respond(embed=em)
        case 0:
            em.description = "You are already verified."
            return await ctx.respond(embed=em)
            
    # Verification done
    self.bot.cm.update_connection(ctx.author.id, user.id, 0)
    em.description = f"Linked to `{user.username}`!"
    await ctx.respond(embed=em)
    
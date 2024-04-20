import discord
import recnetpy
import time
import recnetpy.dataclasses
import io
import aiohttp
import math
import random
from embeds import get_default_embed
from typing import List, TYPE_CHECKING, Optional, Dict
from utils import img_url, snapchat_caption, profile_url, post_url, room_url
from resources import get_icon
from discord.ext import tasks
from database import FeedTypes
from datetime import datetime

"""

TODO

- Handle privated / deleted rooms

"""

if TYPE_CHECKING:
    from bot import RecNetBot

latest_image_timestamps = {}
accounts = {}
rooms = {}
webhooks = {}
cached_attachments = {}

interval = 10 # task loop interval in seconds
rate_limit = 10_000 # rec room rate limit (requests per hour)
multiplier = 1.5 # what to multiply interval with if close to hitting ratelimit
max_photos = 5 # how many photos to fetch at a time

# Calculate the max amount of rooms we can fetch before hitting Rec Room API's rate limit
def calculate_max_rooms(interval_seconds):
    return math.floor(rate_limit/(3600/interval_seconds))

# Calculate how many RR api calls are made in an hour with polling rate and rooms
def rr_api_calls_per_hour(interval_seconds, room_count):
    return math.ceil(3600/interval_seconds*room_count) 

# Links for images in compact mode
class ImageLinks(discord.ui.View):
    def __init__(self, image: recnetpy.dataclasses.Image, username: str, room_name: str):
        super().__init__()

        buttons = [
            discord.ui.Button(
                label=f"^{room_name}",
                url=room_url(room_name),
                style=discord.ButtonStyle.url
            ),
            discord.ui.Button(
                label=f"@{username}",
                url=profile_url(username),
                style=discord.ButtonStyle.url
            ),
            discord.ui.Button(
                label="RecNet",
                url=post_url(image.id),
                style=discord.ButtonStyle.url
            )
        ]
        
        for i in buttons:
            self.add_item(i)

@tasks.loop(seconds=interval)
async def update_feeds(bot: 'RecNetBot'):
    global latest_image_timestamps, accounts, webhooks, interval, rate_limit, multiplier, max_photos, rooms, cached_attachments

    # Get all feeds from database
    feeds = await bot.fcm.get_feeds_based_on_type(FeedTypes.IMAGE)
    if not feeds: return

    # Get all rooms' ids
    room_ids = feeds.keys()
    room_count = len(room_ids)

    # Find any new rooms we haven't fetched yet
    new_rooms = list(filter(lambda room_id: room_id not in rooms, room_ids))

    # Fetch & cache new rooms
    if new_rooms:
        print(f"New rooms: {new_rooms}")  # DEBUG
        rooms_ = await bot.RecNetWebhook.rooms.fetch_many(list(new_rooms))
        for i in rooms_:
            rooms[i.id] = i
            new_rooms.remove(i.id)

        # these rooms are privated or deleted cuz they couldn't be fetched
        for i in new_rooms:
            for j in feeds[i]:
                await delete_feed(bot, j)

    # Calculate feed count (DEBUG)
    feed_count = 0
    for i in feeds.values():
        feed_count += len(i)

    # Calculate max rooms (DEBUG)
    max_rooms = calculate_max_rooms(interval)

    # Print info (DEBUG)
    print(f"\nLoop! Feeds: {feed_count}\nTask interval: {update_feeds.seconds} ({interval})\nRoom count: {room_count}/{max_rooms}\nRR API calls per hour: {rr_api_calls_per_hour(interval, room_count):,}/10,000\nMax photos: {max_photos}\n")

    # If we have a risk of hitting the rate limit, increase task interval
    if rr_api_calls_per_hour(interval, room_count) >= rate_limit:
        interval *= multiplier
        max_photos = math.ceil(max_photos * multiplier)
        print(f"Hitting the rate limit. Increased interval from {interval/multiplier} to {interval}. Increased max rooms from {calculate_max_rooms(interval/multiplier)} to {calculate_max_rooms(interval)}. Increased max photos to {max_photos}")
        update_feeds.change_interval(seconds=interval)
        update_feeds.restart(bot)

    # Begin sending new images to channels
    for room_id in room_ids:
        # Get images from room
        images = await bot.RecNetWebhook.images.in_room(room_id, take=max_photos)

        # Find new images
        new_images: List[recnetpy.dataclasses.Image] = []
        for img in images:
            latest_timestamp = latest_image_timestamps.get(room_id, None)
            if latest_timestamp is None:
                latest_image_timestamps[room_id] = time.time()
            elif img.created_at > latest_timestamp:
                new_images.append(img)

        if not new_images: continue

        # Newer images first
        new_images.reverse()

        # Clear attachment cache
        cached_attachments = {}

        # Benchmarking (DEBUG)
        start = time.perf_counter() 

        print(f"{len(list(new_images))} new images in {room_id}") # DEBUG
        latest_image_timestamps[room_id] = new_images[-1].created_at

        # Fetch all accounts
        acc_ids = []
        for img in new_images:
            if img.player_id in accounts: continue
            acc_ids.append(img.player_id)

        # If there's any new users
        if acc_ids:
            accs = await bot.RecNetWebhook.accounts.fetch_many(acc_ids)

            # Map accounts based on id
            for i in accs:
                accounts[i.id] = i

        # get all channels and map them based on id
        for webhook_id in feeds[room_id]:
            if webhook_id in webhooks: continue
            #channels[channel_id] = bot.get_channel(channel_id)
            try:
                webhooks[webhook_id] = await bot.fetch_webhook(webhook_id)
            except discord.errors.NotFound:
                await delete_feed(bot, webhook_id)
                feeds[room_id].remove(webhook_id)

        # Process each image and send them to webhooks
        for img in new_images:
            if img.description: 
                # Download new photo and edit Snapchat caption
                url_for_img = img_url(img.image_name, resolution=480)
                async with aiohttp.ClientSession() as session:
                    async with session.get(url_for_img) as resp:
                        file = snapchat_caption(io.BytesIO(await resp.read()), img.description, img.id)[0]
            else:
                # Send photo as an URL if no editing needs to be done
                file = discord.MISSING

            # Patch image dataclass
            img.player = accounts[img.player_id]
            img.room = rooms[img.room_id]

            # Some images are taken "from the future". This prevents it.
            timestamp = int(time.time())
            if img.created_at > timestamp:
                img.created_at = timestamp

            if file: img.image_name = None  # Don't embed image as URL
            msg_kwargs = image_message(img, file.filename if file else None)
                    
             # Add display emoji to username if any
            if img.player.display_emoji: 
                user_name = f"{img.player.display_emoji} {img.player.display_name}"
            else:
                user_name = img.player.display_name

            # Send image to all subscribed feeds
            for webhook_id in feeds[room_id]:
                webhook = webhooks.get(webhook_id)
                if webhook: 
                    await send(
                        webhook, 
                        bot,
                        file=file, 
                        username=user_name, 
                        avatar_url=img_url(img.player.profile_image, resolution=180, crop_square=True), 
                        **msg_kwargs
                    )

                    # Use cached attachment next if file sent
                    if file is not discord.MISSING:
                        img.image_name = cached_attachments[file.filename]
                        file = discord.MISSING
                        msg_kwargs = image_message(img)

                else: feeds[room_id].remove(webhook_id)

        print("Elapsed", time.perf_counter()-start) # DEBUG

def image_message(img: recnetpy.dataclasses.Image, filename: str = None) -> Dict[str, str]:
    """
    Returns the kwargs for the image message
    """
    # Create button view
    view = ImageLinks(img, username=img.player.username, room_name=img.room.name)   

    # Create embed skeleton
    embed = get_default_embed(
        footer=discord.EmbedFooter("Powered by RecNetBot", get_icon("rnb"))
    )
    
    # Attach image to embed
    if filename is not None:
        # Use attachment
        url_for_img =f"attachment://{filename}"
    if img.image_name:
        if "discord" in img.image_name:
            # Embed cached Discord image as URL
            url_for_img = img.image_name
        else:
            # Embed RecNet image as URL
            url_for_img = img_url(img.image_name, resolution=480)
        
    embed.set_image(url=url_for_img)

    # Create content
    content = f"New photo taken in ^{img.room.name} by @{img.player.username} — <t:{img.created_at}:R>"

    # Add description in content if any
    if img.description:
        content += f"\n\"{img.description.rstrip()}\""

    return {"content": content, "view": view, "embed": embed}


async def delete_feed(bot: 'RecNetBot', webhook_id: int, channel: int | discord.TextChannel = None):
    """Deletes the feed from memory and database
    """
    global webhooks

    # Get channel id if not passed
    if not channel:
        channel_id = await bot.fcm.get_channel_id_of_feed(webhook_id)
        channel = bot.get_channel(channel_id)
    elif isinstance(channel, int):
        channel = bot.get_channel(channel)

    # Delete the feed
    await bot.fcm.delete_feed_with_webhook_id(webhook_id)
    if webhook_id in webhooks: 
        webhooks.pop(webhook_id)

        try:  # Attempt to delete the webhook if not already deleted
            webhook = await bot.fetch_webhook(webhook_id)
            await webhook.delete()
        except:
            ...
    
    # Inform server 
    if channel and channel.can_send():
        em = get_default_embed(
            title="Photo Feed Disabled!",
            description="The webhook for the photo feed has been deleted. " \
                        "This was either manual or the room was privated / deleted. " \
                        f"Thanks for giving the feature a shot! [|=)] Feel free to let us know your experiences in [my test server](<{bot.config.get('server_link')}>).",
            thumbnail=discord.EmbedMedia(url=get_icon("photo"))
        )
        await channel.send(embed=em)
    

async def send(webhook: discord.Webhook, bot: 'RecNetBot', **kwargs) -> Optional[discord.Message]:
    """Sends a message to the webhook. Deletes the feed if webhook isn't found.
    """
    msg = None
    try:
        # Check for attachments and if they're cached
        file: discord.File = kwargs.get("file")
        if file is not discord.MISSING and file.filename not in cached_attachments:
            kwargs["wait"] = True

        msg: discord.WebhookMessage | None = await webhook.send(**kwargs)

        # Cache the attachment
        if file is not discord.MISSING:
            cached_attachments[file.filename] = msg.embeds[0].image.url

    except discord.errors.NotFound:  # Webhook has been deleted
        # Delete the feed
        await delete_feed(bot, webhook.id, webhook.channel)

    return msg
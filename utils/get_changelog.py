import re

async def get_changelog(bot) -> dict:
    """
    Fetches the latest changelog
    """

    channel = bot.get_channel(bot.config.get("update_channel", 0))

    # Make sure the channel exists
    if not channel:
        return {"error": 0}
    
    # Get the latest message
    messages = await channel.history(limit=1).flatten()

    # Make sure there is a message
    if not messages:
        return {"error": 1}

    # Get the latest one
    latest = messages[0]

    # Form response
    change_log = latest.content

    # Get rid of pings
    change_log = re.sub("<@.+?>", "", change_log)

    # Get rid of @everyone
    change_log = change_log.replace("@everyone", "")

    # Return the data
    data = {
        "raw": change_log,
        "created_timestamp": int(latest.created_at.timestamp()) if latest.created_at else None,
        "edited_timestamp": int(latest.edited_at.timestamp()) if latest.edited_at else None
    }

    return data

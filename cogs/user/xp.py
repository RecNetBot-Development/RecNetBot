import discord
import math # nerdy
from discord.commands import slash_command, Option
from utils.converters import FetchAccount
from embeds import get_default_embed
from resources import get_emoji
from exceptions import ConnectionNotFound
from recnetpy.dataclasses.account import Account
from utils import img_url, profile_url, unix_timestamp
from datetime import datetime, timezone, timedelta
from utils.autocompleters import account_searcher
from database import ConnectionManager

@slash_command(
    name="xp",
    description="View a player's level & XP progress with details.",
)
async def xp(
    self,   
    ctx: discord.ApplicationContext,
    account: Option(FetchAccount, name="username", description="Enter RR username", default=None, required=False, autocomplete=account_searcher)
):
    await ctx.interaction.response.defer()
    
    if not account:  # Check for a linked RR account
        cm: ConnectionManager = self.bot.cm
        account: Account = await cm.get_linked_account(self.bot.RecNet, ctx.author.id)
        if not account: raise ConnectionNotFound

    # Get account progression
    progression = await account.get_level()
    level, xp = progression.level, progression.xp

    # Get details
    details = PROGRESSION.get(level, None)
    if not details:
        # Oddity
        return await ctx.respond(f"Level {level} is not supported! If you believe this is a mistake, yell at my developers.")
    required_xp, total_xp, reward = details["required_xp"], details["total_xp"], REWARDS.get(details["reward"], "None")
    remaining_xp = required_xp - xp

    # Create embed skeleton
    em = get_default_embed()
    em.title = f"Level {level}"
    em.set_author(name=f"@{account.username}", 
                  icon_url=img_url(account.profile_image, crop_square=True, resolution=360),
                  url=profile_url(account.username)
    )

    if required_xp:  # if not max lvl
        nearest_tenth = int(round(xp / required_xp * 100, -1)) // 10

        # Progress bar
        #bar = f"{xp}/{required_xp}" if required_xp else "MAX"
        bar = "=" * nearest_tenth
        bar = bar.ljust(10)

        # Replace with emojis
        filled, empty = get_emoji("progress_filled"), get_emoji("progress_empty")
        bar = bar.replace("=", filled)
        bar = bar.replace(" ", empty)

        # Compile it all together
        progress_text = f"**{xp}** XP {get_emoji('progress_left')}{bar}{get_emoji('progress_right')} **{required_xp}** XP"

        # Next reward
        progress_text += f"\n**Next Reward** • {reward}"

        # Playtime
        remaining_playtime = math.ceil(remaining_xp / 10) * 5
        remaining_days = math.ceil(remaining_playtime / 75)
        progress_text += f"\n**Remaining Playtime** • {remaining_playtime} mins ({remaining_days} day{'' if remaining_days == 1 else 's'})"

        # Next cap reset
        midnight = (datetime
             .now(timezone.utc)
             .replace(hour=0, minute=0, second=0, microsecond=0)
        ) + timedelta(days=1)

        # Information on gaining XP
        em.add_field(name="How to gain XP?", inline=False, value="- You gain 10 XP per 5 minutes spent in public instances." \
                                                "\n - The daily XP cap is 150 XP, which is 75 minutes of playtime." \
                                                f"\n - The daily XP cap resets {unix_timestamp(int(midnight.timestamp()), 'R')}."
                                                "\n- Completing games or quests does NOT give extra XP." \
        )

        """
        remaining_xp_to_max = PROGRESSION[50]["total_xp"] - (total_xp + xp)
        remaining_playtime_to_max = math.ceil(remaining_xp_to_max / 10) * 5
        remaining_days_to_max = math.ceil(remaining_playtime_to_max / 75)
        max_progress_text = f"{total_xp + xp}/{remaining_xp_to_max} XP remaining ({round((total_xp + xp) / remaining_xp_to_max * 100)}%)" \
                            f"\n**Remaining Playtime** • {remaining_playtime_to_max} mins ({remaining_days_to_max} day{'' if remaining_days_to_max == 1 else 's'})"
        em.add_field(name="Progress to LVL 50", value=max_progress_text, inline=False)
        """
    else:
        # ew hard-coded???
        max = get_emoji("progress_max1") + get_emoji("progress_max2") + get_emoji("progress_max3")
        
        if level > 50:
            progress_text = f"— XP {get_emoji('progress_left')}{max}{get_emoji('progress_right')} — XP"
        else:
            progress_text = f"**1080** XP {get_emoji('progress_left')}{max}{get_emoji('progress_right')} **1080** XP"

            em.add_field(name="Congratulations!", value="Good job on reaching level 50! [Now you can finally play the game.](https://youtu.be/tg2PD-dwsIw)")
    
    # Implement to embed
    em.description = progress_text

    # Progress to lvl 50
    if level <= 50:
        xp_to_max = PROGRESSION[50]["total_xp"]
        percentage = round((total_xp + xp) / PROGRESSION[50]["total_xp"] * 100, 1)
        em.set_footer(text=f"({int(percentage) if percentage % 10 == 0 else percentage}%) {total_xp + xp}/{xp_to_max} XP in total")

    await ctx.respond(
        embed=em,
        #view=view
    )

REWARDS = {
    # rewards according to below progression dictionary
    0: f"{get_emoji('pizza')} Consumable",
    2: f"{get_emoji('reward_box')} 2 Star Box",
    3: f"{get_emoji('reward_box')} 3 Star Box",
    4: f"{get_emoji('reward_box')} 4 Star Box",
    5: f"{get_emoji('reward_box')} 5 Star Box"
}
        
PROGRESSION = {
    # required_xp = the amount of XP required to level up
    # reward:
        # 0 = consumable
        # 2 = 2 star box
        # 3 = 3 star box
        # 4 = 4 star box
        # 5 = 5 star box
    1: {
        "required_xp": 10,
        "reward": 2,
        "total_xp": 0
    },
    2: {
        "required_xp": 10,
        "reward": 0,
        "total_xp": 10
    },
    3: {
        "required_xp": 20,
        "reward": 2,
        "total_xp": 20
    },
    4: {
        "required_xp": 20,
        "reward": 0,
        "total_xp": 40
    },
    5: {
        "required_xp": 20,
        "reward": 2,
        "total_xp": 60
    },
    6: {
        "required_xp": 20,
        "reward": 0,
        "total_xp": 80
    },
    7: {
        "required_xp": 20,
        "reward": 2,
        "total_xp": 100
    },
    8: {
        "required_xp": 20,
        "reward": 0,
        "total_xp": 120
    },
    9: {
        "required_xp": 20,
        "reward": 2,
        "total_xp": 140
    },
    10: {
        "required_xp": 45,
        "reward": 2,
        "total_xp": 160
    },
    11: {
        "required_xp": 45,
        "reward": 2,
        "total_xp": 205
    },
    12: {
        "required_xp": 45,
        "reward": 2,
        "total_xp": 250
    },
    13: {
        "required_xp": 45,
        "reward": 2,
        "total_xp": 295
    },
    14: {
        "required_xp": 45,
        "reward": 2,
        "total_xp": 340
    },
    15: {
        "required_xp": 45,
        "reward": 2,
        "total_xp": 385
    },
    16: {
        "required_xp": 45,
        "reward": 2,
        "total_xp": 430
    },
    17: {
        "required_xp": 45,
        "reward": 2,
        "total_xp": 475
    },
    18: {
        "required_xp": 45,
        "reward": 2,
        "total_xp": 520
    },
    19: {
        "required_xp": 45,
        "reward": 2,
        "total_xp": 565
    },
    20: {
        "required_xp": 115,
        "reward": 2,
        "total_xp": 610
    },
    21: {
        "required_xp": 115,
        "reward": 3,
        "total_xp": 725
    },
    22: {
        "required_xp": 115,
        "reward": 2,
        "total_xp": 840
    },
    23: {
        "required_xp": 115,
        "reward": 3,
        "total_xp": 955
    },
    24: {
        "required_xp": 115,
        "reward": 2,
        "total_xp": 1070
    },
    25: {
        "required_xp": 115,
        "reward": 3,
        "total_xp": 1185
    },
    26: {
        "required_xp": 115,
        "reward": 2,
        "total_xp": 1300
    },
    27: {
        "required_xp": 115,
        "reward": 3,
        "total_xp": 1415
    },
    28: {
        "required_xp": 115,
        "reward": 2,
        "total_xp": 1530
    },
    29: {
        "required_xp": 115,
        "reward": 3,
        "total_xp": 1645
    },
    30: {
        "required_xp": 360,
        "reward": 4,
        "total_xp": 1760
    },
    31: {
        "required_xp": 360,
        "reward": 3,
        "total_xp": 2120
    },
    32: {
        "required_xp": 360,
        "reward": 3,
        "total_xp": 2480
    },
    33: {
        "required_xp": 360,
        "reward": 3,
        "total_xp": 2840
    },
    34: {
        "required_xp": 360,
        "reward": 4,
        "total_xp": 3200
    },
    35: {
        "required_xp": 360,
        "reward": 3,
        "total_xp": 3560
    },
    36: {
        "required_xp": 360,
        "reward": 3,
        "total_xp": 3920
    },
    37: {
        "required_xp": 360,
        "reward": 3,
        "total_xp": 4280
    },
    38: {
        "required_xp": 360,
        "reward": 3,
        "total_xp": 4640
    },
    39: {
        "required_xp": 360,
        "reward": 4,
        "total_xp": 5000
    },
    40: {
        "required_xp": 1080,
        "reward": 4,
        "total_xp": 5360
    },
    41: {
        "required_xp": 1080,
        "reward": 4,
        "total_xp": 6440
    },
    42: {
        "required_xp": 1080,
        "reward": 4,
        "total_xp": 7520
    },
    43: {
        "required_xp": 1080,
        "reward": 4,
        "total_xp": 8600
    },
    44: {
        "required_xp": 1080,
        "reward": 4,
        "total_xp": 9680
    },
    45: {
        "required_xp": 1080,
        "reward": 4,
        "total_xp": 10760
    },
    46: {
        "required_xp": 1080,
        "reward": 4,
        "total_xp": 11840
    },
    47: {
        "required_xp": 1080,
        "reward": 4,
        "total_xp": 12920
    },
    48: {
        "required_xp": 1080,
        "reward": 4,
        "total_xp": 14000
    },
    49: {
        "required_xp": 1080,
        "reward": 5,
        "total_xp": 15080
    },
    50: {
        "required_xp": 0,
        "reward": None,
        "total_xp": 16160
    },
    99: {
        "required_xp": 0,
        "reward": None,
        "total_xp": 0
    }
}
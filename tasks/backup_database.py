from datetime import datetime
from datetime import date
from discord.ext import tasks

@tasks.loop(hours=48)
async def backup_database(bot):
    # Backup the database every 2 days
    print("Backing up database...")
    await bot.db.backup(bot.backup)

    # Mark date in which backed up
    with open("backup_date.txt", "w") as f:
        f.write(f"DATABASE BACKED UP ON {date.today()} AT {int(datetime.now().timestamp())} UNIX")
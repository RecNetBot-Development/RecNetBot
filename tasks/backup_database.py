from datetime import datetime
from datetime import date
from discord.ext import tasks
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot import RecNetBot

@tasks.loop(hours=48)
async def backup_database(bot: 'RecNetBot'):
    # Backup the database every 2 days
    print("Backing up database...")
    await bot.db.backup(bot.backup)

    # Mark date in which backed up
    with open("backup_date.txt", "w") as f:
        f.write(f"DATABASE BACKED UP ON {date.today()} AT {int(datetime.now().timestamp())} UNIX")
        
def start_backup_task(bot: 'RecNetBot'):
    """Start the task for backing up the database
    """
    if not backup_database.is_running():
        backup_database.start(bot)
import discord
from exceptions import ConnectionNotFound, AccountNotFound
from recnetpy.dataclasses.account import Account
from recnetpy import Client
from database import ConnectionManager

async def get_linked_account(cm: ConnectionManager, RecNet: Client, discord_id: int) -> Account:
    """
    Fetches the linked Rec Room account of a Discord account
    """
    
    connection = cm.get_discord_connection(discord_id)
    if not connection: raise ConnectionNotFound
    account = await RecNet.accounts.fetch(connection.rr_id)
    if not account: raise AccountNotFound
    return account
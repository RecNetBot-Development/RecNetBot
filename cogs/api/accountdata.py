from utility import load_cfg
from discord.commands import slash_command, Option  # Importing the decorator that makes slash commands.
from rec_net.exceptions import Error
from embeds import account_data_embed

cfg = load_cfg()

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="accountdata",
    description="Get raw account data from the API."
)
async def accountdata(
    self, 
    ctx, 
    account_input_type: Option(str, choices=["Username", "Id"], required=True),
    account: Option(str, "Enter the account", required=True)
):
    await ctx.interaction.response.defer()
    host = "https://accounts.rec.net"
    if account_input_type == "Id":
        if not account.isdigit(): raise InvalidAccountId("Account id must be a digit!")  
        parsed_account_id = int(account)
        account_resp = await self.bot.rec_net.rec_net.accounts.account(parsed_account_id).get().fetch()
        endpoint = f"/account/{account}"
    else:
        account_resp = await self.bot.rec_net.rec_net.accounts.account().get({"username": account}).fetch()
        endpoint = f"/account?username={account}"

    await ctx.respond(
        content = host + endpoint,
        embed=account_data_embed(ctx, account_resp.data)
    )

class InvalidAccountId(Error):
    ...


class AccountNotFound(Error):
    ...
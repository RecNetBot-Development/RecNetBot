import json
import urllib.parse
import re
import itertools
from utils import date_to_unix
from datetime import datetime
from recnetlogin import RecNetLoginAsync
from recnetpy.dataclasses.account import Account
from discord.ext import tasks
from typing import List, Optional

DEVICE_CLASS = [
    "Unknown",
    "VR",
    "Screen Mode",
    "Mobile",
    "Quest 1",
    "Quest 2"
]

class Client():
    def __init__(self, bot, username: str, password: str):
        # RecNetBot
        self.bot = bot
        
        # Credentials for the bot
        self.username = username
        self.password = password
        self.login = None  # Filled in start()
        
        # Bot RR account
        self.account: Account = None
        
        
    async def start(self) -> bool:
        """Initializes and starts the in-game RecNetBot

        Returns:
            bool: Success
        """
        if self.username and self.password:
            # Verify credentials
            self.login = RecNetLoginAsync(username=self.username, password=self.password)
            if not await self.login.get_token(): return False
            
            # Fetch the RR account
            self.account = await self.bot.RecNet.accounts.get(self.username)
            if not self.account: return False
            
            # Start
            self.update.start()
            return True
        return False
            
        
    async def get_headers(self) -> dict:
        """Returns authorized headers for RecNet API.

        Returns:
            dict: Headers with a bearer token
        """
        return {"Authorization": await self.login.get_token(include_bearer=True)}
        
    
    def generate_message(self, text: str) -> dict:
        """Generates a message that can be sent through RecNet's chat API

        Args:
            text (str): Message content

        Returns:
            dict: Message structure
        """
        
        message = {
            "Data": str(text), 
            "Type": 0,
            "Version": 1
        }
        return urllib.parse.quote(json.dumps(message))
    
    
    async def leave_inactive_threads(self) -> None:
        """Makes the bot leave all inactive threads"""
        threads = await self.get_threads()
        
        # Go through threads
        for t in threads:
            # If the bot is the only user
            if len(t["playerIds"]) <= 1:
                # Leave
                await self.bot.RecNet.rec_net.custom("https://chat.rec.net/").thread(t["chatThreadId"]).leave.make_request("post", headers=await self.get_headers())
    
    
    async def get_threads(self, unread_only: bool = False) -> list:
        """Fetches all the unread threads

        Returns:
            list: Raw, unread threads
        """
        
        # Fetch threads
        resp = await self.bot.RecNet.rec_net.custom("https://chat.rec.net/").thread.make_request("get", headers=await self.get_headers(), params={"maxCount": 32, "mode": 0})
        if not resp.success: return []
        
        if unread_only:
            # Get unread threads
            unread_threads = list(
                filter(lambda t: (t["latestMessage"]["chatMessageId"] != t["lastReadMessageId"]), resp.data)
            )
            
            return unread_threads
        
        return resp.data
    
    
    async def get_unread_messages(self, thread_id: int, latest_thread_msg_id: int, contents_only: bool = False, max_count: int = 8) -> list:
        """Fetches all the unread messages

        Returns:
            list: Raw, unread messages
        """
        
        # Fetch messages
        resp = await self.bot.RecNet.rec_net.custom("https://chat.rec.net/").thread(thread_id).message.make_request("get", headers=await self.get_headers(), params={"MessageCount": max_count, "Mode": 0})
        if not resp.success: return []
        
        # Get unread messages
        unread_messages = list(filter(lambda m: m["chatMessageId"] > latest_thread_msg_id and int(m["senderPlayerId"]) != self.account.id, resp.data))
        
        # Return as oldest first
        unread_messages.reverse()

        # If only the contents are wanted
        if contents_only:
            unread_messages = list(map(lambda m: self.parse_raw_message(m["contents"]), unread_messages))
            
        return unread_messages

    
    async def mark_as_read(self, thread_id: int, message_id: int) -> bool:
        """Marks a message as read from a thread

        Args:
            thread_id (int): RR chat thread ID
            message_id (int): RR chat message ID

        Returns:
            bool: Successful or not
        """
        
        resp = await self.bot.RecNet.rec_net.custom("https://chat.rec.net/").thread(thread_id).message(message_id).read.make_request("post", headers=await self.get_headers())
        return resp.success
    
    
    async def send_dm(self, text: str, account_id: int) -> Optional[dict]:
        """Sends a direct message with RecNet's chat API

        Args:
            text (str): Message content
            account_id (int): Player ID to send to

        Returns:
            Optional[dict]: Response if successful
        """
        
        # Generate the payload
        message = self.generate_message(text)
        payload = f"ids={account_id}&messageContents={message}"
        
        # Get headers
        headers = await self.get_headers()
        
        # Update the content type
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        
        # Send the message
        resp = await self.bot.RecNet.rec_net.custom("https://chat.rec.net/").thread.make_request("post", headers=headers, body=payload)
        result = resp.data
        
        # Check if successful
        if result["chatResult"] != 0: return None
        
        # Get the thread
        thread = result["chatThread"]
        
        # Mark as read
        await self.mark_as_read(thread["chatThreadId"], thread["lastReadMessageId"])
        
        return result
    
    
    async def send_thread_msg(self, messages: List[str], thread_id: int) -> Optional[dict]:
        """Sends a thread message with RecNet's chat API

        Args:
            messages (List[str]) Messages to send
            thread_id (int): Thread ID to send to

        Returns:
            Optional[dict]: Message if successful
        """
        
        # Safety
        if not messages: return None
        
        # Generate the payload
        payload = ""
        for text in messages:
            payload += f"msg={self.generate_message(text)}&"
            
        # Get headers
        headers = await self.get_headers()
        
        # Update the content type
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        
        # Send the message
        resp = await self.bot.RecNet.rec_net.custom("https://chat.rec.net/").thread(thread_id).bulk.make_request("post", headers=headers, body=payload)
        if not resp.success: return None  # failure
        
        # Get the first result
        result = resp.data[0]
    
        # Check if successful
        if result["chatResult"] != 0: return None
        
        # Get the message
        message = result["chatMessage"]
        
        # Mark as read
        await self.mark_as_read(message["chatThreadId"], message["chatMessageId"])
        
        return message
        
    
    async def accept_friend_requests(self) -> List[int]:
        """Accepts all friend requests

        Returns:
            List[int]: Accepted player ids
        """
        
        # Get headers for authorized requests
        headers = await self.get_headers()

        # Get notifications
        resp = await self.bot.RecNet.rec_net.api.messages.v3.get.make_request("get", headers=headers, params={"forWebsite": "true", "take": 16**2})
        if not resp.success: return []
        
        # Accept friend requests
        accepted_ids = []
        for notif in resp.data["Results"]:
            # Get the player's ID
            account_id = notif["FromPlayerId"]
            
            # Check if someone else accepted friend request
            if notif["Type"] == 40:
                accepted_ids.append(account_id)
                
            # Check if it's a friend request
            elif notif["Type"] == 4:
                # Check if it's a linked account
                method = "post" if self.bot.cm.get_rec_room_connection(rr_id=account_id) else "delete"
                
                # Accept or reject request
                resp = await self.bot.RecNet.rec_net.api.relationships.v3(account_id).make_request(method, headers=headers)
                if resp.success and method == "post": accepted_ids.append(account_id)
                
            # If it's some other notification
            else:
                continue
                
            # Delete the notification
            await self.bot.RecNet.rec_net.api.messages.v3(notif["Id"]).make_request("delete", headers=headers)       
        
        return accepted_ids
    
    
    async def send_friend_request(self, account_id: int) -> bool:
        """Sends a friend request

        Args:
            account_id (int): Who to friend

        Returns:
            bool: Success
        """
        resp = await self.bot.RecNet.rec_net.api.relationships.v3(account_id).make_request("post", headers=await self.get_headers())
        return resp.success
    
    
    def parse_raw_message(self, message: str) -> dict:
        """Parses a raw stringified message JSON to a dictionary

        Args:
            message (str): Raw message

        Returns:
            dict: Parsed dictionary
        """
        return json.loads(message)
    
    
    def parse_embeds(self, text: str) -> dict:
        """Parses room and account embeds from messages

        Args:
            text (str): Message text

        Returns:
            dict: Found embed ids
        """
        embeds = {}
        
        # Find possible account ids
        account_ids = re.findall("<\@U(\d*)\|", text)
        if account_ids:
            embeds["account"] = set(filter(None, account_ids))
            
        # Find possible room ids
        room_ids = re.findall("<\^R(\d*)\|", text)
        if room_ids:
            embeds["room"] = set(filter(None, room_ids))
        
        return embeds
    
    
    def create_account_embed(self, account_id: int, username: str) -> str:
        """Generates an account embed for RR chats

        Args:
            account_id (int): An account's id
            username (str): The account's username

        Returns:
            str: RR account chat embed
        """
        return f"<@U{account_id}|{username}>"
    
    
    def create_account_details(self, account: Account, matchmaking: dict = None) -> str:
        """Takes an account dataclass and turns it into a short description about the account.

        Args:
            account (Account): RecNetPy account
            matchmaking (dict) Optional matchmaking data for more info

        Returns:
            str: Accounts details
        """
        creation_date = datetime.utcfromtimestamp(account.created_at).strftime('%d %B, %Y')
        embed = self.create_account_embed(account.id, account.username)
        junior_status = "🍼" if account.is_junior else "🔞"
        
        # Start with account name and junior status
        fields = [
            f"{embed} • {account.display_name} {junior_status}",
        ]
        
        # Include platforms if any
        if account.platforms:
            fields.insert(1, ", ".join(account.platforms))
        
        if matchmaking:
            # Add latest platform
            if matchmaking['deviceClass'] > 0 and matchmaking['deviceClass'] < len(DEVICE_CLASS):
                fields.insert(-1, f"Last played on {DEVICE_CLASS[matchmaking['deviceClass']]}!")
            
            # Add last online date if visibility allows
            if matchmaking["statusVisibility"] == 0 and not matchmaking["isOnline"] and matchmaking["lastOnline"]:
                last_online_timestamp = date_to_unix(matchmaking["lastOnline"])
                last_online_date = datetime.utcfromtimestamp(last_online_timestamp).strftime('%d %B, %Y %I %p %Z')
                fields.insert(-1, f"Last seen at {last_online_date}")
            
        # Add creation date last
        fields.append(f"Created at {creation_date}")
        
        return "\n".join(fields)
    
    
    @tasks.loop(seconds=5)
    async def update(self):
        # Accept all friend requests
        ids = await self.accept_friend_requests()
        
        # Send an introduction to just added people
        for account_id in ids:
            await self.send_dm("Hey! You can send me @usernames for details.", account_id)
            print(f"Added id:{account_id}")
            
        # Leave inactive threads
        await self.leave_inactive_threads()
        
        # Respond to messages
        unread = await self.get_threads(unread_only=True)
        for thread in unread:
            # Get unread messages
            messages = await self.get_unread_messages(thread["chatThreadId"], thread["lastReadMessageId"], contents_only=True)
            if not messages: continue
            
            # Get any embeds
            embeds = list(map(lambda m: self.parse_embeds(m["Data"]), messages))
            
            # Build the response
            response, accounts, rooms, matchmaking = [], [], [], []
            for e in embeds:
                for em, ids in e.items():
                    match em:
                        case "room":  # if it's a room embed
                            rooms = await self.bot.RecNet.rooms.fetch_many(ids)
                        case "account":  # if it's an account embed
                            accounts = await self.bot.RecNet.accounts.fetch_many(ids)
                            resp = await self.bot.RecNet.rec_net.custom("https://match.rec.net/player").make_request("post", body={"id": ids}, headers=await self.get_headers())
                            matchmaking = resp.data
                        case _:
                            continue
            
            # Build account details
            for (a, m) in zip(accounts, matchmaking):
                response.append(self.create_account_details(a, m))
                
            if response:
                await self.send_thread_msg(response, thread["chatThreadId"])
                print("SENT", response)
            else:
                await self.send_thread_msg(["No player embeds found!"], thread["chatThreadId"])
                print("SENT No player embeds found!")
        
        
    @update.before_loop
    async def before_tracking(self):
        await self.bot.wait_until_ready()
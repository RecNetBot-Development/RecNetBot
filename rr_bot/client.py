import json
import urllib.parse
from recnetlogin import RecNetLoginAsync
from discord.ext import tasks
from typing import List, Optional

class Client():
    def __init__(self, bot, username: str, password: str):
        # RecNetBot
        self.bot = bot
        
        # Credentials for the bot
        self.username = username
        self.password = password
        self.login = None  # Filled in start()
        
        # temporary
        self.account_id = 81111229
        
        
    async def start(self) -> bool:
        """Initializes and starts the in-game RecNetBot

        Returns:
            bool: Success
        """
        if self.username and self.password:
            self.login = RecNetLoginAsync(username=self.username, password=self.password)
            if not await self.login.get_token(): return False
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
    
    
    async def get_unread_messages(self, thread_id: int, latest_thread_msg_id: int) -> list:
        """Fetches all the unread messages

        Returns:
            list: Raw, unread messages
        """
        
        # Fetch messages
        resp = await self.bot.RecNet.rec_net.custom("https://chat.rec.net/").thread(thread_id).message.make_request("get", headers=await self.get_headers(), params={"MessageCount": 5, "Mode": 0})
        if not resp.success: return []
        
        # Get unread messages
        unread_messages = list(filter(lambda m: m["chatMessageId"] > latest_thread_msg_id and int(m["senderPlayerId"]) != int(self.account_id), resp.data))
        
        # Return as oldest first
        return unread_messages.reverse()

    
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
    
    
    async def send_thread_msg(self, text: str, thread_id: int) -> Optional[dict]:
        """Sends a thread message with RecNet's chat API

        Args:
            text (str): Message content
            thread_id (int): Thread ID to send to

        Returns:
            Optional[dict]: Message if successful
        """
        
        # Generate the payload
        message = self.generate_message(text)
        payload = f"msg={message}"

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
            # Check if it's a friend request
            if notif["Type"] != 4: continue
            
            # Get the player's ID
            account_id = notif["FromPlayerId"]
            
            # Accept request
            resp = await self.bot.RecNet.rec_net.api.relationships.v3(account_id).make_request("post", headers=headers)
            if resp.success: accepted_ids.append(account_id)
            
            # Delete the notification
            await self.bot.RecNet.rec_net.api.messages.v3(notif["Id"]).make_request("delete", headers=headers)       
        
        return accepted_ids
    
    
    @tasks.loop(seconds=5)
    async def update(self):
        # Accept all friend requests
        ids = await self.accept_friend_requests()
        
        # Send an introduction to just added people
        for account_id in ids:
            await self.send_dm("hey!", account_id)
            
        # Leave inactive threads
        await self.leave_inactive_threads()
        
        # Respond to messages
        unread = await self.get_threads(unread_only=True)
        for thread in unread:
            messages = await self.get_unread_messages(thread["chatThreadId"], thread["lastReadMessageId"])
            for msg in messages:
                msg = await self.send_thread_msg(msg["chatMessageId"], msg["chatThreadId"])
        
        
    @update.before_loop
    async def before_tracking(self):
        await self.bot.wait_until_ready()
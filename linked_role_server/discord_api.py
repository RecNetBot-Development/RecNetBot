import uuid
import urllib.parse
import requests
import time
import storage
from config_ import CONFIG

# Code specific to communicating with the Discord API.

# The following methods all facilitate OAuth2 communication with Discord.
# See https://discord.com/developers/docs/topics/oauth2 for more details.

class Discord:
    def __init__(self, discord_client_id, discord_redirect_uri, discord_client_secret):
        self.DISCORD_CLIENT_ID = discord_client_id
        self.DISCORD_REDIRECT_URI = discord_redirect_uri
        self.DISCORD_CLIENT_SECRET = discord_client_secret

    # Generate the url which the user will be directed to in order to approve the
    # bot, and see the list of requested scopes.
    def get_oauth_url(self):
        state = str(uuid.uuid4())

        url = 'https://discord.com/api/oauth2/authorize'
        params = {
            "client_id": self.DISCORD_CLIENT_ID,
            "redirect_uri": self.DISCORD_REDIRECT_URI,
            "response_type": "code",
            "state": state,
            "scope": "role_connections.write identify",
            "prompt": "consent"
        }
        return (url + urllib.parse.urlencode(params), state)


    # Given an OAuth2 code from the scope approval page, make a request to Discord's
    # OAuth2 service to retreive an access token, refresh token, and expiration.
    def get_oauth_tokens(self, code):
        url = "https://discord.com/api/v10/oauth2/token"
        body = {
            "client_id": self.DISCORD_CLIENT_ID,
            "client_secret": self.DISCORD_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.DISCORD_REDIRECT_URI
        }

        response = requests.post(
            url, 
            params=body, 
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )

        if response.ok:
            data = response.json()
            return data
        else:
            print(f"Error fetching OAuth tokens: [{response.status_code}]")


    # The initial token request comes with both an access token and a refresh
    # token.  Check if the access token has expired, and if it has, use the
    # refresh token to acquire a new, fresh access token.
    def get_access_token(self, user_id, tokens):
        if time.time() > tokens["expires_at"]:
            url = "https://discord.com/api/v10/oauth2/token"
            body = {
                "client_id": self.DISCORD_CLIENT_ID,
                "client_secret": self.DISCORD_CLIENT_SECRET,
                "grant_type": "refresh_token",
                "refrest_token": tokens["refresh_token"]
            }
            
            response = requests.post(
                url, 
                params=body, 
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            if response.ok:
                new_tokens = response.json()
                new_tokens["access_token"] = tokens["access_token"]
                new_tokens["expires_at"] = time.time() + tokens["expires_at"] * 1000
                storage.store_discord_tokens(user_id, new_tokens)
                return new_tokens["access_token"]
            else:
                print(f"Error refreshing access token: [{response.status_code}]")
        return tokens["access_token"]
    

    # Given a user based access token, fetch profile information for the current user.
    def get_user_data(self, tokens): 
        url = "https://discord.com/api/v10/oauth2/@me"
        response = requests.get(
            url, 
            headers={"Authorization": f"Bearer {tokens['access_token']}"}
        )
        if response.ok:
            data = response.json()
            return data
        else:
            print(f"Error fetching user data: [{response.status_code}]")
    

    # Given metadata that matches the schema, push that data to Discord on behalf
    # of the current user.
    def push_metadata(self, user_id, tokens, metadata):
        # GET/PUT /users/@me/applications/:id/role-connection
        url = f"https://discord.com/api/v10/users/@me/applications/{self.DISCORD_CLIENT_ID}/role-connection"
        access_token = self.get_access_token(user_id, tokens)
        body = {
            "platform_name": "Rec Room Account",
            "metadata": metadata
        }
        response = requests.put(url, 
            json=body, 
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )
        if not response.ok:
            print(f"Error pushing discord metadata: [{response.status_code}]")

    
    # Fetch the metadata currently pushed to Discord for the currently logged
    # in user, for this specific bot.
    def get_metadata(self, user_id, tokens):
        # GET/PUT /users/@me/applications/:id/role-connection
        url = f"https://discord.com/api/v10/users/@me/applications/{self.DISCORD_CLIENT_ID}/role-connection"
        access_token = self.get_access_token(user_id, tokens)
        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        if response.ok:
            data = response.json()
            return data
        else:
            print(f"Error getting discord metadata: [{response.status_code}]")

DISCORD = Discord(CONFIG.DISCORD_CLIENT_ID, CONFIG.DISCORD_REDIRECT_URI, CONFIG.DISCORD_CLIENT_SECRET)
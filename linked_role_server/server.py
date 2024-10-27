from flask import Flask, redirect, request, Response, make_response
from discord_api import DISCORD
from config_ import CONFIG
import storage
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = CONFIG.COOKIE_SECRET

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# Route configured in the Discord developer console which facilitates the
# connection between Discord and any additional services you may use. 
# To start the flow, generate the OAuth2 consent dialog url for Discord, 
# and redirect the user there.
@app.route("/linked-role")
def linked_role():
    url, state = DISCORD.get_oauth_url()

    # Store the signed state param in the user's cookies so we can verify
    # the value later. See:
    # https://discord.com/developers/docs/topics/oauth2#state-and-security
    response = make_response()
    response.set_cookie(
        key="client_state", 
        value=state, 
        max_age=1000 * 60 * 5
    )

    # Send the user to the Discord owned OAuth2 authorization endpoint
    return redirect(url)
    

# Route configured in the Discord developer console, the redirect Url to which
# the user is sent after approving the bot for their Discord account. This
# completes a few steps:
# 1. Uses the code to acquire Discord OAuth2 tokens
# 2. Uses the Discord Access Token to fetch the user profile
# 3. Stores the OAuth2 Discord Tokens in Redis / Firestore
# 4. Lets the user know it's all good and to go back to Discord
@app.route("/discord-oauth-callback")
def discord_oauth_callback():
    try:
        # 1. Uses the code to acquire Discord OAuth2 tokens
        code = request.args.get("code")
        discord_state = request.args.get("state")

        # Make sure state parameter exists
        client_state = request.cookies
        if client_state != discord_state:
            print("State verification failed.")
            return Response(status=403)
        
        tokens = DISCORD.get_oauth_tokens(code)

        # 2. Uses the Discord Access Token to fetch the user profile
        metadata = DISCORD.get_user_data(tokens)
        user_id = metadata["user"]["id"]
        storage.store_discord_tokens(user_id, {
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "expires_at": time.time() + tokens["expires_in"] * 1000
        })

        # 3. Stores the OAuth2 Discord Tokens in Redis / Firestore
        update_metadata(user_id)
        return "You did it!  Now go back to Discord."
    except Exception as error:
        print(error)
        return Response(status=500)


# Example route that would be invoked when an external data source changes. 
# This example calls a common `update_metadata` method that pushes static
# data to Discord.
@app.route("/update-metadata", methods=["POST"])
def update_metadata_route():
    try:
        user_id = request.form.get("user_id")
        update_metadata(user_id)
        return Response(status=204)
    except Exception as error:
        return Response(status=500)
    
# Given a Discord UserId, push static make-believe data to the Discord 
# metadata endpoint. 
def update_metadata(user_id):
    # Fetch the Discord tokens from storage
    tokens = storage.get_discord_tokens(user_id)
    metadata = {}
    try:
        # Fetch the new metadata you want to use from an external source. 
        # This data could be POST-ed to this endpoint, but every service
        # is going to be different.  To keep the example simple, we'll
        # just generate some random data. 

        metadata = {
            "rr_level": 50,
            "rr_creation_date": "2019-05-16"
        }
    except Exception as error:
        print("Error fetching external data", error)
        # If fetching the profile data for the external service fails for any reason,
        # ensure metadata on the Discord side is nulled out. This prevents cases
        # where the user revokes an external app permissions, and is left with
        # stale linked role data.

    # Push the data to Discord.
    DISCORD.push_metadata(user_id, tokens, metadata)


if __name__ == '__main__':
    app.run()

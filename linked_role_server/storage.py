store = {}

def store_discord_tokens(user_id, tokens):
    store[f"discord-{user_id}"] = tokens

def get_discord_tokens(user_id):
    return store[f"discord-{user_id}"]
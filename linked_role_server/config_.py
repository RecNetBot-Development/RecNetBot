import json
from dataclasses import dataclass

@dataclass
class Config:
    DISCORD_TOKEN: str
    DISCORD_CLIENT_ID: int
    DISCORD_CLIENT_SECRET: str
    DISCORD_REDIRECT_URI: str
    COOKIE_SECRET: str
    
path = "../config/{}.json"
with open(path.format("development"), 'r') as cfg_json:
    temp_config = json.load(cfg_json)

CONFIG = Config(
    temp_config["discord_token"],
    temp_config["discord_client_id"],
    temp_config["discord_client_secret"],
    temp_config["discord_redirect_uri"],
    temp_config["cookie_secret"]
)
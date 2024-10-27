import requests
import json
import sys
from enum import Enum


# Register the metadata to be stored by Discord. This should be a one time action.
# Note: uses a Bot token for authentication, not a user token.

class RoleMetadataType(Enum):
    INTEGER_LESS_THAN_OR_EQUAL = 1
    INTEGER_GREATER_THAN_OR_EQUAL = 2
    INTEGER_EQUAL = 3
    INTEGER_NOT_EQUAL = 4
    DATETIME_LESS_THAN_OR_EQUAL = 5
    DATETIME_GREATER_THAN_OR_EQUAL = 6
    BOOLEAN_EQUAL = 7
    BOOLEAN_NOT_EQUAL = 8


def load_config(is_production: bool = False) -> dict:
    path = "../config/{}.json"
    with open(path.format("production" if is_production else "development"), 'r') as cfg_json:
        config = json.load(cfg_json)

    return config

def register_metadata(is_production: bool) -> None:
    CONFIG = load_config(is_production=is_production)
    DISCORD_CLIENT_ID = CONFIG["discord_client_id"]
    DISCORD_TOKEN = CONFIG["discord_token"]

    url = f"https://discord.com/api/v10/applications/{DISCORD_CLIENT_ID}/role-connections/metadata"
    body = [
    {
        "key": 'rr_level',
        "name": 'Level',
        "description": 'Required Rec Room account level',
        "type": RoleMetadataType.INTEGER_GREATER_THAN_OR_EQUAL.value,
    },
    {
        "key": 'rr_creation_date',
        "name": 'Creation Date',
        "description": 'Days since Rec Room account creation',
        "type": RoleMetadataType.DATETIME_GREATER_THAN_OR_EQUAL.value,
    },
    ]

    response = requests.put(
        url,
        json = body,
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bot {DISCORD_TOKEN}",
    },
    )

    if response.ok:
        data = response.json()
        print(data, "\nSUCCESS!!")
    else:
        data = response.text()
        print(data, "\Failure..!!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Specify which config to use: python register.py [development/production]")
        sys.exit()
    if sys.argv[1] not in ("development", "production"):
        print("Specify which config to use: python register.py [development/production]")
        sys.exit()
    
    is_production = sys.argv[1] == "production"
    print(f"Registering metadata with {sys.argv[1]} configuration...")
    register_metadata(is_production=is_production)

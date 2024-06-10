import json

def format_json_block(raw_json: dict) -> str:
    """
    Formats raw json data into a json block that is sent to Discord
    """
    
    formatted = json.dumps(raw_json, indent=4, separators=(",", ": "))
    return f"```json\n{formatted.replace('`', '')}```"  # Get rid of ` to prevent escaping
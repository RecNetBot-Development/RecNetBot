import json

def load_config(is_production: bool = False) -> dict:
    path = "./config/{}.json"
    with open(path.format("production" if is_production else "development"), 'r') as cfg_json:
        config = json.load(cfg_json)

    return config
import json


def read_config_json(json_path):
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError as e:
        print(e)
        return None
    except json.JSONDecodeError as e:
        print(e)
        return None
    return data

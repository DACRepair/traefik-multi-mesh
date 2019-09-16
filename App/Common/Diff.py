import json


def dict_diff(new, exist):
    exist = exist[list(exist.keys())[0]]
    return json.dumps(new, sort_keys=True) == json.dumps(exist, sort_keys=True)

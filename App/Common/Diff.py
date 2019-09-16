import json


def dict_diff(new, exist):
    exist = exist[exist.keys[0]]
    return json.dumps(new, sort_keys=True) == json.dumps(exist, sort_keys=True)

#
#  Bot Json module
#  Lainupcomputer
#
import json


def read():  # Read Json File
    with open("storage/config.json", "r") as f:
        config = json.load(f)
    return config


def get(cfg, var):  # Get Data from Json
    config = read()
    data = config[str(cfg)][var]
    return data


def edit(cfg, data, value):  # Edit Data
    if cfg is None:
        cfg = "bot_config"
    config = read()
    config[str(cfg)][data] = value
    with open("storage/config.json", "w") as f:
        json.dump(config, f)

#
#  Bot Json module
#  Lainupcomputer
#
import json


def save(file):
    with open("config.json", "w") as f:
        json.dump(file, f, indent=2)


def read():  # Read Json File
    with open("config.json", "r") as f:
        config = json.load(f)
    return config


def get(cfg=None, var=None):  # Get Data from Json
    if cfg is None:
        cfg = "Bot"
    config = read()
    data = config[str(cfg)][var]
    return data


def edit(cfg=None, data=None, value=None):  # Edit Data
    if cfg is None:
        cfg = "bot_config"
    config = read()
    config[str(cfg)][data] = value
    with open("config.json", "w") as f:
        json.dump(config, f)

#
# Bot Config Creator
# Lainupcomputer
#
import json


# Create config file


def config_laden():
    with open("config.json", "r") as f:
        config = json.load(f)
    return config


def save(file):
    with open("config.json", "w") as f:
        json.dump(file, f, indent=2)


def channel():
    cfg = "Channel"
    f = config_laden()
    f[str(cfg)] = {}
    f[str(cfg)]["join_channel"] = 0
    f[str(cfg)]["stats_channel"] = 0
    f[str(cfg)]["log_channel"] = 0
    save(f)


def essential():
    cfg = "Bot"
    f = config_laden()
    f[str(cfg)] = {}
    f[str(cfg)]["token"] = "token not set"
    f[str(cfg)]["guild"] = 0
    f[str(cfg)]["prefix"] = "?"
    save(f)


def settings():
    cfg = "Settings"
    f = config_laden()
    f[str(cfg)] = {}
    f[str(cfg)]["join_message"] = True
    save(f)


essential()
channel()
settings()

import time
from const import io


def check():
    try:
        with open("installed", "r") as f:
            return True
    except:
        return False


def inst():
    f = open("installed", "w+")
    f.write(f"{time.time()}\n")


def check_installed():
    installed = check()
    print("Welcome to Darklegend\n")
    print("Checking Installation:\n")
    t = io.get(cfg="Bot", var="token")
    if len(t) >= 5:
        print("Token:Valid")
        if installed:
            inst()
            print("Bot starting up")
            return True
        else:
            print("This seems to be the first start.")
            print("Creating Data...")
            inst()
            print("Start me again")

    else:
        print("Token:Invalid")
        print("edit configfile: \"storage/config.json\"")
        print("Get Help: https://github.com/Lainupcomputer/DarkLegend")







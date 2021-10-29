from const import io


def check():
    try:
        with open("config.json", "r") as f:
            return True
    except FileNotFoundError:
        f = open("config.json", "w+")
        f.write("{\n\n}")
        print("[-] config not found:")
        print("[/] creating data....\n")
        print("[!] RESTART")
        return False


def check_installed():
    print("[*] Darklegend Alpha V2:\n")
    print("[*] Checking Installation:")
    installed = check()
    if installed:
        print("[?] checking token:")
        try:
            token = io.get(var="token")
            if len(token) >= 10:
                print("[+] token: valid\n")
                print("[+] bot starting up")
                return True

        except KeyError:
            print("[!] token:invalid")
            print("[*] edit configfile: \"config.json\"")
            print("[*] get help: https://github.com/Lainupcomputer/DarkLegend")
            y_n = input("open config helper? Y/n")
            if y_n == "":
                helper()
            return False


def create():
    f = io.read()
    f[str("Bot")] = {}
    f[str("Bot")]["token"] = ""
    f[str("Bot")]["guild"] = 0
    f[str("Bot")]["server_name"] = ""
    f[str("Bot")]["prefix"] = "?"
    f[str("Channel")] = {}
    f[str("Channel")]["join_channel"] = 0
    f[str("Channel")]["stats_channel"] = 0
    f[str("Channel")]["report_channel"] = 0
    f[str("Channel")]["support_channel"] = 0
    io.save(f)


def helper():
    print("Config Editor:\n")
    y_n = input("create blanc ? y/N")
    if y_n == "":
        token = input("Enter: token")
        guild = input("Enter: guild id")
        guild_name = input("Enter: guild name")
        join_channel = input("Enter: join channel")
        stats_channel = input("Enter: stats channel")
        report_channel = input("Enter: report channel")
        support_channel = input("Enter: support channel")
        f = io.read()
        f[str("Bot")] = {}
        f[str("Bot")]["token"] = token
        f[str("Bot")]["guild"] = int(guild)
        f[str("Bot")]["server_name"] = guild_name
        f[str("Bot")]["prefix"] = "?"
        f[str("Channel")] = {}
        f[str("Channel")]["join_channel"] = int(join_channel)
        f[str("Channel")]["stats_channel"] = int(stats_channel)
        f[str("Channel")]["report_channel"] = int(report_channel)
        f[str("Channel")]["support_channel"] = support_channel
        io.save(f)
        print("Done")

    else:
        create()





















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
            return False
















import discord
import datetime




def report_embed(ctx, reason, update_time):
    embed = discord.Embed(title="REPORT",
                          colour=discord.Colour(0x35aa0a),
                          description=f"{ctx.author.name} reported: {reason} Channel: {ctx.channel.name}",
                          timestamp=datetime.datetime.utcfromtimestamp(update_time))

    return embed


def support_embed():
    embed = discord.Embed(title="Support:",
                          colour=discord.Colour(0x35aa0a),
                          description="Du brauchst Hilfe oder willst einen Administrator sprechen ?\n"
                                      "Reagiere um ein Gespräch mit einem Administrator zu beginnen.")

    return embed


def umfrage_embed(update_time, topic):
    embed = discord.Embed(title="Umfrage:",
                          colour=discord.Colour(0x35aa0a),
                          description=f"{topic}",
                          timestamp=datetime.datetime.utcfromtimestamp(update_time))
    return embed



def verify_embed(servername):

    embed = discord.Embed(title=f"Willkommen bei {servername}",
                          description="**Die wesentlichen Informationen des Server:**\n Reagiere um Zugang zu den Bereichen zu erhalten.", color=discord.Colour.dark_purple())
    embed.add_field(name="[💻] Computer", value="Computer-Hilfe, Beratung, Fehlerbehebung, Talk")

    embed.add_field(name="[🎮] Gaming", value="League of legends, Minecraft, Warframe, Valorant")

    embed.add_field(name="[📕] Regeln", value="Die Regeln Findest du unter Regeln: ")
    embed.set_thumbnail(url="http://server-dltv.de/dltv.png")

    return embed


def game_role_embed(bot):
    for i in bot.guilds:
        mc = discord.utils.get(i.emojis, name="Minecraft")
        league = discord.utils.get(i.emojis, name="League")
        wf = discord.utils.get(i.emojis, name="Warframe")
        valo = discord.utils.get(i.emojis, name="Valorant")
    embed = discord.Embed(title=f"Du interessierst dich für Spiele ?",
                          description="Reagiere um eine Spielegruppe zu abbonieren.", color=discord.Colour.dark_green())
    embed.add_field(name=f"Minecraft: {mc} ", value="Betrete unseren Server.\n Tipps und Tricks.", inline=False)
    embed.add_field(name=f"League of Legends: {league}", value="Finde Mitspieler.\n Sieh dir Patches an.", inline=False)
    embed.add_field(name=f"Warframe: {wf}", value="Besuche den Clan der Fluffyuinikornz.\n Austausch von Builds.", inline=False)
    embed.add_field(name=f"Valorant: {valo}", value="Was soll ich hier schreiben ?", inline=False)
    embed.set_thumbnail(url="http://server-dltv.de/dltv.png")

    return embed


def rule_embed():
    embed = discord.Embed(title=f"Regeln",
                          description="Regeln.", color=discord.Colour.dark_purple())
    embed.set_thumbnail(url="http://server-dltv.de/dltv.png")
    embed.add_field(name="1 Namensgebung",
                    value="Der Nickname sollte dem erwünschten Rufnamen entsprechen. Nicknames dürfen keine beleidigenden Inhalte enthalten.")
    embed.add_field(name="2 Avatar",
                    value="Avatare dürfen keine pornographischen, rassistischen, beleidigenden oder andere gegen das deutsche Recht verstoßenden Inhalte beinhalten.")
    embed.add_field(name="3 Umgangston",
                    value="Der Umgang mit anderen Discord-Benutzern sollte stets freundlich sein. Verbale Angriffe gegen andere User sind strengstens untersagt.")
    embed.add_field(name="4 Kicken/Bannen",
                    value="Ein Kick oder Bann ist zu keinem Zeitpunkt unbegründet, sondern soll zum Nachdenken der eigenen Verhaltensweise anregen. Unangebrachte Kicks/Banns müssen den zuständigen Admins gemeldet werden.")
    embed.add_field(name="5 Upload von Dateeien",
                    value="Es ist nicht gestattet pornographisches, rassistisches oder rechtlich geschütztes Material hochzuladen und/oder mit anderen Benutzern zu tauschen.")
    embed.add_field(name="6 Streitigkeiten",
                    value="Private Missverständnisse und Streitigkeiten sind auch privat zu behalten und gehören nicht auf den Discord. Es gibt keine Ausnahmen!")
    embed.add_field(name="7 Werbung",
                    value="Auf unserem Server ist es nicht Erlaubt Werbung eigener Server zu senden oder zu verbreiten.")
    embed.add_field(name="Hinweise:",
                    value="Bei Verstoß gegen die Regeln werden von einem unserer Moderatoren entsprechende Maßnahmen durchgesetzt (zum Beispiel eine Verwarnung). Nach 3 Verwarnungen erfolgt automatisch ein Permabann.")
    embed.add_field(name="..HAFTUNGSAUSSCHLUSS..",
                    value="Hiermit distanzieren wir uns ausdrücklich von allen Inhalten aller gelinkten Seiten \n"
                          "Wir übernehmen daher keinerlei Haftung in Hinsicht auf rechtsextreme, kinderpornografische oder sonstige kriminelle Inhalte")


    return embed



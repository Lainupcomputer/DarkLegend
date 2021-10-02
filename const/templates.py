import discord
import datetime


def stats_embed(update_time, boost_level, total_channel, member):

    embed = discord.Embed(title="Server Stats",
                          colour=discord.Colour(0x35aa0a), url="http://darklegendstv.de/",
                          description="Server Stats: 🅳🅰🆁🅺🅻🅴🅶🅴🅽🅳🆂🆃🆅",
                          timestamp=datetime.datetime.utcfromtimestamp(update_time))
    embed.set_thumbnail(url="https://server-dltv.de/dltv.png")
    embed.add_field(name="Member:", value=f"{member}")
    embed.add_field(name="Channel:", value=f"{total_channel}")
    embed.add_field(name="Boost Level:", value=f"{boost_level}")
    return embed


def warn_embed(update_time, member, count, first_warning):
    if first_warning:
        text = f"{member.mention} That's not cool you has been warned for the first time!"
    else:
        text = f"{member.mention} This is your {count} warning, rethink your behavior. "
    embed = discord.Embed(title="User has been warned!",
                          colour=discord.Colour.red(),
                          description=f"{text}",
                          timestamp=datetime.datetime.utcfromtimestamp(update_time))
    embed.set_thumbnail(url="https://server-dltv.de/dltv.png")
    embed.add_field(name="Warnings:", value=f"{count}")
    return embed


def welcome_dm_embed(update_time):  # the welcome message the bot will send the user via dm
    embed = discord.Embed(title="Willkommen auf 🅳🅰🆁🅺🅻🅴🅶🅴🅽🅳🆂🆃🆅",
                          colour=discord.Colour(0x35aa0a), url="http://darklegendstv.de/",
                          description="Willkommen, Bitte lese dir die Regeln durch.",
                          timestamp=datetime.datetime.utcfromtimestamp(update_time))
    embed.set_thumbnail(url="https://server-dltv.de/dltv.png")
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


def welcome_channel_embed(user, update_time):  # the welcome message the bot will send in channel
    user_creation = user.created_at
    embed = discord.Embed(title=user.name, description=" Joined", colour=discord.Colour.green(),
                          timestamp=datetime.datetime.utcfromtimestamp(update_time))
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="User:", value=user.mention, inline=True)
    embed.add_field(name="Account created: ", value=user_creation, inline=True)
    embed.add_field(name="ID:", value=user.id, inline=True)
    return embed


def member_remove_embed(user, update_time):
    embed = discord.Embed(title=f"{user.name} has Left.",
                          colour=discord.Colour(0x35aa0a),
                          description=f"The {user.name} is no longer a part of this Community.",
                          timestamp=datetime.datetime.utcfromtimestamp(update_time))
    return embed


def report_embed(ctx, reason, update_time):
    embed = discord.Embed(title="REPORT",
                          colour=discord.Colour(0x35aa0a),
                          description=f"{ctx.author.name} reported: {reason} Channel: {ctx.channel.name}",
                          timestamp=datetime.datetime.utcfromtimestamp(update_time))

    return embed


def support_embed(payload, update_time):
    embed = discord.Embed(title="Support:",
                          colour=discord.Colour(0x35aa0a),
                          description=f"{payload.member.mention} requested Support.",
                          timestamp=datetime.datetime.utcfromtimestamp(update_time))
    return embed


def umfrage_embed(update_time, topic):
    embed = discord.Embed(title="Umfrage:",
                          colour=discord.Colour(0x35aa0a),
                          description=f"{topic}",
                          timestamp=datetime.datetime.utcfromtimestamp(update_time))
    return embed


def user_embed(ctx, update_time, member):
    embed = discord.Embed(title=member.name, description=member.mention, color=discord.Colour.green(),
                          timestamp=datetime.datetime.utcfromtimestamp(update_time))
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Beigetreten", value=member.joined_at, inline=True)
    embed.add_field(name="Höchste Rolle", value=member.top_role, inline=True)
    embed.add_field(name="Rollen", value=member.roles, inline=True)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Angefordert: {ctx.author.name}")
    return embed


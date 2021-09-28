import discord
import datetime


def stats_embed(update_time):

    #  Generate Embed
    online = None
    offline = None
    total_channel = None
    boost_level = None

    embed = discord.Embed(title="Server Stats",
                          colour=discord.Colour(0x35aa0a), url="http://darklegendstv.de/",
                          description="Server Stats: 🅳🅰🆁🅺🅻🅴🅶🅴🅽🅳🆂🆃🆅",
                          timestamp=datetime.datetime.utcfromtimestamp(update_time))
    embed.set_thumbnail(url="https://server-dltv.de/dltv.png")
    embed.add_field(name="Online:", value=f"{online}")
    embed.add_field(name="Offline:", value=f"{offline}")
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


def welcome_dm_embed(user, update_time):  # the welcome message the bot will send the user via dm
    embed = discord.Embed(title="Willkommen auf 🅳🅰🆁🅺🅻🅴🅶🅴🅽🅳🆂🆃🆅",
                          colour=discord.Colour(0x35aa0a), url="http://darklegendstv.de/",
                          description="Server Stats: 🅳🅰🆁🅺🅻🅴🅶🅴🅽🅳🆂🆃🆅",
                          timestamp=datetime.datetime.utcfromtimestamp(update_time))
    embed.set_thumbnail(url="https://server-dltv.de/dltv.png")
    embed.add_field(name="User:", value=user.mention, inline=True)
    return embed


def welcome_channel_embed(user, update_time):  # the welcome message the bot will send in channel
    user_creation = user.created_at
    embed = discord.Embed(title=user.name, description="Beigetreten", colour=discord.Colour.green())
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="User:", value=user.mention, inline=True)
    embed.add_field(name="Account created: ", value=user_creation, inline=True)
    embed.add_field(name="ID:", value=user.id, inline=True)


def member_remove_embed(user, update_time):
    embed = discord.Embed(title="Willkommen auf 🅳🅰🆁🅺🅻🅴🅶🅴🅽🅳🆂🆃🆅",
                          colour=discord.Colour(0x35aa0a), url="http://darklegendstv.de/",
                          description="Server Stats: 🅳🅰🆁🅺🅻🅴🅶🅴🅽🅳🆂🆃🆅",
                          timestamp=datetime.datetime.utcfromtimestamp(update_time))
    embed.set_thumbnail(url="https://server-dltv.de/dltv.png")
    embed.add_field(name="User:", value=user.mention, inline=True)
    return embed


def report_embed(ctx, reason, update_time):
    embed = discord.Embed(title="Willkommen auf 🅳🅰🆁🅺🅻🅴🅶🅴🅽🅳🆂🆃🆅",
                          colour=discord.Colour(0x35aa0a), url="http://darklegendstv.de/",
                          description="Server Stats: 🅳🅰🆁🅺🅻🅴🅶🅴🅽🅳🆂🆃🆅",
                          timestamp=datetime.datetime.utcfromtimestamp(update_time))
    embed.set_thumbnail(url="https://server-dltv.de/dltv.png")
    embed.add_field(name="User:", value=user.mention, inline=True)
    return embed

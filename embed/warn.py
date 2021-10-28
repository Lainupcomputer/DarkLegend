import discord
import datetime

thumbnail = "http://server-dltv.de/dltv.png"


def warn_embed(update_time, member, first_warning):
    if first_warning:
        text = f"{member.mention} That's not cool you has been warned for the first time!"
    else:
        text = f"{member.mention} This is your last warning, rethink your behavior. "
    embed = discord.Embed(title="User has been warned!",
                          colour=discord.Colour.red(),
                          description=f"{text}",
                          timestamp=datetime.datetime.utcfromtimestamp(update_time))
    embed.set_thumbnail(url=thumbnail)
    return embed


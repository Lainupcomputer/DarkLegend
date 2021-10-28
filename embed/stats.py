import discord
import datetime

thumbnail = "http://server-dltv.de/dltv.png"


def stats_embed(update_time, boost_level, total_channel, member):

    embed = discord.Embed(title="Server Stats",
                          colour=discord.Colour(0x35aa0a),
                          description="🆃🅴🅲🅷🅲🆁🅴🆆",
                          timestamp=datetime.datetime.utcfromtimestamp(update_time))
    embed.set_thumbnail(url=thumbnail)
    embed.add_field(name="Member:", value=f"{member}")
    embed.add_field(name="Channel:", value=f"{total_channel}")
    embed.add_field(name="Boost Level:", value=f"{boost_level}")
    return embed

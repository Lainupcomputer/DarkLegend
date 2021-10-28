import discord
import datetime

thumbnail = "http://server-dltv.de/dltv.png"


def welcome_dm_embed():  # the welcome message the bot will send the user via dm
    embed = discord.Embed(title="Willkommen auf 🆃🅴🅲🅷🅲🆁🅴🆆",
                          colour=discord.Colour(0x35aa0a), url=thumbnail,
                          description="Bitte lese dir die Regeln durch.\n"
                                      "Den Regeln muss zugestimmt werden, bevor du hier aktiv werden kannst.")
    embed.set_thumbnail(url=thumbnail)

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

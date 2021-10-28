import discord


def system_embed(msg):
    embed = discord.Embed(title=f"System Message",
                          description=f"{msg}", color=discord.Colour.dark_purple())

    return embed

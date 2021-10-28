import discord
import datetime


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


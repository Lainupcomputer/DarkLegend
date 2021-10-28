from embed import system
from const import io
import asyncio
import discord
import datetime


def report_embed(ctx, reason, update_time):
    embed = discord.Embed(title="Someone Reported:",
                          color=discord.Colour.dark_purple(),
                          description=f"{ctx.author.name} reported:",
                          timestamp=datetime.datetime.utcfromtimestamp(update_time))

    embed.add_field(name="Channel", value=f"{ctx.channel.mention}", inline=False)
    embed.add_field(name="Message:", value=f"{reason}", inline=False)
    return embed


async def report(bot, ctx, reason, update_time):
    if reason is None:
        return await ctx.send(embed=system.system_embed("Where is the problem?"))
    await bot.get_channel(io.get(cfg="Channel", var="report_channel")).send(embed=report_embed(ctx, reason, update_time)
                                                                            )
    await ctx.send(embed=system.system_embed("Your report has been sent."))
    await asyncio.sleep(2)
    await ctx.channel.purge(limit=2)

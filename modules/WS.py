import aiofiles
from embed import system, warn

warnings = {}


async def initialise(bot):
    for guild in bot.guilds:
        async with aiofiles.open("modules/warnings", mode="a") as temp:
            pass
        warnings[guild.id] = {}

    for guild in bot.guilds:
        async with aiofiles.open("modules/warnings", mode="r") as file:
            lines = await file.readlines()

            for line in lines:
                data = line.split(" ")
                member_id = int(data[0])
                admin_id = int(data[1])
                reason = " ".join(data[2:]).strip("\n")

                try:
                    warnings[guild.id][member_id][0] += 1
                    warnings[guild.id][member_id][1].append((admin_id, reason))
                    return warnings

                except KeyError:
                    warnings[guild.id][member_id] = [1, [(admin_id, reason)]]
                    return warnings


async def warn_user(ctx, member, reason, update_time):
    if member is None:
        await ctx.send(embed=system.system_embed("missing member"))

    if reason is None:
        await ctx.send(embed=system.system_embed("missing reason"))

    try:
        first_warning = False
        warnings[ctx.guild.id][member.id][0] += 1
        warnings[ctx.guild.id][member.id][1].append((ctx.author.id, reason))

    except KeyError:
        first_warning = True
        warnings[ctx.guild.id][member.id] = [1, [(ctx.author.id, reason)]]

    async with aiofiles.open("modules/warnings", mode="a") as file:
        await file.write(f"{member.id} {ctx.author.id} {reason}\n")
    await ctx.channel.purge(limit=1)
    await ctx.send(embed=warn.warn_embed(update_time, member, first_warning))



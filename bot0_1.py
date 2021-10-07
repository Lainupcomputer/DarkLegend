import discord
from discord.ext import commands
from const import io, help, checks, templates
import random
import asyncio
import aiofiles
import time

# Setup
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=io.get(cfg="Bot", var="prefix"), help_command=None, intents=intents)
bot.reaction_roles = []
bot.warnings = {}
bot.ticket_configs = {}


@bot.event  # Startup Task
async def on_ready():
    async with aiofiles.open("storage/ticket", mode="a") as temp:
        pass

    async with aiofiles.open("storage/ticket", mode="r") as file:
        lines = await file.readlines()
        for line in lines:
            data = line.split(" ")
            bot.ticket_configs[int(data[0])] = [int(data[1]), int(data[2]), int(data[3])]

    async with aiofiles.open("storage/reaction_roles", mode="a") as temp:  # create if not exists
        pass

    for guild in bot.guilds:
        async with aiofiles.open("storage/warnings", mode="a") as temp:
            pass
        bot.warnings[guild.id] = {}

    for guild in bot.guilds:
        async with aiofiles.open("storage/warnings", mode="r") as file:
            lines = await file.readlines()

            for line in lines:
                data = line.split(" ")
                member_id = int(data[0])
                admin_id = int(data[1])
                reason = " ".join(data[2:]).strip("\n")

                try:
                    bot.warnings[guild.id][member_id][0] += 1
                    bot.warnings[guild.id][member_id][1].append((admin_id, reason))

                except KeyError:
                    bot.warnings[guild.id][member_id] = [1, [(admin_id, reason)]]

    async with aiofiles.open("storage/reaction_roles", mode="r") as file:  # open, read, append
        lines = await file.readlines()
        for line in lines:
            data = line.split(" ")
            bot.reaction_roles.append((int(data[0]), int(data[1]), data[2].strip("\n")))
            pass

    bot.loop.create_task(status_task())  # Update Discord Status
    print("Bot Started")


@bot.event  # create warning list
async def on_guild_join(guild):
    bot.warnings[guild.id] = {}


@bot.event  # Reaction add
async def on_raw_reaction_add(payload):
    global category
    for role_id, msg_id, emoji in bot.reaction_roles:
        if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode("utf-8")):
            await payload.member.add_roles(bot.get_guild(payload.guild_id).get_role(role_id))
            return

    if payload.member.id != bot.user.id and str(payload.emoji) == u"\U0001F3AB":  # Ticket System
        msg_id, channel_id, category_id = bot.ticket_configs[payload.guild_id]

        if payload.message_id == msg_id:
            guild = bot.get_guild(payload.guild_id)

            for category in guild.categories:
                if category.id == category_id:
                    break

            channel = guild.get_channel(channel_id)
            ticket_channel = await category.create_text_channel(f"{payload.member.display_name}´s Ticket",
                                                                topic=f"ticket for {payload.member.display_name}.",
                                                                permission_synced=True)

            await bot.get_channel(io.get(cfg="Channel", var="support_channel")).send(embed=templates.support_embed(payload,
                                                                                                                   update_time=time.time()))

            await ticket_channel.set_permissions(payload.member, read_messages=True, send_messages=True)
            message = await channel.fetch_message(msg_id)
            await message.remove_reaction(payload.emoji, payload.member)

            await ticket_channel.send(
                f"{payload.member.mention} Thank you for creating a ticket! Use **'-close'** to close your ticket.")

            try:
                await bot.wait_for("message", check=lambda
                    m: m.channel == ticket_channel and m.author == payload.member and m.content == "-close",
                                   timeout=3600)

            except asyncio.TimeoutError:
                await ticket_channel.delete()

            else:
                await ticket_channel.delete()


@bot.command()
async def configure_ticket(ctx, msg: discord.Message = None, category: discord.CategoryChannel = None):
    if msg is None or category is None:
        await ctx.channel.send("Failed to configure the ticket as an argument was not given or was invalid.")
        return

    bot.ticket_configs[ctx.guild.id] = [msg.id, msg.channel.id, category.id]  # this resets the configuration

    async with aiofiles.open("storage/ticket", mode="r") as file:
        data = await file.readlines()

    async with aiofiles.open("storage/ticket", mode="w") as file:
        await file.write(f"{ctx.guild.id} {msg.id} {msg.channel.id} {category.id}\n")

        for line in data:
            if int(line.split(" ")[0]) != ctx.guild.id:
                await file.write(line)
    await msg.add_reaction(u"\U0001F3AB")
    await ctx.channel.send("OK")
    await asyncio.sleep(1)
    await ctx.channel.purge(limit=2, check=checks.is_not_pinned)


@bot.event  # reaction remove
async def on_raw_reaction_remove(payload):
    for role_id, msg_id, emoji in bot.reaction_roles:
        if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode("utf-8")):
            guild = bot.get_guild(payload.guild_id)
            await guild.get_member(payload.user_id).remove_roles(guild.get_role(role_id))
            return


@bot.event  # member join
async def on_member_join(user):
    if io.get(cfg="Settings", var="join_message"):  # Check if enabled
        await user.send(embed=templates.welcome_dm_embed(update_time=time.time()))
        await bot.get_channel(io.get(cfg="Channel",
                                     var="join_channel")).send(embed=templates.welcome_channel_embed(user,
                                     update_time=time.time()))


@bot.event
async def on_member_remove(member):
    if io.get(cfg="Settings", var="join_message"):  # Check if enabled
        await bot.get_channel(io.get(cfg="Channel",
                                     var="join_channel")).send(embed=templates.member_remove_embed(user=member,
                                     update_time=time.time()))

@bot.command()
async def umfrage(ctx, *, topic):
    msg = await ctx.send(embed=templates.umfrage_embed(update_time=time.time(),topic=topic))
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")


@bot.command()
async def hilfe(ctx):
    await ctx.channel.purge(limit=1)
    current = 0
    init_dl = 0
    msg = await ctx.send(embed=help.help_pages[current])
    for button in help.buttons:
        await msg.add_reaction(button)

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add",
                                                check=lambda reaction,
                                                user: user == ctx.author and reaction.emoji in help.buttons,
                                                timeout=60.0)
        except asyncio.TimeoutError:
            pass

        else:
            previous_page = current
            if reaction.emoji == "🔎":
                current = 0
            elif reaction.emoji == "🎲":
                current = 1
            elif reaction.emoji == "💰":
                current = 2
            elif reaction.emoji == "🎶":
                current = 3
            elif reaction.emoji == "⚙":
                current = 4
            elif reaction.emoji == "🗑":
                init_dl = 1

            for button in help.buttons:
                await msg.remove_reaction(button, ctx.author)
            if current != previous_page:
                await msg.edit(embed=help.help_pages[current])

            if init_dl == 1:
                await ctx.channel.purge(limit=1)


@bot.command()
async def Münze(ctx):
    options = ["Kopf", "Zahl"]
    choice = random.choice(options)
    await ctx.send(f"Die Münze wurde geworfen es ist: {choice}")


@bot.command()
@commands.has_permissions(administrator=True)
async def logout(ctx):
    await ctx.send("Bot logged out.")
    await bot.logout()


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amt=2):
    member = ctx.author
    deleted = await ctx.channel.purge(limit=amt, check=checks.is_not_pinned)
    await ctx.channel.send(member.mention + "**{} Nachrichten gelöscht.**".format(len(deleted)))


@bot.command()
@commands.has_permissions(administrator=True)
async def rr(ctx, role: discord.Role = None, msg: discord.Message = None, emoji=None):
    if role is None:
        return await ctx.send("Enter Role id.")
    if msg is None:
        return await ctx.send("Enter message id.")
    if emoji is None:
        return await ctx.send("Enter Emoji")
    if role != None and msg != None and emoji != None:
        await msg.add_reaction(emoji)
        bot.reaction_roles.append((role.id, msg.id, str(emoji.encode("utf-8"))))

        async with aiofiles.open("storage/reaction_roles", mode="a") as file:
            emoji_utf = emoji.encode("utf-8")
            await file.write(f"{role.id} {msg.id} {emoji_utf}\n")

        await ctx.channel.send("reaction Role created.")

    else:
        await ctx.send("ERROR.")


@bot.command()  # Warn a User
@commands.has_permissions(administrator=True)
async def warn(ctx, member: discord.Member = None, *, reason=None):
    if member is None:
        return await ctx.send("Enter User.")

    if reason is None:
        return await ctx.send("Reason required.")

    try:
        first_warning = False
        bot.warnings[ctx.guild.id][member.id][0] += 1
        bot.warnings[ctx.guild.id][member.id][1].append((ctx.author.id, reason))

    except KeyError:
        first_warning = True
        bot.warnings[ctx.guild.id][member.id] = [1, [(ctx.author.id, reason)]]

    async with aiofiles.open("storage/warnings", mode="a") as file:
        await file.write(f"{member.id} {ctx.author.id} {reason}\n")
    await ctx.channel.purge(limit=1, check=checks.is_not_pinned)
    await ctx.send(embed=templates.warn_embed(update_time=time.time(), member=member, first_warning=first_warning,
                                              count=bot.warnings[ctx.guild.id][member.id][0]))


@bot.command()  # Show User warnings
@commands.has_permissions(administrator=True)
async def showwarn(ctx, member: discord.Member = None):
    if member is None:
        return await ctx.send("Insert a User!")
    embed = discord.Embed(title=f"warn list for: {member.name}", description="", colour=discord.Colour.red())
    try:
        i = 1
        for admin_id, reason in bot.warnings[ctx.guild.id][member.id][1]:
            admin = ctx.guild.get_member(admin_id)
            embed.description += f"**{i}** Admin: {admin.mention} Reason: *'{reason}'*.\n"
            i += 1

        await ctx.send(embed=embed)

    except KeyError:  # no warnings
        embed = discord.Embed(title=f" {member.name} is clean AF.", description="", colour=discord.Colour.red())
        await ctx.send(embed=embed)


@bot.command()  # Report
async def report(ctx, reason=None):
    if reason is None:
        return await ctx.send("Reason required.")
    embed = templates.report_embed(ctx, reason=reason, update_time=time.time())
    await bot.get_channel(io.get(cfg="Channel", var="report_channel")).send(embed=embed)
    await ctx.send("Your report has been sent.")
    await asyncio.sleep(2)
    await ctx.channel.purge(limit=2, check=checks.is_not_pinned)


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="Du wurdest Geckickt!"):
    await member.send("Du wurdest gekickt. Weil:"+ reason)
    await bot.get_channel(io.get(cfg="Channel",
                                 var="join_channel")).send(f"{member.mention} **Wurde von {ctx.author.mention} Gekickt**")
    await member.kick(reason=reason)


@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason="Du Wurdest Gebannt!"):
    await member.send("Du wurdest gebannt. Weil:"+reason)
    await bot.get_channel(io.get(cfg="Channel",
                                 var="join_channel")).send(f"{member.mention} **Wurde von {ctx.author.mention} Gebannt!**")
    await member.ban(reason=reason)


@bot.command()
@commands.has_permissions(kick_members=True)
async def info(ctx, member: discord.Member):
    await ctx.send(embed=templates.user_embed(ctx=ctx, member=member, update_time=time.time()))


@bot.command()
@commands.has_permissions(kick_members=True)
async def verify(ctx):
    await ctx.channel.purge(limit=1, check=checks.is_not_pinned)
    await ctx.send(embed=templates.verify_embed(servername=io.get(cfg="Bot", var="server_name")))


async def status_task():  # Display Discord Status
    embed = discord.Embed(title="Server Stats",
                          colour=discord.Colour(0x35aa0a),
                          description="Server Stats: LOADING")

    msg = await bot.get_channel(io.get(cfg="Channel", var="stats_channel")).send(embed=embed)

    while True:
        guild = bot.get_guild(io.get(cfg="Bot", var="guild"))
        boost_lvl = guild.premium_tier
        channel = len(guild.text_channels) + len(guild.voice_channels)
        members = len(guild.members)
        await bot.change_presence(activity=discord.Game('OK'), status=discord.Status.online)
        await asyncio.sleep(20)
        new = templates.stats_embed(update_time=time.time(), boost_level=boost_lvl, total_channel=channel, member=members)
        await msg.edit(embed=new)
        await bot.change_presence(activity=discord.Game('UPDATE'), status=discord.Status.online)
        await asyncio.sleep(10)


bot.run(io.get(cfg="Bot", var="token"))


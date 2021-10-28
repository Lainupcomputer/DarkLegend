import discord
from discord.ext import commands
from const import io, help, checks, templates, musikbot, installer
import asyncio
import time
from embed import system, user_info, stats, join_leave
from modules import RS, TS, WS, rep

# Setup
installed = installer.check_installed()
if installed:
    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(command_prefix=io.get(var="prefix"), help_command=None, intents=intents)
    bot.reaction_roles = []
    bot.warnings = {}
    bot.ticket_configs = {}


    @bot.event  # Startup Task
    async def on_ready():
        bot.reaction_roles = await RS.initialise()
        bot.ticket_configs = await TS.initialise()
        bot.warnings = await WS.initialise(bot)
        bot.loop.create_task(status_task())  # Update Discord Status
        print("Bot Started")


    @bot.event  # create warning list
    async def on_guild_join(guild):
        bot.warnings[guild.id] = {}


    @bot.event  # Reaction add
    async def on_raw_reaction_add(payload):
        await RS.check_reaction(bot, payload)
        await TS.check_reaction(bot, payload)


    @bot.event  # reaction remove
    async def on_raw_reaction_remove(payload):
        await RS.remove_reaction(bot, payload)


    @bot.command()
    async def configure_ticket(ctx, msg: discord.Message = None, category: discord.CategoryChannel = None):
        await TS.create_ticket(ctx, msg, category)


    @bot.event  # member join
    async def on_member_join(user):
        await user.send(embed=join_leave.welcome_dm_embed())
        await bot.get_channel(io.get(cfg="Channel", var="join_channel")).send(embed=join_leave.welcome_channel_embed(
            user, update_time=time.time()))


    @bot.event
    async def on_member_remove(member):
        await bot.get_channel(io.get(cfg="Channel",var="join_channel")).send(embed=join_leave.member_remove_embed(
            user=member, update_time=time.time()))


    @bot.command()
    async def poll(ctx, *, topic):
        msg = await ctx.send(embed=templates.umfrage_embed(update_time=time.time(), topic=topic))
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
    @commands.has_permissions(administrator=True)
    async def logout(ctx):
        await ctx.send(embed=system.system_embed("Bot logged out."))
        await bot.logout()


    @bot.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(ctx, amt=2):
        deleted = await ctx.channel.purge(limit=amt, check=checks.is_not_pinned)
        await ctx.channel.send(embed=system.system_embed(f"{ctx.author.mention} deleted {len(deleted)} messages."))


    @bot.command()
    @commands.has_permissions(administrator=True)
    async def create_reaction(ctx, role: discord.Role = None, msg: discord.Message = None, emoji=None):
        IO = await RS.create_reaction(role, msg, emoji)
        if IO:
            await ctx.send(embed=system.system_embed(msg="Reaction Role created."))
        else:
            await ctx.send(embed=system.system_embed(msg="Error creating Reaction Role."))


    @bot.command()
    @commands.has_permissions(administrator=True)
    async def warn(ctx, member: discord.Member = None, *, reason=None):
        await WS.warn_user(ctx, member, reason, update_time=time.time())


    @bot.command()  # Show User warnings
    @commands.has_permissions(administrator=True)
    async def warn_show(ctx, member: discord.Member = None):
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


    @bot.command()
    async def report(ctx, *, reason=None):
        await rep.report(bot, ctx, reason, update_time=time.time())


    @bot.command()
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, member: discord.Member, *, reason="Kicked by Admin: "):
        await bot.get_channel(io.get(cfg="Channel",
                                     var="join_channel")).send(embed=embed.system(f"{member.mention} **Was Kicked by "
                                                                                  f"{ctx.author.mention} **"))
        await member.kick(reason=reason + f"{ctx.author.mention} !")


    @bot.command()
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member, *, reason="The Ban Hammer has spoken!"):
        await bot.get_channel(io.get(cfg="Channel",
                                     var="join_channel")).send(embed=embed.system(f"{member.mention} **Was Banned by "
                                                                                  f"{ctx.author.mention} **"))
        await member.ban(reason=reason + f"{ctx.author.mention} !")


    @bot.command()
    @commands.has_permissions(kick_members=True)
    async def info(ctx, member: discord.Member):
        await ctx.send(embed=user_info.user_embed(ctx=ctx, member=member, update_time=time.time()))


    @bot.command()
    @commands.has_permissions(kick_members=True)
    async def embed(ctx, arg):
        if arg == "gamerole":
            await ctx.channel.purge(limit=1, check=checks.is_not_pinned)
            await ctx.send(embed=templates.game_role_embed(bot))
        if arg == "verify":
            await ctx.channel.purge(limit=1, check=checks.is_not_pinned)
            await ctx.send(embed=templates.verify_embed(servername=io.get(cfg="Bot", var="server_name")))
        if arg == "rules":
            await ctx.channel.purge(limit=1, check=checks.is_not_pinned)
            await ctx.send(embed=templates.rule_embed())
        if arg == "support":
            await ctx.send(embed=templates.support_embed())


    @bot.command()
    async def dj(ctx, arg=None, link=None):
        if arg is None:
            buttons = ["📑", "⏹", "⏯", "⏭", "🗑"]
            await ctx.channel.purge(limit=1)
            init_dl = 0
            msg = await ctx.send(embed=musikbot.dj_embed(update_time=time.time()))
            for button in buttons:
                await msg.add_reaction(button)
            while True:
                try:
                    reaction, user = await bot.wait_for("reaction_add",
                                                        check=lambda reaction,
                                                                     user: user == ctx.author and reaction.emoji in buttons,
                                                        timeout=60.0)
                except asyncio.TimeoutError:
                    pass

                else:

                    if reaction.emoji == "📑":
                        embed = await musikbot.que_status(update_time=time.time())
                        await msg.edit(embed=embed)
                    elif reaction.emoji == "⏹":
                        musikbot.stop(ctx)
                    elif reaction.emoji == "⏯":
                        musikbot.play_pause(ctx)
                    elif reaction.emoji == "⏭":
                        musikbot.skip()
                        await msg.edit(embed=embed)
                    elif reaction.emoji == "🗑":
                        init_dl = 1

                    for button in buttons:
                        await msg.remove_reaction(button, ctx.author)
                        # await msg.edit(embed=templates.dj_embed(update_time=time.time()))

                    if init_dl == 1:
                        await ctx.channel.purge(limit=1)
        if arg == "join":  # join channel
            await ctx.channel.purge(limit=1)
            await musikbot.join(ctx)
        if arg == "add":  # add to playlist

            if link is not None:
                await musikbot.add_que(ctx, link=link)
            else:
                await ctx.send("enter a valid link")
        if arg == "list":
            await ctx.channel.purge(limit=1)
            await ctx.send(embed=await musikbot.que_status(update_time=time.time()))
        if arg == "delete":  # clear playlist
            await ctx.channel.purge(limit=1)
            response = await musikbot.delete()
            await ctx.send(f"{response}")


    @bot.command()
    async def emoji(ctx, emojiname):
        for i in bot.guilds:
            emoji = discord.utils.get(i.emojis, name=emojiname)
            await ctx.send(f"{emoji}")

    async def status_task():  # Display Discord Status
        await bot.get_channel(io.get(cfg="Channel", var="stats_channel")).purge()
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
            new = stats.stats_embed(update_time=time.time(), boost_level=boost_lvl, total_channel=channel,
                                        member=members)
            await msg.edit(embed=new)
            await bot.change_presence(activity=discord.Game('UPDATE'), status=discord.Status.online)
            await asyncio.sleep(10)


    bot.run(io.get(var="token"))
else:
    pass

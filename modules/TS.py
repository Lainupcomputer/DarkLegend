import aiofiles
import asyncio
from const import io, templates
import time
import discord
import datetime

ticket_configs = {}


def support_embed(payload, update_time):
    embed = discord.Embed(title="Support:",
                          colour=discord.Colour(0x35aa0a),
                          description=f"{payload.member.mention} requested Support.",
                          timestamp=datetime.datetime.utcfromtimestamp(update_time))
    return embed


async def initialise():
    async with aiofiles.open("modules/ticket", mode="a") as temp:
        pass
    async with aiofiles.open("modules/ticket", mode="r") as file:
        lines = await file.readlines()
        for line in lines:
            data = line.split(" ")
            ticket_configs[int(data[0])] = [int(data[1]), int(data[2]), int(data[3])]
            return ticket_configs


async def create_ticket(ctx, msg, category):
    if msg is None or category is None:
        await ctx.channel.send("Failed to configure the ticket as an argument was not given or was invalid.")
        return

    ticket_configs[ctx.guild.id] = [msg.id, msg.channel.id, category.id]  # this resets the configuration

    async with aiofiles.open("modules/ticket", mode="r") as file:
        data = await file.readlines()

    async with aiofiles.open("modules/ticket", mode="w") as file:
        await file.write(f"{ctx.guild.id} {msg.id} {msg.channel.id} {category.id}\n")

        for line in data:
            if int(line.split(" ")[0]) != ctx.guild.id:
                await file.write(line)
    await msg.add_reaction(u"\U0001F3AB")
    await ctx.channel.send("OK")


async def check_reaction(bot, payload):
    if payload.member.id != bot.user.id and str(payload.emoji) == u"\U0001F3AB":  # Ticket System
        msg_id, channel_id, category_id = ticket_configs[payload.guild_id]

        if payload.message_id == msg_id:
            guild = bot.get_guild(payload.guild_id)

            for category in guild.categories:
                if category.id == category_id:
                    break

            channel = guild.get_channel(channel_id)
            ticket_channel = await category.create_text_channel(f"{payload.member.display_name}´s Ticket",
                                                                topic=f"ticket for {payload.member.display_name}.",
                                                                permission_synced=True)

            await bot.get_channel(io.get(cfg="Channel", var="support_channel")).send(
                embed=support_embed(payload,
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

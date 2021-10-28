import aiofiles

reaction_roles = []


async def initialise():
    async with aiofiles.open("modules/reaction_roles", mode="a") as temp:  # create if not exists
        pass
    async with aiofiles.open("modules/reaction_roles", mode="r") as file:  # open, read, append
        lines = await file.readlines()
        for line in lines:
            data = line.split(" ")
            reaction_roles.append((int(data[0]), int(data[1]), data[2].strip("\n")))
            return reaction_roles


async def check_reaction(bot, payload):
    for role_id, msg_id, emoji in reaction_roles:
        if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode("utf-8")):
            await payload.member.add_roles(bot.get_guild(payload.guild_id).get_role(role_id))
            return


async def remove_reaction(bot, payload):
    for role_id, msg_id, emoji in reaction_roles:
        if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode("utf-8")):
            guild = bot.get_guild(payload.guild_id)
            await guild.get_member(payload.user_id).remove_roles(guild.get_role(role_id))
            return


async def create_reaction(role, msg, emoji):
    if role is not None and msg is not None and emoji is not None:
        await msg.add_reaction(emoji)
        reaction_roles.append((role.id, msg.id, str(emoji.encode("utf-8"))))

        async with aiofiles.open("modules/reaction_roles", mode="a") as file:
            emoji_utf = emoji.encode("utf-8")
            await file.write(f"{role.id} {msg.id} {emoji_utf}\n")
            IO = True
            return IO

    else:
        IO = False
        return IO



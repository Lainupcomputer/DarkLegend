import aiofiles


async def initialise(bot):
    async with aiofiles.open("reaction_system/reaction_roles", mode="a") as temp:  # create if not exists
        pass
    async with aiofiles.open("reaction_system/reaction_roles", mode="r") as file:  # open, read, append
        lines = await file.readlines()
        for line in lines:
            data = line.split(" ")
            bot.reaction_roles.append((int(data[0]), int(data[1]), data[2].strip("\n")))
            return bot.reaction_roles


async def create_reaction(bot, role, msg, emoji):
    if role is not None and msg is not None and emoji is not None:
        await msg.add_reaction(emoji)
        bot.reaction_roles.append((role.id, msg.id, str(emoji.encode("utf-8"))))

        async with aiofiles.open("reaction_system/reaction_roles", mode="a") as file:
            emoji_utf = emoji.encode("utf-8")
            await file.write(f"{role.id} {msg.id} {emoji_utf}\n")
            IO = True
            return IO

    else:
        IO = False
        return IO




import discord
import discord.ext.commands
from better_profanity import profanity
import os
import json

warns = {}

with open("./warns.json", "r") as file:
    if file:
        warns = json.load(file)

bot = discord.ext.commands.Bot("c!")

@bot.listen()
async def on_message(message):
    if profanity.contains_profanity(message.content):
        #await message.edit(content=profanity.censor(message.content))
        await message.channel.send("Don't swear, " + message.author.mention + "! You have been warned.")
        warn(message.author)

@bot.command()        
async def warn(uid: discord.Member):
    global warns
    if warns[uid]:
        warns[uid] += 1
        if warns[uid] == 7:
            await uid.ban()
            await uid.send("You have been banned for gaining too many warns.")
        return
    warns[uid] = 1

bot.run(os.getenv("DISCORD_TOKEN"))

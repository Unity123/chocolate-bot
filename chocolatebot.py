import discord
import discord.ext.commands
from better_profanity import profanity
import os

bot = discord.ext.commands.Bot("c!")

@bot.listen()
async def on_message(message):
    if profanity.contains_profanity(message.content):
        #await message.edit(content=profanity.censor(message.content))
        await message.channel.send("Don't swear, " + message.author.mention + "! You have been warned.")
        
bot.run(os.getenv("DISCORD_TOKEN"))

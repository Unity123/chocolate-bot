import discord
import discord.ext.commands
from better_profanity import profanity
import os
import json

warns = {}

if os.path.exists("./warns.json"):
    with open("./warns.json", "r") as file:
        warns = json.load(file)

bot = discord.ext.commands.Bot("c!")

@bot.listen()
async def on_message(message):
    if profanity.contains_profanity(message.content):
        hook = await message.channel.create_webhook(name=message.author.nickname, avatar=message.author.avatar)
        await hook.send(profanity.censor(message.content, "#"))
        await message.delete() #message.edit(content=profanity.censor(message.content))
        await message.channel.send("Don't swear, " + message.author.mention + "! You have been warned.")
        await _warn(message.author, "Swearing")
        await hook.delete()

@bot.command()
@discord.ext.commands.has_permissions(kick_members=True)
async def warn(ctx, uid: discord.Member, reason="None"):
    await ctx.send("Warned " + uid.nickname + " for reason " + reason)
    await _warn(uid, str(reason))

@bot.command()
@discord.ext.commands.has_permissions(kick_members=True)
async def kick(ctx, uid: discord.Member, reason="None"):
    await ctx.send("Kicked " + uid.nickname + " for reason " + str(reason))
    await uid.send("You have been kicked from " + ctx.guild.name + ".\nReason: " + reason)
    await uid.kick()

@bot.command()
@discord.ext.commands.has_permissions(ban_members=True)
async def ban(ctx, uid: discord.Member, reason="None"):
    await ctx.send("Banned " + uid.nickname + " for reason " + str(reason))
    await uid.send("You have been banned from " + ctx.guild.name + ".\nReason: " + reason)
    await uid.ban()

@warn.error
@kick.error
async def error(error, ctx):
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send("You don't have the permissions to do that!")

async def _warn(uid: discord.Member, reason):
    global warns
    if uid in warns:
        warns[uid] += 1
            return
    else:
        warns[uid] = 1
    await uid.send("You have been warned.\nReason: " + reason + "\nYour warns: " + str(warns[uid]))
    if warns[uid] == 7:
        await uid.send("You have been banned from " + uid.guild.name + ".\nReason: Too many warns.")
        warns[uid] = 0
        await uid.ban()

@bot.event
async def on_disconnect():
    global warns
    with open("./warns.json", "w") as file:
        json.dump(warns, file)

@bot.event
async def on_ready():
    jeff = await bot.get_channel(906297627904192594).webhooks()
    jeff[0].delete()

bot.run(os.getenv("DISCORD_TOKEN")))

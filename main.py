import discord
from discord import utils
from discord.ext import commands
from config import start
import os
client = commands.Bot(command_prefix=start['prefix'], intents=discord.Intents.all()) #intents=discord.Intents.all()
blacklist=[]
@client.event
async def on_guild_join(guild):
    if guild.system_channel is not None:
        embed = discord.Embed(title="Hello, this is HouseStoreBot, I will help you to save stuff, just ask me!",
                              description="Use !help command to see my commands",

                              color=0xff00f6)
        await guild.system_channel.send(embed=embed)



@client.event
async def on_message(message):

    await client.process_commands(message)
    if message.author == client.user:
        return
    #comand mute
    for x in blacklist:
        if (x in message.content.upper()):
            await message.delete()
    if message.content=='save':
        for attach in message.attachments:
            if os.path.exists(f"path/{str(message.author)}"):
                await attach.save(f"path/{str(message.author)+'/'+attach.filename}")
            else:
                os.mkdir(f"path/{message.author}")
                await attach.save(
                    f"path/{str(message.author) + '/' + attach.filename}")
        await message.delete()
@client.command()
async def getall(ctx):
    a=os.listdir(f"path/{str(ctx.message.author)}")
    print(*a)
    for file in a:
        await ctx.message.author.send(file)
        await ctx.message.author.send(file=discord.File(f"/path/{str(ctx.message.author) + '/' + file}"))
@client.command()
async def get(ctx, filename):
    a = os.listdir(f"path/{str(ctx.message.author)}")
    print(*a)
    if filename in a:

        await ctx.message.author.send(file=discord.File(
            f"path/{str(ctx.message.author) + '/' + filename}"))
    else:
        embed = discord.Embed(title="No file found :(",
                              description="Use !getall to see the list of files.",

                              color=0xff00f6)
        await ctx.send(embed=embed)
@client.command()
async def givecontroll(ctx, user):
    message=ctx.message
    for attach in message.attachments:
        if os.path.exists(f"path/{str(message.author)+str(user)}"):
            await attach.save(
                f"path/{str(message.author) +str(user)+ '/' + attach.filename}")
        else:
            os.mkdir(f"Saves/{message.author}")
            await attach.save(
                f"path/{str(message.author) + '/' + attach.filename}")
client.run(start['token'])

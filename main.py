import json
import os

import discord
from dotenv import load_dotenv

fulldata = dict
load_dotenv()

bot = discord.Client(intents=discord.Intents.all())


@bot.event
async def on_ready():
    loaddata()
    print("connected")


@bot.event
async def on_message(ctx):
    dguild = ctx.author.guild
    if ctx.content == "a!toggleactivity":
        loaddata()
        if str(ctx.author.id) in fulldata["Active"]:
            del fulldata["Active"][str(ctx.author.id)]
            await ctx.reply("You are no longer in the player pool.")
        else:
            fulldata["Active"][str(ctx.author.id)] = "True"
            await ctx.reply("You are now in the player pool")

        savedata()

    elif ctx.content.startswith("a!search "):
        availablecount = 0
        available = []

        for member in dguild.members:
            if str(member.id) in fulldata["Active"]:
                if member.activity.name.upper() == ctx.content[9:].upper():
                    available.append(f"{member.name}#{member.discriminator} - <@{member.id}>")
                    availablecount += 1
        if availablecount == 0:
            embed = discord.Embed(
                title=f"Available {ctx.content[9:]} player:",
                description=f"There are currently no online members playing {ctx.content[9:]} in the player pool."
            )
        else:
            merge = "\n"
            embed = discord.Embed(
                title=f"Available {ctx.content[9:]} player:",
                description=f'{f"{merge}".join(str(e) for e in available)}\n'
            )

        await ctx.reply(embed=embed)

    elif ctx.content.startswith("a!globalsearch "):
        availablecount = 0
        available = []

        for guild in bot.guilds:
            for member in guild.members:
                if str(member.id) in fulldata["Active"]:
                    try:
                        if member.activity.name.upper() == ctx.content[15:].upper():
                            if f"{member.name}#{member.discriminator} - <@{member.id}>" not in available:
                                available.append(f"{member.name}#{member.discriminator} - <@{member.id}>")
                                availablecount += 1
                    except:
                        print(f"[LOG] Error while getting activity from user {member.name}.")
        if availablecount == 0:
            embed = discord.Embed(
                title=f"Available {ctx.content[15:]} player:",
                description=f"There are currently no online members playing {ctx.content[15:]} in the player pool."
            )
        else:
            merge = "\n"
            embed = discord.Embed(
                title=f"Available {ctx.content[15:]} player:",
                description=f'{f"{merge}".join(str(e) for e in available)}\n'
            )

        await ctx.reply(embed=embed)


# FUNCTIONS
def loaddata():
    with open("data.json", "r") as f:
        global fulldata
        fulldata = json.load(f)


def savedata():
    with open("data.json", "w") as f:
        global fulldata
        json.dump(fulldata, f, indent=4)


bot.run(os.getenv("TOKEN"))

from main import generate_meme
import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(intents=intents)


@bot.slash_command(name="meme", guild_ids=[1170471455146909757])
async def meme(ctx, description: str):
    await ctx.respond("working on it...")
    meme = generate_meme(description)
    if meme:
        await ctx.respond(file=discord.File(meme.name))
    else:
        await ctx.respond("couldn't make it work :( try again")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = str(message.content)
    if message.author.id == 193479248294445056:
        meme = generate_meme(f"nerd emoji glasses gif with caption '''\"{content}\"'''")
        if meme:
            await message.channel.send(file=discord.File(meme.name))
    print(content)


bot.run(open(".env", "r").read())

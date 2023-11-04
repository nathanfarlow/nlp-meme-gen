from main import generate_meme
import discord
from discord.ext import commands

bot = commands.Bot()


@bot.slash_command(name="meme", guild_ids=[1170471455146909757])
async def meme(ctx, description: str):
    await ctx.respond("working on it...")
    meme = generate_meme(description)
    if meme:
        await ctx.respond(file=discord.File(meme.name))
    else:
        await ctx.respond("couldn't make it work :( try again")


# listen for a user to send a message, and if they did, respond to it
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.author.id == 193479248294445056:
        meme = generate_meme(
            'nerd emoji with glasses gif with caption """message.content"""'
        )
        if meme:
            await message.channel.send(file=discord.File(meme.name))


bot.run(open(".env", "r").read())

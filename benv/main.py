from typing import Final
import os
import discord
from dotenv import load_dotenv
from discord import Intents, Client, Message
from discord.ext import commands
#Loading token from somewhere safe
load_dotenv()
TOKEN: Final[str] = os.getenv('BOT_TOKEN')

# Bot setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("Bot is ready.")
    await bot.load_extension("cogs.mod")
    await bot.load_extension("cogs.leaderboard") #have to load cogs first before tree sync
    print("Cogs loaded")
    await bot.tree.sync()


@bot.event
async def on_message(msg: discord.Message) :
	content = msg . content
	if content == "hello" :
		await msg. reply( "hii!")
	await bot.process_commands(msg) #msg will be processed by process commands too
	


@bot.command()
async def ping(ctx):
    await ctx.send("Hello!")

#For clear command 
@bot.tree.command()
@commands.has_permissions(manage_messages=True)
@commands.bot_has_permissions(manage_messages=True)
async def clear(inter: discord.Interaction, amount: int):
	"""Clears specified number of messages"""
	await inter.response.defer(thinking=True, ephemeral=True)
	await inter.channel.purge(limit=amount)
	await inter.followup.send(f"Deleted {amount} messages", ephemeral=True)


@clear.error # type: ignore
async def on_error(inter:discord.Interaction, error:commands.CommandError):
	if isinstance(error, commands.MissingPermissions):
		await inter.response.send_message("You don't have permission to use this command.", ephemeral=True)

bot.run(TOKEN) 
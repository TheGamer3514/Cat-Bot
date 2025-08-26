import discord
from discord.ext import commands, tasks
import asyncio
import requests
import os
import random
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None, description="A bot that sends cat images", case_insensitive=True)

statuses = [
    "Cats are super duper cute",
    "Meow! 🐾",
    "Send !cat for a cat pic",
    "Cats every few hours!",
    "Pet a cat today!"
]

status_index = 0

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    change_status.start()
    cat_task.start()

@tasks.loop(minutes=10)
async def change_status():
    global status_index
    activity = discord.CustomActivity(name=statuses[status_index])
    await bot.change_presence(activity=activity)
    status_index = (status_index + 1) % len(statuses)

cat_frequency_hours = 6
cat_channel_id = 1136257543174357082

@tasks.loop(hours=cat_frequency_hours)
async def cat_task():
    channel = bot.get_channel(cat_channel_id)
    if not channel:
        print("Channel not found!")
        return
    try:
        response = requests.get("https://api.thecatapi.com/v1/images/search", timeout=10)
        response.raise_for_status()
        json_data = response.json()
        url = json_data[0]['url']
        embed = discord.Embed(title="Cat images", description="Meow", color=0x00ff00)
        embed.set_image(url=url)
        embed.set_footer(text=f"Will send another cat image in {cat_frequency_hours} hours")
        await channel.send("<@&1136257572060536902>", embed=embed)
    except Exception as e:
        await channel.send(f"Couldn't fetch a cat image right now. Error: {e}")
# Help command
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Bot Commands", color=0x00ff00)
    embed.add_field(name="!cat", value="Send a random cat image.", inline=False)
    embed.add_field(name="!setcatfreq <hours>", value="Change how often cat images are sent automatically.", inline=False)
    embed.add_field(name="!sync", value="Sync the cat image channel to the current channel.", inline=False)
    embed.add_field(name="!help", value="Show this help message.", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def sync(ctx):
    global cat_channel_id
    cat_channel_id = ctx.channel.id
    await ctx.send(f"Cat images will now be sent to this channel (ID: {cat_channel_id}).")

@cat_task.before_loop
async def before_cat_task():
    await bot.wait_until_ready()

@bot.command()
async def cat(ctx):
    """Send a random cat image."""
    try:
        response = requests.get("https://api.thecatapi.com/v1/images/search", timeout=10)
        response.raise_for_status()
        json_data = response.json()
        url = json_data[0]['url']
        embed = discord.Embed(title="Cat images", description="Meow", color=0x00ff00)
        embed.set_image(url=url)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Couldn't fetch a cat image right now. Error: {e}")

@bot.command()
async def setcatfreq(ctx, hours: int):
    """Set how often cat images are sent automatically (hours)."""
    global cat_frequency_hours, cat_task
    if hours < 1 or hours > 24:
        await ctx.send("Please choose a value between 1 and 24 hours.")
        return
    cat_frequency_hours = hours
    cat_task.change_interval(hours=cat_frequency_hours)
    await ctx.send(f"Cat images will now be sent every {cat_frequency_hours} hours.")


TOKEN = "<YOUR_BOT_TOKEN>"  # <-- Replace with your actual bot token
bot.run(TOKEN)

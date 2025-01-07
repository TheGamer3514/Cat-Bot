import discord
from discord.ext import commands, tasks
import asyncio
import requests
intents = discord.Intents.all()
# Create a bot instance
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None, description="A bot that sends cat images every 6 hours", case_insensitive=True)

@bot.event
async def on_ready():
    #set status
    activity = discord.CustomActivity(
        name = "Cats are super duper cute",
    )
    await bot.change_presence(activity=activity)
    print(f'Logged in as {bot.user.name}')
    cat_task.start()
@tasks.loop(hours=6)
async def cat_task():
    channel = bot.get_channel(1136257543174357082)
    #get cat api
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    #get json from api
    json_data = response.json()
    #get url from json
    url = json_data[0]['url']
    #send message
    embed = discord.Embed(title="Cat images", description="Meow", color=0x00ff00)
    embed.set_image(url=url)
    embed.set_footer(text="Will send another cat image in 6 hours")
    await channel.send("<@&1136257572060536902>", embed=embed)

@cat_task.before_loop
async def before_cat_task():
    await bot.wait_until_ready()

# Run the bot
bot.run("TOKEN HERE")

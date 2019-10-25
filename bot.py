# Work with Python 3.6
import discord
from keys import TOKEN
from bs4 import BeautifulSoup as Soup
import requests

client = discord.Client()

URL = 'https://teamtrees.org'

        
@client.event
async def on_message(message):    
    if message.author == client.user:
        return
    
    
    r = requests.get(URL)
    s = Soup(r.content)
    trees = s.find(id='totalTrees')["data-count"]
    await message.author.send(f"Planted {trees} Trees! Awesome!")
    return

        
@client.event
async def on_ready():
    print('Logged in as:', client.user.name)
    print(client.user.id)
    print()
    get_anime_list.start()
    
client.run(TOKEN)
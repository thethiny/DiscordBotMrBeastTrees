# Work with Python 3.6
import discord
from keys import TOKEN
from bs4 import BeautifulSoup as Soup
import requests
from datetime import datetime

client = discord.Client()

URL = 'https://teamtrees.org'

def get_page():
    r = requests.get(URL)
    return Soup(r.content)

def get_count(s):
    return s.find(id='totalTrees')["data-count"]
    
def format_donation(s):
    message = None
    name = s[0]
    trees = s[1]
    time = str(datetime.fromisoformat(s[2].split('.')[0]).strftime('%d-%b-%Y %I:%m %p'))
    if len(s) == 4:
        message = s[3].strip()
    string = f"{name}: {trees}"
    if message:
        string += '\n' + message
    string += f"\n{time}\n"
    return string
    
def get_leaderboard(s, full=False):
    leaderboard = s.find(id='top-donations')
    donations = []
    for i, donation in enumerate(leaderboard.findAll(class_='media-body')):
        if full:
            string = format_donation(donation.text.strip().split('\n'))
        else:
            string = f"{i+1}: " + donation.text.strip().split('\n')[0]
        donations.append(string)
    
    return '\n'.join(donations)
    
    
        
@client.event
async def on_message(message):    
    if message.author == client.user:
        return
        
    if message.content.startswith("?treescount"):
        print(message.author, message.content)
        s = get_page()
        trees = get_count(s)
        await message.channel.send(f"Planted {trees} Trees! Awesome!")
    elif message.content.startswith("?treestop"):
        print(message.author, message.content)
        m = message.content.split()
        s = get_page()
        if len(m) == 1:
            donations = get_leaderboard(s)
            await message.channel.send(donations)
        else:
            if m[1].lower() == 'full':
                donations = get_leaderboard(s, True)
                await message.author.send(donations)
            else:
                await message.channel.send("Usage is:\n?treestop\n?treestop full")
    return

        
@client.event
async def on_ready():
    print('Logged in as:', client.user.name)
    print(client.user.id)
    print()
    
client.run(TOKEN)
from nextcord import Client, Intents, Interaction, SlashOption, HTTPException, Member,Embed
from typing import Optional
import urllib.request as http
import json
import time
import os

api = "https://api.minetools.eu/ping/thetechnodot.aternos.me/22744"
desc = r"\u00a7cWelcome to \u00a79TheSMP \u00a7cof \u00a7a{\u00a7o\u00a7kX\u00a7a\u00a7o\u00a7nTechnoDot\u00a7a\u00a7o\u00a7kX\u00a7a}\u00a7b!"
bot: Client = Client()
guild_ids: int = 990640712330649631

i = 0
members = ["TechnoDot#4398"]
for user_id in members:
  members[i] = bot.get_user(user_id)

@bot.event
async def on_ready():
  print('Successfully logged in')

@bot.event
async def on_member_join(user):
  if user in members:
    role = get(user.server.roles, name="Bot Test Role")
    await bot.add_roles(user, role) 

@bot.slash_command(name='hello', description='Says hello', guild_ids=[guild_ids])
async def hello(interaction: Interaction, user: Member):
  await interaction.send(f"Hello, {user}!")

@bot.slash_command(name='status', description='Checks server status of server', guild_ids=[guild_ids])
async def status(interaction: Interaction):
  running, online = False, []
  payload = json.loads(http.urlopen(api).read())
  if bool(payload.get("description")):
    running = True
  for user in payload.get('players').get("sample"):
    online.append(user.get("name"))
  
  if not running:
    offlineEmbed = Embed(title="Server is Offline", description='DM TechnoDot to start the server')
    await interaction.send(embed=offlineEmbed)
    return
  statusEmbed = Embed(
      title="Server Status",
      description="Join the server!"
  )
  player_online = payload.get("players").get('online')
  player_limit = payload.get('players').get('max')
  statusEmbed.add_field(name='Capacity', value=f'`{player_online}/{player_limit}`')
  newLine = '\n'
  player_array = [f'{index + 1}. {player}' for index, player in enumerate(online)]
  statusEmbed.add_field(name='Players', value=f"```{f'{newLine}'.join(player_array)}```", inline=False)
  await interaction.send(embed=statusEmbed)

try:
  bot.run(os.getenv("TOKEN"))
except HTTPException as e:
  if e.status == 429:
    print("Connection denied by Discord servers\nRestarting Repl in 3 seconds...")
    time.sleep(3)
    os.system("kill 1")
  else:
    print("Unknown error")

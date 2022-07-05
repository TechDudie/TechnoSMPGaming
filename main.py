from nextcord import (
    Client,
    Intents,
    Interaction,
    SlashOption,
    HTTPException,
    Member,
    Embed,
    utils,
    Color,
)
from typing import Optional
import urllib.request as http
from jsonHandler import readConfig
import json
import time
import os

intents = Intents.default()
intents.members = True
api = f"https://api.minetools.eu/ping/{readConfig('Url')}/{readConfig('Port')}"
desc = r"\u00a7cWelcome to \u00a79TheSMP \u00a7cof \u00a7a{\u00a7o\u00a7kX\u00a7a\u00a7o\u00a7nTechnoDot\u00a7a\u00a7o\u00a7kX\u00a7a}\u00a7b!"
bot: Client = Client(intents=intents)
guild_ids: list = readConfig("guildIds")


@bot.event
async def on_ready():
    print("Successfully logged in")


@bot.event
async def on_member_join(member: Member):
    roles_id = readConfig("OnJoinRolesID")
    for roleid in roles_id:
        await member.add_roles(utils.get(member.guild.roles, id=roleid))


@bot.slash_command(name="hello", description="Says hello", guild_ids=guild_ids)
async def hello(interaction: Interaction, user: Member):
    await interaction.send(f"Hello, {user}!")


@bot.slash_command(
    name="status", description="Checks server status of server", guild_ids=guild_ids
)
async def status(interaction: Interaction):
    payload = json.loads(http.urlopen(api).read())
    if payload.get("error"):
        embed = Embed(
            title="Server is Offline",
            description="DM TechnoDot to start the server",
            color=Color.red(),
        )

    if payload.get("description"):
        online = []
        for user in payload.get("players").get("sample"):
            online.append(user.get("name"))
        embed = Embed(
            title="Server Status", description="Join the server!", color=Color.green()
        )
        player_online, player_limit = payload.get("players").get("online"), payload.get(
            "players"
        ).get("max")
        statusEmbed.add_field(
            name="Capacity", value=f"`{player_online}/{player_limit}`"
        )
        newLine = "\n"
        player_array = [f"{index + 1}. {player}" for index, player in enumerate(online)]
        statusEmbed.add_field(
            name="Players",
            value=f"```{f'{newLine}'.join(player_array)}```",
            inline=False,
        )

    await interaction.send(embed=embed)


try:
    bot.run(os.environ['TOKEN'])
except HTTPException as e:
    if e.status == 429:
        print("Connection denied by Discord servers\nRestarting Repl in 3 seconds...")
        time.sleep(3)
        os.system("kill 1")
    else:
        print("Unknown error")

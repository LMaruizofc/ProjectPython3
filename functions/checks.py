import discord
import requests

from discord.ext import commands
from functions.defs import translates
from utils.loader import configData
from db.moderation import mod

class NoVote(commands.CheckFailure):
    ...

class ModuleDisable(commands.CheckFailure):
    ...

def vote():

    async def check(ctx: discord.Interaction) -> commands.check:

        t: dict = translates(ctx.guild)

        o = requests.get(headers = {"Authorization": configData['topauth']},url = f'https://top.gg/api/bots/1012121641947517068/check?userId={ctx.user.id}')

        if o.json()['voted'] == 0:
            raise NoVote(t['args']['notvote'])
        
        return True
    return commands.check(check)

def moduleCheck(nameModule: str):

    async def check(ctx: discord.Interaction) -> commands.check:

        t: dict = translates(ctx.guild)

        db = mod.find_one({"_id": ctx.guild.id})

        if db['modules'][nameModule] == False:
            raise ModuleDisable(t['args']['moduledisable'])

        return True
    return commands.check(check)
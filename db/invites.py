from pymongo import MongoClient
from utils.loader import configData

cluster = MongoClient(configData['mongokey'])

db = cluster[configData['database']]

invite = db['invites']

async def add_invite(guild,inviter, qnt):

    invite.update_one( { "_id": f'{guild.id}_{inviter.id}'}, {'$inc': {'qnt': qnt}}, upsert = True )
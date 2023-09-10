from pymongo import MongoClient
from utils.loader import configData

cluster = MongoClient(configData['mongokey'])

db = cluster[configData['database']]

mod = db['MOD']

payment = db['PAYMENT']

class dbmoderation:

    def lang(opt,oq,guild):

        if opt is not None:

            if mod.count_documents({"_id":guild.id}) == 0:

                mod.insert_one({"_id":guild.id, "Nome":guild.name})

            mod.update_one({"_id": guild.id}, {"$set": {f"{opt}": oq}}, upsert = True)

    def logs(opt,oq,guild,id):

        if opt is not None:

            if mod.count_documents({"_id":guild.id}) == 0:

                mod.insert_one({"_id":guild.id, "Nome":guild.name})

            mod.update_one({"_id": guild.id}, {'$set': {opt: {'True?': oq,'id': id}}},upsert = True)
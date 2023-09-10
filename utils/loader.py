import os, discord, json

from discord import Bot as BotBase

with open('utils/config.json') as f:
    configData = json.load(f)

class client(BotBase):

    def __init__(self):
        super().__init__(
            command_prefix = configData['prefix'],
            intents = discord.Intents(
                invites = True,
                guilds = True,
                members = True,
                emojis_and_stickers = True,
                guild_messages = True,
                message_content = True,
                dm_messages = False
            ),
            case_insensitive = True,
            help_command = None
        )

    def loadcogs(self):
        pastaname = 'cogs'
        for filename in os.listdir(f'./{pastaname}'):
            for file in os.listdir(f'./{pastaname}/{filename}'):
                if file.endswith('.py'):
                    self.load_extensions(f'{pastaname}.{filename}.{file[:-3]}')
    
    def __run__(self):

        self.loadcogs()

        self.run(configData['token'])
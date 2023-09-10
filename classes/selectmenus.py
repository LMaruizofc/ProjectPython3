import discord, hexacolors

from discord.ui import Select
from db.moderation import mod, dbmoderation
from functions.defs import translates

class setlang(Select):

    def __init__(self, bot, ctx, t):

        self.bot = bot

        self.ctx = ctx

        self.t = t

        super().__init__(
        placeholder= t['args']['lang']['lang'],
        options = [
            discord.SelectOption(
                label = 'pt-BR',
                description = t['args']['lang']['ptbr'],
                value = 'pt-br'
            ),
            discord.SelectOption(
                label = 'en-US',
                description = t['args']['lang']['eng'],
                value = 'en-us'
            )
        ])
    async def callback(self, interaction: discord.Interaction):...

        # match self.values[0]:

        #     case 'pt-br':

        #         if self.values[0] == mod.find_one({'_id':interaction.guild.id})['lang']:

        #             await interaction.response.send_message(self.t['args']['lang']['langequal'], ephemeral = True)

        #             return

        #         dbmoderation.lang('lang',self.values[0],interaction.guild)

        #         await interaction.response.send_message('Okay, agora falarei português', ephemeral = True)

        #     case 'en-us':

        #         if self.values[0] == mod.find_one({'_id':interaction.guild.id})['lang']:

        #             await interaction.response.send_message(self.t['args']['lang']['langequal'], ephemeral = True)

        #             return

        #         dbmoderation.lang('lang',self.values[0],interaction.guild)

        #         await interaction.response.send_message('ok now i will speak english', ephemeral = True)

class actvate(Select):

    def __init__(self, bot, ctx, guild, log):

        self.bot = bot

        self.ctx = ctx

        self.log = log

        t = translates(guild)

        super().__init__(

            placeholder= log,
            
            options = [

                discord.SelectOption(

                    label = t['args']['act'],
                    value = 'ativar'

                ),

                discord.SelectOption(

                    label = t['args']['dsb'],
                    value = 'desativar'

                ),

            ]
        )
    async def callback(self, interaction: discord.Interaction):

        t = translates(interaction.guild)

        db = mod.find_one({'_id': interaction.guild.id})

        match self.values[0]: 

            case 'ativar':

                await interaction.response.send_message(t['args']['sendid'], ephemeral = True)

                def check50(m):
                    
                    return m.content and m.author.id == interaction.user.id

                msg50 = await self.bot.wait_for('message', check = check50, timeout = 130)

                id = interaction.guild.get_channel(int(msg50.content.strip('< # >')))

                await msg50.delete()

                await interaction.channel.send(t['args']['sucessdef'], delete_after = 3)

                dbmoderation.logs(self.log,True,interaction.guild,id.id)
            
            case 'desativar':

                await interaction.response.send_message(t['args']['undef'], ephemeral = True)

                dbmoderation.logs(self.log,False,interaction.guild,None,None)

class setlog(Select):

    def __init__(self, bot, ctx, t):

        self.bot = bot

        self.ctx = ctx

        self.t = t

        super().__init__(
            placeholder= t['args']['mod']['log'],

            options = [

                discord.SelectOption(

                    label = t['args']['mod']['invitename'],
                    description = t['args']['mod']['invite'],
                    value = 'Invite'

                ),

                discord.SelectOption(

                    label = t['args']['mod']['invitenamecreate'],
                    description = t['args']['mod']['invitecreate'],
                    value = 'InviteCreate'

                ),

                discord.SelectOption(

                    label = t['args']['mod']['invitenamedelete'],
                    description = t['args']['mod']['invitedelete'],
                    value = 'InviteDelete'

                ),
            ]
        )
    async def callback(self, interaction : discord.Interaction):

        match self.values[0]:

            case 'Invite':

                await interaction.response.send_message(view = discord.ui.View(actvate(self.bot, interaction.user,interaction.guild,'LogInvite')), ephemeral = True)

            case 'InviteCreate':

                await interaction.response.send_message(view = discord.ui.View(actvate(self.bot, interaction.user,interaction.guild,'LogInviteCreate')), ephemeral = True)

            case 'InviteDelete':

                await interaction.response.send_message(view = discord.ui.View(actvate(self.bot, interaction.user,interaction.guild,'LogInviteDelete')), ephemeral = True)

class selecthelp(Select):

    def __init__(self, bot, ctx, t):

        self.bot = bot

        self.ctx = ctx

        self.t = t
    
        super().__init__(
        placeholder = t['help']['extras']['commands'],
        options = [
            discord.SelectOption(
                label =  t['help']['mod']['name1'],
                description =  t['help']['mod']['name2'],
                value = '0'
            ),
            discord.SelectOption(
                label =  t['help']['general']['name'],
                description =  t['help']['general']['description'],
                value = '1'
            ),
            discord.SelectOption(
                label =  t['help']['suport']['name'],
                description =  t['help']['suport']['description'],
                value = '2'
            )
        ]
    )
    async def callback(self, interaction: discord.Interaction):

        if interaction.user.id == self.ctx.id:

            match self.values[0]:

                case '0':

                    m = discord.Embed(title = self.t['help']['extras']['commands'],
                    description = self.t['help']['mod']['description'],
                    color = hexacolors.stringColor('steelblue'))

                    m.add_field(
                        name = self.t['help']['mod']['name1'],
                        value = self.t['help']['mod']['content'],
                        inline = False)
                    m.set_thumbnail(url = f'{self.bot.user.avatar}')

                    await interaction.response.edit_message(embed = m)

                case '1':

                    g = discord.Embed(title = self.t['help']['extras']['commands'],
                    color = hexacolors.stringColor('steelblue'))

                    g.add_field(
                        name = self.t['help']['general']['description'],
                        value = self.t['help']['general']['content'],
                        inline = False)
                    g.set_thumbnail(url = f'{self.bot.user.avatar}')

                    await interaction.response.edit_message(embed=g)

                case '2':

                    s = discord.Embed(title = self.t['help']['extras']['commands'],
                    color = hexacolors.stringColor('steelblue'))

                    s.add_field(
                        name = self.t['help']['suport']['description'], 
                        value = self.t['help']['suport']['content'],
                        inline = False)
                    s.set_thumbnail(url = f'{self.bot.user.avatar}')

                    await interaction.response.edit_message(embed=s)
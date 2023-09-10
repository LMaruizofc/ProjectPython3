import time
import discord
import hexacolors
import platform
from discord import slash_command
from discord.ext import commands
from classes.selectmenus import selecthelp
from functions.defs import translates


class gerais(commands.Cog):

    def __init__(self, bot:commands.Bot):

        self.bot = bot

    @slash_command(name='ping', description="Shows the bot's latency in ms.")
    async def ping(self, interaction: discord.Interaction):
        
        start_time: time = time.time()

        t: dict = translates(interaction.guild)

        Ping:int = round(self.bot.latency * 1000)

        end_time: time = time.time()

        p4: discord.Embed = discord.Embed(title = 'Ping', 

        description = f'{t["args"]["ping"]}: {Ping}ms\nAPI: {round((end_time - start_time) * 1000)}ms', color = hexacolors.stringColor('steelblue'))

        await interaction.response.send_message(embed = p4)
    
    @slash_command(
        guild_only = True,
        name = 'help',
        description = 'Help command InviterInfo',
        name_localizations = {
            'en-US': 'help',
            'pt-BR': 'ajuda',
        },
        description_localizations = {
            'en-US': 'Help command InviterInfo',
            'pt-BR': 'Comando de ajuda do InviterInfo',
        })
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx):

        t = translates(ctx.guild)

        h = discord.Embed(title =  t['help']['extras']['commands'],
        description = t['help']['extras']['init'],
        color = hexacolors.stringColor('steelblue'))
        h.set_thumbnail(url = self.bot.user.avatar)

        await ctx.response.send_message(embed = h, view = discord.ui.View(selecthelp(self.bot,ctx.author,t)))
    
    @slash_command(guild_only = True,name = 'vote', description = 'Envia o link para votar em mim no top.gg')
    @commands.cooldown(1,5,commands.BucketType.user)
    async def Vote(self, ctx):

        t = translates(ctx.guild)

        e1 = self.bot.get_emoji(972895959191289886)

        server = '[Server Suport](https://discord.com/invite/USMVRUcDGa)'

        top = f'[Top.gg](https://top.gg/bot/{self.bot.user.id})'

        inv = f'[Invite](https://discord.com/api/oauth2/authorize?client_id=1023217955556823130&permissions=414934461616&scope=bot%20applications.commands)'

        topgg = discord.Embed(title = 'Vote', 

        description = t['args']['topgg']['dsc'].format(ctx.author.mention))

        topgg.add_field(name = f':grey_question: {t["args"]["topgg"]["duvids"]}', value = server, inline = False)
        
        topgg.add_field(name = f'{e1} {t["args"]["topgg"]["cresc"]}', 
        
            value = top, inline = False)

        topgg.add_field(name = f':partying_face: {t["args"]["topgg"]["invite"]}', 

            value = inv, inline = False)

        topgg.set_thumbnail(url = self.bot.user.avatar.url)

        await ctx.response.send_message(embed = topgg)
    
    @slash_command(
        guild_only = True,
        name = 'invite',
        description = 'Envia o link para me convidar para seu server')
    @commands.cooldown(1,5, commands.BucketType.user)
    async def invite(self, ctx):

        t = translates(ctx.guild)
        
        e = discord.Embed(title = t['args']['invite']['invite'], 

        description = f'[{t["args"]["invite"]["dsc"]}](https://discord.com/api/oauth2/authorize?client_id=1023217955556823130&permissions=137976106113&scope=bot%20applications.commands)')

        e.set_thumbnail(url = self.bot.user.avatar)

        await ctx.response.send_message(embed=e)

    @slash_command(guild_only = True,name = 'bot_info', description = 'Envia algumas informações minha')
    @commands.cooldown(1,5, commands.BucketType.user)
    async def botinfo(self, ctx):

        t = translates(ctx.guild)

        python = self.bot.get_emoji(1044744677578002452)
        discord = self.bot.get_emoji(1044749602257125517)
        Vs = self.bot.get_emoji(1045113609488965662)
        name = self.bot.get_emoji(1045112581062393946)

        e = discord.Embed(title = t["args"]["commands"]["botinfo"]["mif"])
        e.set_thumbnail(url = self.bot.user.avatar.url)
        e.add_field(name = f'{name} {t["args"]["commands"]["botinfo"]["name"]}', value = self.bot.user.name, inline = True)
        e.add_field(name = f'{Vs} {t["args"]["commands"]["botinfo"]["language"]}', value = f'{python} Python', inline = True)
        e.add_field(name = '════════════', value = '════════════', inline = False)
        e.add_field(name = f'{discord} {t["args"]["commands"]["botinfo"]["version"]}', value = discord.__version__, inline = True)
        e.add_field(name = f'{python} {t["args"]["commands"]["botinfo"]["pyversion"]}', value = platform.python_version(), inline = True)
        e.add_field(name = '════════════', value = '════════════', inline = False)
        e.add_field(name = f':calendar_spiral: {t["args"]["commands"]["botinfo"]["ii"]}', value = '2019', inline = True)
        e.add_field(name = f':calendar_spiral: {t["args"]["commands"]["botinfo"]["rz"]}', value = '2022', inline = True)
        e.add_field(name = '════════════', value = '════════════', inline = False)
        e.add_field(name = 'Commands', value = len(self.bot.application_commands), inline = True)

        await ctx.response.send_message(embed = e)

def setup(bot:commands.Bot):
    
    bot.add_cog(gerais(bot))
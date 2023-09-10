import discord as discord

from discord.ext import commands
from discord import slash_command, option
from functions.defs import translates

class feedback(commands.Cog):

    def __init__(self, bot:commands.Bot):

        self.bot: commands.Bot = bot

    @slash_command(
        name = 'sugest',
        description = 'Send a suggestion to my owner',
        guild_only = True,
        name_localizations = {
            'en-US': 'sugest',
            'en-GB': 'sugest',
            'es-ES': 'sugerencia',
            'pt-BR': 'sugestão',
            'fr': 'suggestion'
        },
        description_localizations = {
            'en-US': 'Send a suggestion to my owner',
            'en-GB': 'Send a suggestion to my owner',
            'es-ES': 'Enviar una sugerencia a mi dueño',
            'pt-BR': 'Envia uma sugestão para meu dono',
            'fr': 'Envoyer une suggestion à mon propriétaire'
        })
    @commands.cooldown(1,5, commands.BucketType.user)
    @option(name = 'sugest', description = 'Escreva a sugestão')
    @commands.cooldown(1,5, commands.BucketType.user)
    async def sugest(self, interaction: discord.Interaction, sugestão):

        t: dict = translates(interaction.guild)

        channel: discord.TextChannel = self.bot.get_channel(int(1012123748637343756))

        embed: discord.Embed = discord.Embed(
            title = 'Sugest',
            description = f'''
                **Enviado por:** \n {interaction.author}
                **Sugestão:** \n {sugestão}
                **No server:** \n {interaction.guild.name}
                **ID:** {interaction.author.id}'''
            )

        await interaction.response.send_message(t['args']['feedback']['sugest'], ephemeral = True)

        await channel.send(embed=embed)

    @slash_command(
        name = 'report',
        description = 'Send a report to my owner',
        guild_only = True,
        name_localizations = {
            'en-US': 'report',
            'en-GB': 'report',
            'es-ES': 'reportar',
            'pt-BR': 'reportar',
            'fr': 'signaler'
        },
        description_localizations = {
            'en-US': 'Send a report to my owner',
            'en-GB': 'Send a report to my owner',
            'es-ES': 'Enviar un informe a mi propietario',
            'pt-BR': 'Envia um report para meu dono',
            'fr': 'Envoyer un rapport à mon propriétaire'
        })
    @commands.cooldown(1,5, commands.BucketType.user)
    @option(name = 'report', description = 'Escreva o report')
    @commands.cooldown(1,5, commands.BucketType.user)
    async def report(self, interaction: discord.Interaction, report):

        t: dict = translates(interaction.guild)
        
        channel: discord.TextChannel = self.bot.get_channel(int(1012123813070262312))

        embed: discord.Embed = discord.Embed(
            title = 'report',
            description = f'''
                    **Enviado por:** \n {interaction.author}
                    **Report:** \n {report}
                    **No server:** \n {interaction.guild.name}
                    **ID:** {interaction.author.id}'''
                )

        await interaction.response.send_message(t['args']['feedback']['report'], ephemeral = True)

        await channel.send(embed=embed)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(feedback(bot))
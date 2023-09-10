import asyncio
import discord
from discord.ext import commands
from discord import slash_command, option
from classes.selectmenus import setlang, setlog
from db.moderation import dbmoderation
from functions.defs import translates


class moderation(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @slash_command(
        name='set-language',
        description='Sets InviteInfo language',
        name_localizations={
            'en-US': 'set-language',
            'pt-BR': 'definir-idioma',
        },
        description_localizations={
            'en-US': 'Sets Lotus language',
            'pt-BR': 'Define o idioma do Lothus',
        }
    )
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def setlang(self, interaction: discord.Interaction):

        t = translates(interaction.guild)

        await interaction.response.send_message(
            t['args']['lang']['select'],
            view=discord.ui.View(setlang(self.bot, interaction.user, t)),
            ephemeral=True
        )

    @slash_command(
        guild_only=True,
        name='set-logs',
        description='Sets InviteInfo logs',
        name_localizations={
            'en-US': 'set-logs',
            'pt-BR': 'definir-logs',
        },
        description_localizations={
            'en-US': 'Sets InviteInfo logs',
            'pt-BR': 'Define as logs do InviteInfo',
        }
    )
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def setlogs(self, interaction: discord.Interaction):

        t = translates(interaction.guild)

        await interaction.response.send_message('', view=discord.ui.View(setlog(self.bot, interaction.user, t)),
                                                ephemeral=True)

    @slash_command(
        guild_only=True,
        name='delete-invite',
        description='Delete a invite of server',
        name_localizations={
            'en-US': 'delete-invite',
            'pt-BR': 'deletar-convite',
        },
        description_localizations={
            'en-US': 'Delete a invite of server',
            'pt-BR': 'Deleta um convite do servidor',
        }
    )
    @option(
        name='code',
        description_localizations={
            'en-US': 'Invitation code',
            'pt-BR': 'Codigo do convite',
        })
    @option(
        name='reason',
        description_localizations={
            'en-US': 'Reason for delete the invite',
            'pt-BR': 'Motivo de deletar o convite',
        })
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def deleteinvite(self, interaction: discord.Interaction, code, reason=None):

        invite = await interaction.guild.invites()

        t = translates(interaction.guild)

        if reason == None:reason = t['args']['notreason']

        count = 1

        while True:

            try:

                if invite[count - 1].code == code or invite[count - 1].url == code:
                    await invite[count - 1].delete(reason=reason)

                    await interaction.response.send_message(t['args']['commands']['deleteinvite']['success'])

                    return

            except:

                break

            if count == len(invite):

                break

            else:

                count += 1

        await interaction.response.send_message(t['args']['commands']['deleteinvite']['notfound'])

    @slash_command(
        guild_only=True,
        name='setup',
        description='setup all functions bot'
    )
    async def setup(self, interaction: discord.Interaction):

        try:
            t = translates(interaction.guild)

            await interaction.response.defer()

            await interaction.followup.send(t['args']['commands']['setup']['init'])

            def checkinteraction(m: discord.Interaction):
                return m.user.id == interaction.user.id

            msg = await interaction.followup.send(t['args']['commands']['setup']['selectlang'],
                                                 view=discord.ui.View(setlang(self.bot, interaction.user, t)))
            await self.bot.wait_for('interaction', check=checkinteraction, timeout=300)
            await msg.delete()

            def checkinvitelogger(m: discord.Message):
                return m.content and m.author.id == interaction.user.id

            im = await interaction.channel.send(t['args']['commands']['setup']['invitelogger'])
            msg = await self.bot.wait_for('message', check=checkinvitelogger, timeout=130)

            if msg.content.lower().replace(' ', '') == 'skip':
                await msg.delete()
                await im.delete()
                pass
            else:
            
                await msg.delete()
                await im.delete()
                dbmoderation.logs('LogInvite', True, interaction.guild,
                                    interaction.guild.get_channel(int(msg.content.strip('< # >'))).id)
                await interaction.channel.send(t['args']['commands']['setup']['success'], delete_after=5)

            def checkinvitecreate(m: discord.Message):
                return m.content and m.author.id == interaction.user.id

            im = await interaction.channel.send(t['args']['commands']['setup']['invitecreate'])
            msg = await self.bot.wait_for('message', check=checkinvitecreate, timeout=130)
            if msg.content.lower().replace(' ', '') == 'skip':
                await msg.delete()
                await im.delete()
                pass
            else:
                await msg.delete()
                await im.delete()
                dbmoderation.logs('LogInviteCreate', True, interaction.guild,
                                  interaction.guild.get_channel(int(msg.content.strip('< # >'))).id)
                await interaction.channel.send(t['args']['commands']['setup']['success'], delete_after=5)

            def checkinvitedelete(m: discord.Message):
                return m.content and m.author.id == interaction.user.id

            im = await interaction.channel.send(t['args']['commands']['setup']['invitedelete'])
            msg = await self.bot.wait_for('message', check=checkinvitedelete, timeout=130)
            if msg.content.lower().replace(' ', '') == 'skip':
                await msg.delete()
                await im.delete()
                pass
            else:
                await msg.delete()
                await im.delete()
                dbmoderation.logs('LogInviteDelete', True, interaction.guild,
                                  interaction.guild.get_channel(int(msg.content.strip('< # >'))).id)
                await interaction.channel.send(t['args']['commands']['setup']['invitecreate'], delete_after=5)

            await interaction.channel.send(t['args']['commands']['setup']['terminated'])
        except Exception as error:

            await interaction.followup.send('error: {}'.format(error))
    
    @slash_command()
    async def hello(self, interaction: discord.Interaction):
        t = translates(interaction.guild)
        try:
            def user(u: discord.Interaction):
                return u.user.id == interaction.user.id
            msg = await interaction.response.send_message(t['args']['commands']['setup']['selectlang'],
                                                    view=discord.ui.View(setlang(self.bot, interaction.user, t)))
            await self.bot.wait_for("interaction", check = user, timeout = 3)
            print("sucesso")
        except Exception as error:
            print("error")

def setup(bot: commands.Bot):
    bot.add_cog(moderation(bot))
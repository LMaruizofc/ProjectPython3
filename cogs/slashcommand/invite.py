import discord
from discord.ext import commands
from discord import slash_command, option
from functions.defs import translates
from discord.ui import Button

class invite(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        
        self.bot = bot

    @slash_command(
        name='invites',
        description='Shows a member\'s invites on the server',
        name_localizations={
            'en-US': 'invites',
            'pt-BR': 'convites',
        },
        description_localizations={
            'en-US': 'Shows a member\'s invites on the server',
            'pt-BR': 'Mostra os convites de um membro no servidor',
        }
    )
    @option(name='member', description='Escolha o membro')
    async def invites(self, ctx: discord.Interaction, member: discord.Member = None):

        t = translates(ctx.guild)

        if member == None:member = ctx.user

        invite = await member.guild.invites()

        count = 1

        e = discord.Embed(title=t['args']['commands']['invites']['invite'].format(member.name))

        try:

            while True:

                if invite[count - 1].inviter == member:
                    e.add_field(name=f'{invite[count - 1]}',
                                value=t['args']['commands']['invites']['uses'].format(invite[count - 1].uses),
                                inline=False)

                if count == len(invite):

                    break

                else:

                    count += 1

            if e.fields == []:
                await ctx.response.send_message(t['args']['commands']['invites']['notinvite'], ephemeral=True)

                return

            await ctx.response.send_message(embed=e)

        except:

            await ctx.response.send_message(t['args']['commands']['invites']['notinviteguild'])

    @slash_command(
        name='invite-info',
        description='Send some information from an invite',
        name_localizations={
            'en-US': 'invite-info',
            'pt-BR': 'convite-info',
        },
        description_localizations={
            'en-US': 'Send some information from an invite',
            'pt-BR': 'Envia algumas informações de um convite',
        }
    )
    @option(name='code', description='Coloque o codigo do convite')
    async def inviteinfo(self, ctx: discord.Interaction, code):

        t = translates(ctx.guild)

        invite = await ctx.guild.invites()

        if invite == []: 
            return await ctx.response.send_message(t['args']['commands']['invites']['notinviteguild'], ephemeral = True)

        count = 1

        e = discord.Embed(title=code)

        while True:

            if invite[count - 1].code == code or invite[count - 1].url == code:

                uses = invite[count - 1].max_uses

                expira = invite[count - 1].expires_at

                if uses == 0:
                    uses = t['args']['commands']['inviteinfo']['uses0']

                if expira == None:
                    expira = t['args']['commands']['inviteinfo']['expirenone']

                e.add_field(name=t['args']['commands']['inviteinfo']['created'], value=invite[count - 1].inviter,
                            inline=False)

                e.add_field(name=t['args']['commands']['inviteinfo']['usest'], value=invite[count - 1].uses,
                            inline=False)

                e.add_field(name=t['args']['commands']['inviteinfo']['usesm'], value=uses, inline=False)

                e.add_field(name=t['args']['commands']['inviteinfo']['expire'], value=expira, inline=False)

                e.add_field(name=t['args']['commands']['inviteinfo']['datecreate'],
                            value=invite[count - 1].created_at.strftime("%d %m %Y"), inline=False)

            else:

                await ctx.response.send_message(t['args']['commands']['inviteinfo']['notfound'], ephemeral=True)

                return

            if count == len(invite):break
            else:count += 1

        await ctx.response.send_message(embed=e)

def setup(bot: commands.Bot):
    bot.add_cog(invite(bot))

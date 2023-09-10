import DiscordUtils
import discord
from discord.ext import commands
from db.invites import add_invite, invite
from db.moderation import dbmoderation, mod
from functions.checks import NoVote
from functions.defs import translates, better_time

class events(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

        self.tracker = DiscordUtils.InviteTracker(bot)

    @commands.Cog.listener()
    async def on_application_command_error(self, interaction: discord.Interaction, error):

        errorEmoji: discord.Emoji = self.bot.get_emoji(1044750438978818049)

        t: dict = translates(interaction.guild)

        if isinstance(error, commands.CommandOnCooldown):

            cd = round(error.retry_after)

            if cd == 0:

                cd = 1

            await interaction.response.send_message(f'{errorEmoji} || {t["args"]["mod"]["cooldown"].format(better_time(cd))}', ephemeral = True)

        if isinstance(error, NoVote):

            await interaction.response.send_message(f"{errorEmoji} || {error}", ephemeral = True)
        
        if isinstance(error, commands.BotMissingPermissions):
            
            await interaction.response.send_message(f'{errorEmoji} || {t["args"]["mod"]["botnotpermission1"]} "Ban_Members" {t["args"]["mod"]["botnotpermission2"]}')

        if isinstance(error, commands.MissingPermissions):
            
            await interaction.response.send_message(f"{errorEmoji} || {t['args']['mod']['notpermission']}", ephemeral = True)

        if isinstance(error, commands.MemberNotFound):

            await interaction.response.send_message(f'{errorEmoji} || {t["args"]["mod"]["bannotfound"]}')
        
        if error:

            print(error)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):

        dbmoderation.lang('lang', 'en-us', guild)
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        
        mod.find_one_and_delete({"_id": guild.id})

    @commands.Cog.listener()
    async def on_ready(self):

        print("I'm ready")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):

        t = translates(member.guild)

        try:

            if mod.find_one({'_id': member.guild.id})['LogInvite']['True?'] == True:

                c = mod.find_one({'_id': member.guild.id})['LogInvite']['id']

                inviter = await self.tracker.fetch_inviter(member)

                if member.bot:
                    return await member.guild.get_channel(c).send(t['args']['invites']['bot'].format(member.mention))


                await add_invite(member.guild, inviter, + 1)

                await member.guild.get_channel(c).send(
                    t['args']['invites']['invited'].format(member.mention, inviter.name,
                                                           invite.find_one({"_id": f"{member.guild.id}_{inviter.id}"})[
                                                               "qnt"]))

        except:

            None

    @commands.Cog.listener()
    async def on_invite_create(self, invite: discord.Invite):

        emojiInvite: discord.Emoji = self.bot.get_emoji(1044747249378414612)
        t: dict = translates(invite.guild)

        try:

            if mod.find_one({'_id': invite.guild.id})['LogInviteCreate']['True?'] == True:

                c = mod.find_one({'_id': invite.guild.id})['LogInviteCreate']['id']

                uses = invite.max_uses

                if mod.find_one({"_id": invite.guild.id})['lang'] != 'pt-br':

                    expira = invite.expires_at.strftime("%Y/%m/%d")

                else:

                    expira = invite.expires_at.strftime("%d/%m/%Y")

                if uses == 0:
                    uses = t['args']['invites']['uses']

                if expira == None:
                    expira = t['args']['invites']['expira']

                await invite.guild.get_channel(c).send(
                    f"{emojiInvite} {t['args']['invites']['invitecreate'].format(invite.inviter.mention, invite.code, uses, expira)}")

        except:

            None

    @commands.Cog.listener()
    async def on_invite_delete(self, invite: discord.Invite):

        t = translates(invite.guild)

        try:

            if mod.find_one({'_id': invite.guild.id})['LogInviteDelete']['True?'] == True:
                c = mod.find_one({'_id': invite.guild.id})['LogInviteDelete']['id']
                await invite.guild.get_channel(c).send(t['args']['invites']['invitedelete'].format(invite.code))

        except:

            None


def setup(bot: commands.Bot):
    bot.add_cog(events(bot))

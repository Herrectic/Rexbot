import discord
import random
from discord.ext import commands
from discord.ext.commands import cooldown,BucketType
from aiohttp import request


class GeneralCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # the eight ball

    @commands.command(aliases=['8ball'])
    @cooldown(1,3,BucketType.channel)
    async def eight_ball(self, ctx, *, question):
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."
                     ]

        embed = discord.Embed(title='*The 8ball*', description=f'**{ctx.message.author}** asked a question.\n\nThe question was: **{question}**\n\n\n{random.choice(responses)}', colour=0x0000ff)
        await ctx.send(embed=embed)

    # Help console

    @commands.command()
    @cooldown(1,3,BucketType.channel)
    async def help(self, ctx, helprole=None):
        mod_role = discord.utils.get(ctx.author.roles, name='Moderator')
        admin_role = discord.utils.get(ctx.author.roles, name='Administrator')

        general_embed = discord.Embed(
                title = 'Bot commands for @Rexbot',
                description='**8ball**- Uses AI to give you the best answers to your questions\n'
                            '**avatar**- Shows the avatar of the user entered\n'
                            '**userinfo**- Gives the info of the entered user\n'
                            '**serverinfo**- Gives the info of the server\n'
                            '**meme**- Sends a beautiful meme\n'
                            '**dog**-Gets you a dog picture\n',
                colour=0x01a901
            )
        general_embed.set_footer(text='Made by CABREX with ❤')

        mod_embed = discord.Embed(
                title = 'Moderation commands for @Rexbot',
                description = '**help**\ngives you this dialogue\n\n'
                              '**kick**\nKicks the member out of the server\nUsage: $kick {member_name} {reason}, reason is neccessary\n\n'
                              '**ban**\nbans the user from the server\nUsage: $ban {member_name} {reason}, reason is necessary\n\n'
                              '**unban**\nunbans the user, you need to know the member\'s name\nUsage: $unban {member_name}\n\n'
                              '**mute**\nmutes the user\nUsage: $mute {member_name} {reason}, reason is necessary\n\n'
                              '**unmute**\nunmutes the user\nUsage: {member_name}\n\n'
                              '**clear | remove | purge**\n clears messages from that channel\nUsage: $clear {n} where `n` is the number of messages to be purged\n\n'
                              '**embedpost**\nWill post an embedded announcement\nUsage: $embedpost {message}\n\n'
                              '**userpost**\nWill send message instead of you\nUsage: $userpost {message}\n\n'
                              '**addrole**\nAdds role to member\nUsage: $addrole {role_name}\n\n'
                              '**removerole | purgerole**\nRemoves role from member\nUsage: $removerole {member_name}',
                colour=0x01a901
            )
        mod_embed.set_footer(text='Made by CABREX with ❤')

        if (mod_role is not None or admin_role is not None or ctx.message.author.guild_permissions.manage_messages):            
            
            await ctx.send(embed=general_embed)
            user = ctx.author
            await user.send(embed=mod_embed)

        else:

          if (str(ctx.message.channel) == 'bot-commands') or (str(ctx.message.channel) == '🤖bot-commands') or (str(ctx.message.channel) == '🤖-bot-commands'):
              await ctx.send(embed=general_embed)

          else:

              embed = discord.Embed(title='Wrong channel', description='**Please use this command in #bot-commands**', colour=0xff0000)
              await ctx.send(embed=embed)

    # Avatar fetcher

    @commands.command()
    @cooldown(1,5,BucketType.channel)
    async def avatar(self, ctx, member: discord.Member):
      try:
          if member is None:
            embed = discord.Embed(colour=0x0000ff)
            embed.set_image(url=f'{ctx.author.avatar_url}')
          else:
            embed = discord.Embed(colour=0x0000ff)
            embed.set_image(url=f'{member.avatar_url}')
            await ctx.send(embed=embed)
      except Exception as e:
            await ctx.send(f'Exception thrown: {e}')

    # Avatar fetcher: Error handling
    @avatar.error
    async def avatar_error(self, ctx, error):
      if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour=0x0000ff)
        embed.set_image(url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)
      else:
        await ctx.send(f'{error}')

    # Userinfo

    @commands.command()
    @cooldown(1,3,BucketType.channel)
    async def userinfo(self, ctx, member: discord.Member):

        roles = []
        for role in member.roles:
            roles.append(role)

        embed = discord.Embed(
            colour = 0x0000ff,
        )
        embed.set_author(name=f'User Info - {member}')
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text='made by CABREX with ❤')

        embed.add_field(name='ID:', value=member.id)
        embed.add_field(name='Member Name:', value=member.display_name)

        embed.add_field(name='Created at: ', value=member.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
        embed.add_field(name='Joined at:', value=member.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))

        embed.add_field(name=f'Roles ({len(roles)})', value=' '.join([role.mention for role in roles]))

        embed.add_field(name='Bot?', value=member.bot)

        await ctx.send(embed=embed)


    # Userinfo: Error handling

    @userinfo.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send('```\n$userinfo {member_name}\n          ^^^^^^^^^^^^^\nMissing Required Argument member_name\n```')
        else:
          await ctx.send(f'**{error}**')


    # Server info

    @commands.command()
    @cooldown(1,4,BucketType.channel)
    async def serverinfo(self, ctx):

        count = 0
        for people in ctx.guild.members:
          if people.bot:
            count = count + 1
          else:
            pass

        embed = discord.Embed(
              title = f'{ctx.guild.name} info',
              colour = 0x0000ff
          )
        embed.set_thumbnail(url=ctx.guild.icon_url)

        embed.add_field(name='Owner name:', value=ctx.guild.owner.display_name)
        embed.add_field(name='Server ID:', value=ctx.guild.id)

        embed.add_field(name='Server region:', value=ctx.guild.region)
        embed.add_field(name='Members:', value=len(ctx.guild.members))
        embed.add_field(name='bots:', value=count)

        embed.add_field(name='Text Channels:', value=len(ctx.guild.text_channels))
        embed.add_field(name='Voice Channels:', value=len(ctx.guild.voice_channels))

        embed.add_field(name='Created On:', value=ctx.guild.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))

        await ctx.send(embed=embed)

    # Memes

    @commands.command()
    @cooldown(1,3,BucketType.channel)
    async def meme(self, ctx):

        colour_choices= [0x400000,0x997379,0xeb96aa,0x4870a0,0x49a7c3,0x8b3a3a,0x1e747c,0x0000ff]

        meme_url = "https://meme-api.herokuapp.com/gimme?nsfw=false"
        async with request("GET", meme_url, headers={}) as response:
          if response.status==200:
            data = await response.json()
            image_link = data["url"]
          else:
            image_link = None

        async with request("GET", meme_url, headers={}) as response:
          if response.status==200:
            data = await response.json()
            embed = discord.Embed(
              title=data["title"],
              colour=random.choice(colour_choices)
            )
            if image_link is not None:
              embed.set_image(url=image_link)
              await ctx.send(embed=embed)

          else:
            await ctx.send(f"The API seems down, says {response.status}")

    # Dog pictures

    @commands.command()
    @cooldown(1,1,BucketType.channel)
    async def dog(self, ctx):
      
      colour_choices= [0x400000,0x997379,0xeb96aa,0x4870a0,0x49a7c3,0x8b3a3a,0x1e747c,0x0000ff]

      dog_url="https://random.dog/woof.json"
      async with request("GET", dog_url, headers={}) as response:
        if response.status == 200:
          data = await response.json()
          image_link = data["url"]
          embed = discord.Embed(
              colour = random.choice(colour_choices)
          )
          embed.set_image(url=image_link)
          await ctx.send(embed=embed)

        else:
          await ctx.send(f"The API seems down, says {response.status}")





def setup(bot):
    bot.add_cog(GeneralCog(bot))

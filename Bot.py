import discord
import sqlite3
import random
from discord.ext import commands
from config import settings
bot=commands.Bot(command_prefix=settings['prefix']) 
connection = sqlite3.connect('server.db')
cursor = connection.cursor()

@bot.command()
async def hello(ctx):
	author = ctx.message.author
	await ctx.send(f'Здравствуй говнарь {author.mention}!')

@bot.command()
async def test(ctx, *, arg):
    await ctx.send(arg)
@bot.event 
async def on_ready():
	connection.commit()
	print('Bot connected')



@bot.command()
async def up(ctx, a: int, b: int):
    await ctx.send(a+b)

class Slapper(commands.Converter):
    async def convert(self, ctx, argument):
        to_slap = random.choice(ctx.guild.members)
        return '{0.author} ебнул {1} потому что *{2}*'.format(ctx, to_slap, argument)

@bot.command()
async def slap(ctx, *, reason: Slapper):
    await ctx.send(reason)

class JoinDistance:
    def __init__(self, joined, created):
        self.joined = joined
        self.created = created

    @classmethod
    async def convert(cls, ctx, argument):
        member = await commands.MemberConverter().convert(ctx, argument)
        return cls(member.joined_at, member.created_at)

    @property
    def delta(self):
        return self.joined - self.created

@bot.command()
async def delta(ctx, *, member: JoinDistance):
    is_new = member.delta.days < 100
    if is_new:
        await ctx.send("Hm you're not so new.")
    else:
        await ctx.send("Hey you're pretty new!")



bot.run(settings['token'])
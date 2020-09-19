import discord
import sqlite3
from discord.ext import commands
from config import settings
bot=commands.Bot(command_prefix=settings['prefix']) 

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

@bot.command()
async def hello(ctx):
	author = ctx.message.author
	await ctx.send(f'Здравствуй говнарь {author.mention}!')
@bot.event 
async def on_ready():
	cursor.execute("""CREATE TABLE IF NOT  EXISTS  users(
		name TEXT,
		id INT,
		cash BIGINT,
		rep INT,
		lvl INT
		)""")
	for guild in bot.guilds:
		for member in guild.members: 
			if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is  None:
				cursor.execute(f"INSERT INTO users VALUES ('{member}',{member.id}, 0, 0 , 1 )")
					
			else:
				pass
	connection.commit()
	print('Bot connected')
@bot.event 
async def on_member_join(member):
	if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is  None:
		cursor.execute(f"INSERT INTO users VALUES ('{member}',{member.id}, 0, 0 , 1 )")	
		connection.commit()	
	else:
		pass

@bot.command(aliases = ['govno','cashe'])  #!команды выводящие одно и тоже 
async def __balance(ctx,member:discord.Member = None):
	if member is None:
		await ctx.send(embed = discord.Embed(
			description = f"""Уровень говнярства **{ctx.author}** . **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} мда, ну и вонь :coolstory**"""
		))
	else:
		await ctx.send(embed = discord.Embed(
			description = f"""Уровень говнярства **{member}** . **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.member.id)).fetchone()[0]} мда, ну и вонь :poo **"""
		))



bot.run(settings['token'])
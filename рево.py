import asyncio

import discord
from discord.ext import commands
import Config
bot = commands.Bot(command_prefix="-")

@bot.event
async  def on_ready():
    print("Негры начинают пахать")

@bot.command()
async def sum(ctx, x: int, y: int):
    await ctx.send(x+y)

@bot.command()
async def diff(ctx, x: int, y: int):
    await ctx.send(x - y)

@bot.command()
async def mult(ctx, x: int, y: int):
    await ctx.send(x * y)

@bot.command()
async def vide(ctx, x: int, y: int):
    await ctx.send(x / y)

@bot.command()
async def ban(ctx, member: discord.Member = None, time = None, *, reason: str = None):
    time_letter = time[-1:]
    time_numbers = int(time[:-1])

    def t(time_letter):
        if time_letter == 's':
            return 1
        if time_letter == 'm':
            return 60
        if time_letter == 'h':
            return 60 * 60
        if time_letter == 'd':
            return 60 * 60 * 24

    async def unb(member):
        users = await ctx.guild.bans()
        for ban_user in users:
            if ban_user.user == member:
                await ctx.guild.unban(ban_user.user)


    if member:
        if time:
            if time_letter == 's':
                return 1
            if time_letter == 'm':
                return 60
            if time_letter == 'h':
                return 60 * 60
            if time_letter == 'd':
                return 60 * 60 * 24
            if reason:
                await member.ban(reason=reason)
                await ctx.send(embed=discord.Embed(description=f"ты забанил чела  {member.mention} \nВремя: {time} \nПричина: {reason}"))

                await asyncio.sleep(time_numbers * t(time_letter))

                await unb(member)
                await ctx.send(f"Ты разбанил чела под ником {member.mention}")
            else:
                await member.ban()
                await ctx.send(embed=discord.Embed(description=f"ты забанил чела  {member.mention} \nВремя: {time}"))

                await asyncio.sleep(time_numbers * t(time_letter))

                await unb(member)
                await ctx.send(f"Ты разбанил чела под ником {member.mention}")


        else:
                await member.ban()
                await ctx.send(embed=discord.Embed(description=f"ты забанил чела  {member.mention}"))
    else:
            await ctx.send("Напиши имя пользователя дебил")

@bot.command()
async def unban(ctx, id: int = None):
    if id:
        users = await ctx.guild.bans()
        member = bot.get_user(id=id)
        for ban_user in users:
            if ban_user.user == member:
                await ctx.guild.unban(ban_user.user)
        await ctx.send(f"Чел {member.mention} разбанен")
    else:
        await ctx.send("Напиши айди")



@bot.command()
async def clear(ctx, count: int):
    await ctx.channel.purge(limit=count+1)
    await ctx.send(f"Ха я удалил {count} сообщения")

bot.run(Config.token)
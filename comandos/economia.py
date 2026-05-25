import discord
from discord.ext import commands
import os
from utilidades import datos_economia
import random

class Economia(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(help="Revisa tu balance", aliases=["bal", "cash"])
	async def balance(self, ctx, member: discord.Member = None):

		if member is None:
			member=ctx.author

		balance = datos_economia.get_balance(member.id)

		await ctx.send(
			f"""
			## Balance de __{member.name}__
			** **
			**Dinero:** ${balance}
			"""
		)

	@commands.command(help="Modificar el balance [Solo Asf puede usarlo]", name="set-balance", aliases=["establecer-balance", "set-cash"])
	async def set_balance(self, ctx, member: discord.Member, amount: int):

		if ctx.author.id != 925480868049465366:
			await ctx.reply("TU... TU NO ERES ASF!!!")
			await ctx.send("https://tenor.com/view/you-aren%27t-toji-toji-naoya-naoya-jjk-maki-gif-5580724116189358420")
			return

		datos_economia.set_balance(member.id, amount)

		await ctx.send(f"Balance modificado de {member.mention} a **{amount}**", allowed_mentions=discord.AllowedMentions.none())

	@commands.command(name="add-money", aliases=["addmoney", "add-cash"])
	async def add_money(self, ctx, member: discord.Member, amount: int):

		if ctx.author.id != 925480868049465366:
			await ctx.reply("TU... TU NO ERES ASF!!!")
			await ctx.send("https://tenor.com/view/you-aren%27t-toji-toji-naoya-naoya-jjk-maki-gif-5580724116189358420")
			return

		datos_economia.add_balance(member.id, amount)

		await ctx.send(f"¡He añadido a {member.mention} la suma de **{amount}** a su balance!", allowed_mentions=discord.AllowedMentions.none())

	@commands.command(name="remove-money", aliases=["removemoney", "quitar-balance", "remove-cash"])
	async def remove_money(self, ctx, member: discord.Member, amount: int):
		if ctx.author.id != 925480868049465366:
			await ctx.reply("TU... TU NO ERES ASF!!!")
			await ctx.send("https://tenor.com/view/you-aren%27t-toji-toji-naoya-naoya-jjk-maki-gif-5580724116189358420")
			return

		datos_economia.remove_balance(member.id, amount)

		await ctx.send(f"¡He removido a {member.mention} la suma de $**{amount}** de su balance!", allowed_mentions=discord.AllowedMentions.none())

	@commands.cooldown(1, 86400, commands.BucketType.user)
	@commands.command(help="Usalo para trabajar, ¡Y dejar el ocio! Gana desde `20` a `20`.", aliases=["trabajo", "trabajar"])
	async def work(self, ctx):

		tipos = [
			"repartidor de Rappi",
			"novia de Jiro",
			"staff de Symbols",
			"creador de infos",
			"creador de gifs en **Lookism: posterita**",
			"novia de Black Star"
		]
		amount = random.randint(1, 20)
		tipo = random.choice(tipos)

		datos_economia.add_balance(ctx.author.id, amount)

		await ctx.send(f"Tu trabajo como {tipo} ha rendido frutos, ganando **${amount}**.")


async def setup(bot):
	await bot.add_cog(Economia(bot))

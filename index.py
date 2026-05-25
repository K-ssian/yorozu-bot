import discord
from discord.ext import commands
import asyncio
import time
import random
import traceback
import os
from utilidades import datos_prefixes
from dotenv import load_dotenv

# importar variables de dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

# Importar permisos del bot

intents = discord.Intents.default()
intents.message_content = True

async def prefix(bot,message):

    if message.guild is None:

        prefix_servidor = "!"

    else:

        prefix_servidor = (datos_prefixes.recib_prefix(message.guild.id))

    return commands.when_mentioned_or(prefix_servidor, "yoru", "Yoru", "YORU")(bot, message)

bot = commands.Bot(
    command_prefix=prefix,
    intents=intents,
    case_insensitive=True,
    help_command=None
)

@bot.event
async def on_ready():

	await bot.change_presence(
		status=discord.Status.idle,
		activity=discord.Game("programar")
	)

	print(f"[*] Conectado como {bot.user}")

@bot.command(name="recargar", hidden=True)
async def recargar_cog(ctx, extension: str):
# Reemplaza esto con tu lista de ADMIN_IDS si ya la creaste
	if ctx.author.id != 925480868049465366:
		return await ctx.send("❌ No tienes permisos para usar este comando.")

	try:
		await bot.reload_extension(f"comandos.{extension}")
		await ctx.send(f"✅ El módulo `comandos.{extension}` ha sido recargado con éxito. Los cambios ya están en vivo.")
	except Exception as e:
		await ctx.send(f"❌ Error al recargar `{extension}`:\n```py\n{e}\n```")

@bot.event
async def on_message(message):

	if message.author.bot:
		return

	if message.guild is None:
		print(
            	f"""
		[MD]

		Usuario:
		{message.author}

		Contenido:
		{message.content}
		"""
		)

	await bot.process_commands(message)

async def main():

	async with bot:
		print("[+] Cargando comandos...")
		for archivo in os.listdir("./comandos"):

			if archivo.endswith(".py"):
				await bot.load_extension(f"comandos.{archivo[:-3]}")
				print(f"[-] El listado de comandos: '{archivo[:-3]}' ha sido cargado.")

		print("[*] Todo ha sido cargado con exito.")
		await bot.start(TOKEN)

asyncio.run(main())

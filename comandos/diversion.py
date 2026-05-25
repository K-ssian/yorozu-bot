import discord
from discord.ext import commands
import random
import aiohttp

class Diversion(commands.Cog):
    emoji = "🎲"
    descripcion_corta = "Comandos de uso recreativo"

    def __init__(self, bot):

        self.bot = bot

    @commands.command()
    async def md(self, ctx, user_id: int, *, message):

        objetivo = self.bot.get_user(user_id)

        if objetivo is None:
            objetivo = await self.bot.fetch_user(user_id)

        await objetivo.send(message)

    @commands.command(help="Proporcioname opciones, ¡Y escogere uno aleatoriamente! Ej: escoge gatos, perros, Sukuna.")
    async def escoge(self, ctx, *, opciones):
        if not argumentos:
            await ctx.send("No me has proporcionado nada que escoger, bwam.")
            return

        opciones=opciones.replace(" o ", ", ").split(", ")
        if len(opciones) < 2:
            await ctx.send("Cari, necesito minimo 2 opciones y lo sabes...")
            return
        eleccion=random.choice(opciones)

        await ctx.send(eleccion.strip())

    @commands.command(help="Envía un post de reddit aleatorio, puedes indicar con un `<subreddit>` que subreddit revisar.")
    async def reddit(self, ctx, subreddit="Meme"):

        url = (f"https://meme-api.com/gimme/{subreddit}")

        async with aiohttp.ClientSession() as session:

            async with session.get(url) as response:

                if response.status != 200:
                    await ctx.send("Subreddit inválido.")
                    return

                data = await response.json()

        titulo = data["title"]
        imagen = data["url"]
        post = data["postLink"]
        subreddit = data["subreddit"]

        embed = discord.Embed(
			title=titulo,
			url=post,
			description=f"r/{subreddit}",
			color=discord.Color.random()
        )

        embed.set_image(url=imagen)

        await ctx.send(embed=embed)

    @commands.command(help="Proporcionale un número y te dara un resultado aleatorio, ¡Un dado!", aliases=["roll"])
    async def dice(self, ctx, monto: int):

        resultado=random.randint(1, monto)
        await ctx.send(f"🎲 ¡Ha salido un `{resultado}`!")

async def setup(bot):
    await bot.add_cog(Diversion(bot))

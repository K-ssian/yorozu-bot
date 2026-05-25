import discord
from discord.ext import commands
from datetime import datetime
from utilidades import datos_prefixes

class General(commands.Cog):

    def __init__(self, bot):

        self.bot = bot


    @commands.command()
    async def ping(self, ctx):

        await ctx.send(
            f"¡Pong! {round(self.bot.latency * 1000)}ms"
        )

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, nuevoprefix = None):
        if nuevoprefix:
          datos_prefixes.guardar_prefix(ctx.guild.id, nuevoprefix)
          await ctx.send(f"¡Se ha cambiado exitosamente el prefix a `{nuevoprefix}`!")
        elif nuevoprefix is None:
          dato=datos_prefixes.recib_prefix(ctx.guild.id)

          embed=discord.Embed(
                description=f"> El prefix del servidor es: **`{dato}`**",
                color=discord.Color(0x000000)
          )

          await ctx.send(embed=embed)

    @commands.command()
    async def avatar(
        self,
        ctx,
        miembro: discord.Member = None
    ):

        if miembro is None:

            miembro = ctx.author

        embed = discord.Embed(
            title=f"Avatar de {miembro.name}",
            color=discord.Color.random(),
            timestamp=datetime.utcnow()
        )

        embed.set_image(
            url=miembro.display_avatar.with_size(4096).url
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def say(self, ctx, *, mensaje):

        partes = mensaje.split(" ", 1)

        try:

            id_msj = int(partes[0])

            if len(partes) < 2:

                await ctx.send(
                    "Debes escribir el nuevo texto."
                )

                return

            texto = partes[1]

            mensaje = await ctx.channel.fetch_message(
                id_msj
            )

            if mensaje.author != self.bot.user:

                embed = discord.Embed(
                    title="Error",
                    description=(
                        "Ese mensaje no me pertenece."
                    ),
                    color=discord.Color.red(),
                    timestamp=datetime.utcnow()
                )

                await ctx.reply(embed=embed)

                return

            await mensaje.edit(content=texto)

            await ctx.send(
                "Mensaje editado."
            )

        except ValueError:

            await ctx.send(mensaje)

        except discord.NotFound:

            await ctx.send(
                "No encontré ese mensaje."
            )



async def setup(bot):

    await bot.add_cog(
        General(bot)
    )

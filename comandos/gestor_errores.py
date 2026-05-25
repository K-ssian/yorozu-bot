import discord
from discord.ext import commands
import random
import time
import traceback
from utilidades.util_embeds import gestor_mensajes

embeds=gestor_mensajes()

class GestorErrores(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # En un Cog, @bot.event se transforma en @commands.Cog.listener()
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.CommandNotFound):                           # Usando el estilo suave de Nekotina fuera del embed
            await ctx.send(
                embed=embeds.crear("stress", f"El comando `{ctx.invoked_with}` no existe.", color=discord.Color.red())
            )
            return
        elif isinstance(error, commands.MissingRequiredArgument):
                 await ctx.send(embed=embeds.crear(
                    "larp",
                    f"Faltan argumentos en el comando `{ctx.invoked_with}`.",
                    f"Uso: `{ctx.prefix}{ctx.command.name} {ctx.command.signature}`",
                    color=discord.Color.red()
                )
            )

        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                embed=embeds.crear(
                    "sigh",
                    "Argumentó inválido",
                    "...así como todos los que tiras lmao.",
                    color=discord.Color.red()
                )
            )

        elif isinstance(error, commands.CommandOnCooldown):
            timestamp = int(time.time() + error.retry_after)
            molestias = [
                f"¡Oye! Aguarda <t:{timestamp}:R> antes de volver a usar `{ctx.invoked_with}`.",
                f"Recuerda el cooldown, lo podrás usar <t:{timestamp}:R>.",
                f"¡Pero tonto!~ <t:{timestamp}:R> podrás usar `{ctx.invoked_with}` de nuevo."
            ]

            await ctx.send(
                embed=embeds.crear(subtexto=f"{random.choice(molestias)}", color=discord.Color.blue())
            )

        else:
            # Si el error es otra cosa (un bug real en tu código), lo imprime en la terminal de Termux
            traceback.print_exception(type(error), error, error.__traceback__)

# Función obligatoria para que el index lo cargue
async def setup(bot):
    await bot.add_cog(GestorErrores(bot))

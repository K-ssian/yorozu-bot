import discord
from discord.ext import commands
from utilidades.util_visual import AyudaViewAutomatizada
from utilidades.util_embeds import gestor_mensajes

class AyudaInteractiva(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embeds = gestor_mensajes() 

    @commands.command(name="help", aliases=["ayuda"])
    async def comando_help(self, ctx):
        
        embed_inicio = self.embeds.crear(
            emoji_y="happy", 
            texto_principal="Panel de Control de Yorozu",
            subtexto="Selecciona una categoría en el menú desplegable para ver mis comandos.",
            color=discord.Color.dark_theme()
        )
        
        # Le pasamos el bot a la vista
        vista = AyudaViewAutomatizada(self.bot)
        
        mensaje = await ctx.send(embed=embed_inicio, view=vista)
        vista.mensaje_referencia = mensaje

async def setup(bot):
    await bot.add_cog(AyudaInteractiva(bot))

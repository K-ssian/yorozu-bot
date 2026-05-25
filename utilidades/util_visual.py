import discord
from discord.ext.commands import bot

class AyudaView(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        opciones = []
        blacklist = ["AyudaInteractiva", "GestorErrores"]

        for nombre_cog, cog in bot.cogs.items():
            if nombre_cog in blacklist:
                continue

            # Extrae atributos
            emoji = getattr(cog, "emoji", "⚙️")
            desc = getattr(cog, "descripcion_corta", f"Ver comandos de {nombre_cog}")

            label_limpio = nombre_cog.replace("_", " ").title()

            opciones.append(discord.SelectOption(
                label=label_limpio,
                value=nombre_cog,
                description=desc,
                emoji=emoji
                ))

        super().__init__(placeholder="Selecciona una categoría...", min_values=1, max_values=1, options=opciones)

    async def callback(self, interaction: discord.Interaction):
        nombre_cog_elegido=self.values[0]
        cog = self.bot.get_cog(nombre_cog_elegido)

        embed = discord.Embed(
                title=f"__ {nombre_cog_elegido} __",
                color=discord.Colour.dark_theme()
                )

        for comando in cog.get_commands():
            if not comando.hidden:
                ayuda_texto = comando.help or "Sin descripcion"
                if comando.signature:
                    embed.add_field(name=f"{comando.name} `{comando.signature}`", value=ayuda_texto, inline=False)
                else:
                    embed.add_field(name=f"{comando.name}", value=ayuda_texto, inline=False)

        await interaction.response.edit_message(embed=embed)

class AyudaViewAutomatizada(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=60)
        self.mensaje_referencia = None
        
        # Añadimos el menú desplegable a la vistaselself
        self.add_item(AyudaView(bot))

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        
        if self.mensaje_referencia:
            try:
                await self.mensaje_referencia.edit(view=self)
            except discord.NotFound:
                pass


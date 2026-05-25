import discord

class gestor_mensajes:
	def __init__(self):

		self.emojis={
			"sigh":
			"<:yorozu_sigh:1506193174161395782>",

			"fly":
			"<:yorozu_fly:1506193582594199592>",

			"stress":
			"<:yorozu_stress:1506193500968849528>",

			"happy":
			"<:yorozu_happy:1506193293426298991>",

			"larp":
			"<:yorozu_larp:1506193392378314892>"
		}

	def crear(self, emoji_y: str = None, texto_principal: str = None, subtexto: str = None, color: discord.Color = None) -> discord.Embed:

		titulo = ""

		if emoji_y:
			emoji = self.emojis.get(
				emoji_y,
				"❓"
				)

			titulo += f"{emoji} "

		if texto_principal:
			titulo += texto_principal

		descripcion = subtexto or ""

		embed=discord.Embed(
			title=titulo or None,
			description=descripcion,
			color=color
			)

		return embed

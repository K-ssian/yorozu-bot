import discord
from discord.ext import commands, tasks
import yt_dlp
import os
import asyncio
import re
import time
from yt_dlp.utils import DownloadError
from utilidades.util_embeds import gestor_mensajes
import utilidades.datos_reminders as db_remind

embeds=gestor_mensajes()

class Utilidades(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
		# Expresión regular general para atrapar cualquier URL que empiece con http o https
        self.url_pattern = re.compile(r'(https?://[^\s]+)')
        self.chequeo_remind.start()

    def cog_unload(self):
        self.chequeo_remind.cancel()

	# Función síncrona que maneja la descarga en el almacenamiento
    def procesar_descarga(self, url, codec):
        opciones = {
			'outtmpl': 'temp_%(extractor)s_%(id)s.%(ext)s',
			'noplaylist': True,  
			'quiet': True,
			'no_warnings': True,
            # 'cookiefile': 'cookies.txt'
		}

        # Ajustae las calidades según el parámetro recibidos
        if codec == "h265":
            opciones['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            opciones['format_sort'] = ['vcodec:h265', 'ext:mp4:m4a']
        elif codec == "alta":
            opciones['format'] = 'bestvideo+bestaudio/best'
            opciones['format_sort'] = ['ext:mp4:m4a']
        elif codec == "baja":
            opciones['format'] = 'worstvideo[ext=mp4]+worstaudio[ext=m4a]/worst[ext=mp4]/worst'
        else:
            # h264 (Por defecto)
            opciones['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            opciones['format_sort'] = ['vcodec:h264', 'ext:mp4:m4a']

        with yt_dlp.YoutubeDL(opciones) as ydl:
			# Extraemos la info y descargamos el archivo al almacenamiento local
            info = ydl.extract_info(url, download=True)
            nombre_archivo = ydl.prepare_filename(info)
            return nombre_archivo

    @commands.command(name="video", aliases=["videos", "descargar"], help="Descarga uno o varios videos de plataformas como TikTok, IG, X, Twitch, Pinterest, etc.")
    async def fetch_multiple_videos(self, ctx, *, enlaces: str):
		# Codecs validos y el codec base.
        codecs_validos = ["h264", "h265", "alta", "baja"]
        codec_elegido = "h264"

        palabras = enlaces.split()
        if palabras and palabras[0].lower() in codecs_validos:
            codec_elegido = palabras[0].lower()

		# Buscar todos los enlaces en el mensaje proporcionado
        enlaces = self.url_pattern.findall(enlaces)

        if not enlaces:
            await ctx.send("⚠️ No encontré ningún enlace en tu mensaje.")
            return

		# Para no hacer spam, limitamos a un máximo razonable por comando (ej. 5 enlaces a la vez)
        limite_enlaces = 5
        if len(enlaces) > limite_enlaces:
            await ctx.send(f"⚠️ Has enviado demasiados enlaces. Solo procesaré los primeros {limite_enlaces}.")
            enlaces = enlaces[:limite_enlaces]

        await ctx.send(f"🔍 Se han detectado **{len(enlaces)}** enlace(s). Procesando...")

        for index, url in enumerate(enlaces, start=1):
            mensaje_progreso = await ctx.send(f"⏳ Descargando video {index}/{len(enlaces)}...\n`{url}`")
            nombre_archivo = None

            try:
				# Ejecutamos la descarga en un hilo secundario para no congelar el bot
                nombre_archivo = await asyncio.to_thread(self.procesar_descarga, url, codec_elegido)

				# Verificamos el peso del archivo (Límite de Discord: 25MB)
                peso_archivo = os.path.getsize(nombre_archivo)
                limite_mb = 25 * 1024 * 1024

                if peso_archivo > limite_mb:
                    await mensaje_progreso.edit(content=f"❌ El video {index}/{len(enlaces)} pesa más de 25MB y no se puede enviar por Discord.")

                else:
					# Preparamos y enviamos el archivo
                    archivo = discord.File(nombre_archivo)
                    await ctx.send(content=f"🎬 **Video {index}/{len(enlaces)}** solicitado por {ctx.author.mention}:", file=archivo)
                    await mensaje_progreso.delete()

            except DownloadError as e:
                error_str = str(e).lower()

                if "too many requests" in error_str or "http error 429" in error_str:
                    await mensaje_progreso.edit(content=f"⚠️ Parece que la pagina me esta bloqueando para descargar el video **{index}** (too many requests). Espera unos segundos y vuelve a intentar descargar `{url}`")
                elif "connection reset by peer" in error_str or "eerrno 104" in error_str:
                    await mensaje_progreso.edit(content=f"📡 La conexión se cerro de golpe, parece que el servidor de esa web esta fallando para descargar el video **{index}**. Intenta denuevo a descargar `{url}`.")
                elif "no address associated with hostname" in error_str or "errno 7" in error_str:
                    await mensaje_progreso.edit(content=f"🔌 El servidor en el cual estoy alojado (dentro del pobre de Asf) ha tenido un fallo en la red, y simplemente ha detenido la descarga del video **{index}**. Reintenta en cuanto Asf decida comprarse un buen internet.")
                else:
                    await mensaje_progreso.edit(content=f"❌ No se pudo descargar el video {index}. Puede que el enlace sea privado, no contenga video o la plataforma no sea compatible.")
                    print(f"Error procesando {url}: {e}")

            except Exception as e:
                print(f"Error general procesando {url}: {e}")

            finally:
				# BLOQUE DE LIMPIEZA CRÍTICO
				# Esto se ejecuta SIEMPRE, haya ocurrido un error o no, garantizando que tu almacenamiento no se llene
                if nombre_archivo and os.path.exists(nombre_archivo):
                    try:
                        os.remove(nombre_archivo)
                    except Exception as e:
                        print(f"No se pudo borrar el archivo temporal {nombre_archivo}: {e}")

		# Pequeña pausa entre descargas para no saturar la red ni ser bloqueados por la API de Discord
        await asyncio.sleep(2)

    @commands.command(aliases=["recordar"], help="Usalo para crear recordatorios.")
    async def remind(self, ctx, tiempo: str, *, recordatorio: str):
        conversion = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800, "mo": 2592000}

        tiempo = tiempo.lower()
        if tiempo.endswith("mo"):
            cantidad = tiempo[:-2]
            unidad = "mo"
        else:
            cantidad = tiempo[:-1]
            unidad = tiempo[-1]

        if unidad not in conversion or not cantidad.isdigit():
            await ctx.send("❌ Formato incorrecto. Usa `10s`, `5m`, `2h`, `7d`, `2w` o `1mo`.")
            return
        
        st = int(cantidad) * conversion[unidad]
        tf = int(time.time() + st)

        # Guardar reminder en la base
        db_remind.add_remind(ctx.author.id, tf, ctx.channel.id, recordatorio)

        await ctx.send(f"Recordatorio listo, te avisare <t:{tf}:R>")

    @tasks.loop(seconds=1)
    async def chequeo_remind(self):
        tiempo_actual = int(time.time())

        reminds_vencidos = db_remind.check_loop(tiempo_actual)

        if not reminds_vencidos:
            return

        for row in reminds_vencidos:
            db_id, user_id, channel_id, message = row

            channel = self.bot.get_channel(channel_id)
            if channel:
                try:
                    await channel.send(f"<@{user_id}>, ¡Ha transcurrido el tiempo (<t:{tiempo_actual}:R>), y llego el momento acordado de `{message}`!")
                except Exception as e:
                    print(f"No pude enviar un recordatorio en el canal {channel_id}: {e}")

            db_remind.del_remind(db_id)

    @chequeo_remind.before_loop
    async def previo_chequeo(self):
        await self.bot.wait_until_ready()

    @commands.command(aliases=["calculadora", "calcula", "calc"])
    async def math(self, ctx, *, expresion: str):
        expresion = re.sub(r'[^0-9+\-*/(). ]', '', expresion)

        if not expresion.strip():
            await ctx.send("❌ No hay nada que pueda calcular ahi, bwam...")
            return

        try:
            resultado=eval(expresion)

            embed=embeds.crear(
				"happy",
				"__ Calculadora __",
				f""".	**Expresion**
    ```css
{expresion}```
.	**Resultado**
    ```css
{resultado}```
"""
            )

            await ctx.send(embed=embed)

        except ZeroDivisionError:
            embed=embeds.crear(
                "sigh",
                "Corazón, esa matematica esta mal.",
                "Intenta dividirte a ti mismo mejor.\n",
                discord.Colour.red()
            )

            await ctx.send(embed=embed)
        except Exception:
            await ctx.send(embed=embeds.crear(
                    "sigh",
                    "La operación es ilegible",
                    "¿Sabés calcular verdad?\n",
                    discord.Colour.red()
                    )
            )

async def setup(bot):
    await bot.add_cog(Utilidades(bot))

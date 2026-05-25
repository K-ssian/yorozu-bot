import sqlite3
import os

BASE_DIR = os.path.dirname(
	os.path.abspath(__file__)
)

DB_PATH = os.path.join(
	BASE_DIR,
	"prefixes.db"
)

# Realizar conexion con SQLite3
conexion=sqlite3.connect(DB_PATH)

# Funcion para modificar datos.
cursor=conexion.cursor()

# Crear tabla en caso de no existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS prefixes (

    guild_id INTEGER PRIMARY KEY,
    prefix TEXT

)
""")

# Guardar Datos
conexion.commit()

# Obtener Prefix
def recib_prefix(guild_id):
	cursor.execute(
		"""
		SELECT prefix
		FROM prefixes
		WHERE guild_id = ?
		""",
		(guild_id,)
	)
	resultado = cursor.fetchone()

	if resultado:
		return resultado[0]
	return "!"

# Guardar Prefix
def guardar_prefix(guild_id, prefix):
	cursor.execute(
		"""
		INSERT OR REPLACE INTO prefixes
		VALUES (?, ?)
		""",
		(guild_id, prefix)
	)
	conexion.commit()

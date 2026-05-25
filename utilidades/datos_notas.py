import sqlite3
import os

BASE_DIR = os.path.dirname(
	os.path.abspath(__file__)
)

DB_PATH = os.path.join(
	BASE_DIR,
	"notas.db"
)

# Realizar conexion con SQLite3
conexion=sqlite3.connect(DB_PATH)

# Funcion para modificar datos.
cursor=conexion.cursor()

# Crear tabla en caso de no existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS prefixes (

    user_id INTEGER PRIMARY KEY,
    nota TEXT

)
""")

# Guardar Datos
conexion.commit()

# Obtener Nota
def get_nota(guild_id):
	cursor.execute(
		"""
		SELECT nota
		FROM notas
		WHERE user_id = ?
		""",
		(user_id,)
	)
	resultado = cursor.fetchone()

	if resultado:
		return resultado[0]
	return "Ninguna nota."

# Guardar Nota
def save_nota(user_id, contenido):
	cursor.execute(
		"""
		INSERT OR REPLACE INTO notas
		VALUES (?, ?)
		""",
		(user_id, contenido)
	)
	conexion.commit()

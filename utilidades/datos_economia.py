import sqlite3
import os

BASE_DIR = os.path.dirname(
	os.path.abspath(__file__)
)

DB_PATH = os.path.join(
	BASE_DIR,
	"economia.db"
)

# Realizar conexion con SQLite3
conexion=sqlite3.connect(DB_PATH)

# Funcion para modificar datos.
cursor=conexion.cursor()

# Crear tabla en caso de no existir

cursor.execute("""
CREATE TABLE IF NOT EXISTS economia (

    user_id INTEGER PRIMARY KEY,
    dinero INTEGER

)
""")

# Guardar Datos
conexion.commit()

### FUNCIONES INTERNAS: ECONOMIA

# Crear balance de dinero
def crear_balance(user_id):

	cursor.execute(
		"""
		INSERT OR IGNORE INTO economia
		VALUES (?, ?)
		""",
		(user_id, 0)
	)
	conexion.commit()

# Obtener dinero
def get_balance(user_id):

	crear_balance(user_id)

	cursor.execute(
		"""
		SELECT dinero
		FROM economia
		WHERE user_id = ?
		""",
		(user_id,)
	)
	balance=cursor.fetchone()
	if balance:
		return balance[0]
	return 0

# Modificar/Guardar dinero
def set_balance(user_id, amount):

	crear_balance(user_id)

	cursor.execute(
		"""
		UPDATE economia
		SET dinero = ?
		WHERE user_id = ?
		""",
		(amount, user_id)
	)
	conexion.commit()

def add_balance(user_id, amount):

	crear_balance(user_id)

	cursor.execute(
		"""
		UPDATE economia
		SET dinero = dinero + ?
		WHERE user_id = ?
		""",
		(amount, user_id)
	)
	conexion.commit()

def remove_balance(user_id, amount):

	crear_balance(user_id)

	cursor.execute(
		"""
		UPDATE economia
		SET dinero = dinero - ?
		WHERE user_id = ?
		""",
		(amount, user_id)
	)
	conexion.commit()

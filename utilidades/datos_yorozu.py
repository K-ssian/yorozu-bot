import sqlite3
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "yorozu_memoria.db")

# Conexión
conexion = sqlite3.connect(DB_PATH)
cursor = conexion.cursor()

# Creamos la tabla (canal_id como clave primaria y el historial como texto JSON)
cursor.execute('''
CREATE TABLE IF NOT EXISTS memoria (
    canal_id INTEGER PRIMARY KEY,
    historial TEXT
)
''')
conexion.commit()

# --- FUNCIONES ---

def get_historial(canal_id):
    """Busca el historial del canal y lo convierte de texto a una lista de Python."""
    cursor.execute("SELECT historial FROM memoria WHERE canal_id = ?", (canal_id,))
    resultado = cursor.fetchone()
    
    if resultado:
        # json.loads() transforma el texto guardado de vuelta a la lista original
        return json.loads(resultado[0])
    return None

def save_historial(canal_id, historial_list):
    """Convierte la lista en texto JSON y la guarda/actualiza en la base de datos."""
    # json.dumps() transforma la lista de diccionarios en un string de texto
    historial_texto = json.dumps(historial_list)
    
    cursor.execute(
        """
        INSERT OR REPLACE INTO memoria (canal_id, historial)
        VALUES (?, ?)
        """,
        (canal_id, historial_texto)
    )
    conexion.commit()

def delete_historial(canal_id):
    """Borra el registro de la base de datos."""
    cursor.execute("DELETE FROM memoria WHERE canal_id = ?", (canal_id,))
    conexion.commit()

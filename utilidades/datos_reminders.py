import sqlite3
import time
from discord.ext import tasks, commands
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "reminders.db")


# CONEXIÓN Y CREACIÓN DE LA BASE DE DATOS
conexion = sqlite3.connect(DB_PATH)
cursor = conexion.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        channel_id INTEGER,
        target_time REAL,
        message TEXT
    )
''')

conexion.commit()

# FUNCIONES DE EDICIÓN DE BASE

def get_owner_remind(db_id):
    cursor.execute("SELECT user_id FROM reminders WHERE id = ?", (db_id,))
    resultado = cursor.fetchone()
    
    if resultado:
        return resultado[0]
    return None

def add_remind(usuario, tiempo, canal, mensaje):
	cursor.execute(
		"INSERT INTO reminders (user_id, channel_id, target_time, message) VALUES (?, ?, ?, ?)",
		(usuario, canal, tiempo, mensaje)
    )
	conexion.commit()

def check_loop(tiempo_actual):
    cursor.execute("SELECT id, user_id, channel_id, message FROM reminders WHERE target_time <= ?", (tiempo_actual,))
    return cursor.fetchall()

def check_allreminders(usuario):
    cursor.execute("SELECT id, target_time, message FROM reminders WHERE user_id = ? ORDER BY target_time ASC", (usuario,))
    return cursor.fetchall()

def del_remind(db_id):
	
    cursor.execute("DELETE FROM reminders WHERE id = ?", (db_id,))
    conexion.commit()

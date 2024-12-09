import sqlite3
from logs.logs import logs
from tkinter.messagebox import showerror


def connection():
    try:
        con = sqlite3.connect('database/productos.db')
        return con
    except sqlite3.Error as e:
        logs(f'Error conecting with database - {e}')
        showerror('Error', 'Problema al conectarse con la base de datos')

def create_table():
    con = connection()
    cursor = con.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS productos
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto varchar(20) NOT NULL,
    fecha TEXT NOT NULL,
    precio REAL NOT NULL)
    """
    try:
        cursor.execute(query)
        con.commit()
    except sqlite3.Error as e:
        logs(f'Error creating database - {e}')
        showerror('Error', 'Problema al crear la tabla en la base de datos')
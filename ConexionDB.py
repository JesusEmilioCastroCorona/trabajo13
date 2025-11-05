# ConexionDB.py

import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

class ConexionDB:
    def __init__(self, host, database, user, password):
        """Inicializa la clase con las credenciales de la base de datos."""
        self.host = host
        self.database = database
        self.user = user
        self.password = toor
        self.connection = None

    def __get_connection(self):
        """Establece una conexión si no existe o si se ha cerrado."""
        if self.connection is None or not self.connection.is_connected():
            try:
                # ATENCIÓN: Esta función puede mostrar un error si las credenciales son incorrectas
                self.connection = mysql.connector.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password
                )
                return self.connection
            except Error as e:
                messagebox.showerror("Error de Conexión", 
                                     f"No se pudo conectar a MySQL. Revise las credenciales y el servidor. Error: {e}")
                return None
        return self.connection
    
    def execute_query(self, query, params=None, fetch=False):
        """Ejecuta una consulta SQL, usando parámetros para evitar inyección SQL."""
        conn = self.__get_connection()
        if conn is None:
            return None if fetch else False
        
        try:
            cursor = conn.cursor()
            # Uso de parámetros (%s) para consultas seguras
            cursor.execute(query, params or ()) 
            
            if fetch:
                results = cursor.fetchall()
                cursor.close()
                return results
            else:
                conn.commit()
                cursor.close()
                return True
        except Error as e:
            messagebox.showerror("Error SQL", f"No se pudo completar la operación en la DB. Error: {e}")
            return None if fetch else False

def crear_tabla_empleados(db_manager):
    """Crea la tabla de empleados si no existe (ID Auto-Generado)."""
    query = """
    CREATE TABLE IF NOT EXISTS empleados (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        sexo VARCHAR(10) NOT NULL,
        correo VARCHAR(100) UNIQUE NOT NULL
    )
    """
    db_manager.execute_query(query)
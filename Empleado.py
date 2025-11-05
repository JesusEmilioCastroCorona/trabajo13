# Empleado.py

from ConexionDB import ConexionDB 
from mysql.connector import Error
from tkinter import messagebox

class Empleado:
    """Clase que representa el modelo de datos de un empleado (POO)."""
    def __init__(self, nombre, sexo, correo, id=None):
        self.id = id 
        self.nombre = nombre
        self.sexo = sexo
        self.correo = correo

class EmpleadoManager:
    """Clase que maneja las operaciones CRUD de los empleados con la base de datos."""
    def __init__(self, db_manager):
        self.db = db_manager

    def agregar_empleado(self, empleado):
        """Añadir empleado."""
        query = "INSERT INTO empleados (nombre, sexo, correo) VALUES (%s, %s, %s)"
        params = (empleado.nombre, empleado.sexo, empleado.correo)
        return self.db.execute_query(query, params)

    def ver_empleados(self):
        """Ver empleados. Retorna una lista de objetos Empleado."""
        query = "SELECT id, nombre, sexo, correo FROM empleados ORDER BY id DESC"
        results = self.db.execute_query(query, fetch=True)
        if results:
            return [Empleado(r[1], r[2], r[3], r[0]) for r in results]
        return []

    def eliminar_empleado(self, empleado_id):
        """Eliminar empleado."""
        query = "DELETE FROM empleados WHERE id = %s"
        params = (empleado_id,)
        return self.db.execute_query(query, params)

    def obtener_todos_para_exportar(self):
        """
        [MÉTODO REQUERIDO PARA LA EXPORTACIÓN CSV]
        Obtiene todos los datos y encabezados para la exportación CSV.
        """
        query = "SELECT id, nombre, sexo, correo FROM empleados"
        
        # Acceder al método de conexión de forma protegida
        conn = self.db._ConexionDB__get_connection() 
        if conn is None:
            return None, None
        
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            
            # Obtener los nombres de las columnas para usarlos como encabezados en el CSV
            columns = [i[0] for i in cursor.description]
            cursor.close()
            return columns, data
        except Error as e:
            messagebox.showerror("Error de Exportación", f"Error al leer datos para CSV: {e}")
            return None, None
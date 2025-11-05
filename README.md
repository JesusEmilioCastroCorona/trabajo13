# 🧾 Sistema de Registro de Empleados

Un sistema de escritorio desarrollado en **Python** con interfaz gráfica **Tkinter**, que permite **registrar, listar, eliminar y exportar empleados** utilizando una base de datos **MySQL**.  
El diseño modular separa la interfaz, la conexión a la base de datos y la lógica del negocio en archivos independientes para facilitar el mantenimiento.

---

## 📂 Estructura del Proyecto

📁 proyecto_registro_empleados/
│
├── AppGUI.py # Interfaz gráfica principal (Tkinter)
├── ConexionDB.py # Módulo para la conexión y gestión de la base de datos
├── Empleado.py # Clases del modelo de empleado y su gestor CRUD
├── fondo.png # Imagen opcional de fondo para la interfaz
├── saludo.gif # GIF opcional para ventana de mensaje secreto
└── README.md # Documento explicativo del sistema

yaml
Copiar código

---

## ⚙️ Requisitos

Antes de ejecutar el sistema, asegúrate de tener instalado:

- **Python 3.8 o superior**
- **MySQL Server**
- Librerías necesarias:

```bash
pip install mysql-connector-python pillow
🧠 Descripción del Sistema
El sistema se divide en tres módulos principales:

1. ConexionDB.py
Encargado de la conexión segura con la base de datos MySQL.
Incluye funciones para ejecutar consultas (execute_query) y crear la tabla empleados si no existe.

Estructura de la tabla:

sql
Copiar código
CREATE TABLE empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    sexo VARCHAR(10) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL
);
2. Empleado.py
Contiene:

La clase Empleado, que modela los atributos básicos de un empleado (id, nombre, sexo, correo).

La clase EmpleadoManager, que gestiona las operaciones CRUD:

agregar_empleado(): inserta nuevos registros.

ver_empleados(): obtiene todos los empleados.

eliminar_empleado(): elimina un empleado por ID.

obtener_todos_para_exportar(): obtiene los datos para exportarlos a CSV.

3. AppGUI.py
Interfaz gráfica basada en Tkinter.
Permite interactuar con los datos de empleados de forma visual e intuitiva.

Características principales:

Formulario de registro con campos para nombre, sexo y correo.

Listado de empleados con opción de eliminar registros.

Exportación a CSV con el botón “Hackear ilegalmente la base de datos”.

Ventana secreta con animación GIF (“Hola Mundo”).

Botón de cierre “esquivo” que se mueve aleatoriamente al intentar presionarlo 😄.

Estilo visual personalizado con colores modernos y tipografía “pixel art”.

🧰 Ejecución del Programa
Crea la base de datos en MySQL:

sql
Copiar código
CREATE DATABASE registro_empleados;
Abre AppGUI.py y revisa la configuración de conexión en esta parte:

python
Copiar código
self.db = ConexionDB(
    host="localhost",
    database="registro_empleados",
    user="root",
    password="toor"
)
⚠️ Cambia user y password según tus credenciales locales de MySQL.

Ejecuta el programa:

bash
Copiar código
python AppGUI.py
¡Listo! Se abrirá la interfaz gráfica donde podrás:

Añadir nuevos empleados

Visualizarlos en una tabla

Eliminar registros

Exportar los datos a CSV

📤 Exportación de Datos
La opción “Hackear ilegalmente la base de datos” permite exportar todos los empleados registrados a un archivo .csv, con formato:

id	nombre	sexo	correo
1	Juan Pérez	Masculino	juan@example.com

💡 Extras y Detalles Técnicos
Librerías utilizadas:
tkinter, ttk, PIL (Pillow), mysql.connector, csv, random

Seguridad:
Las consultas usan parámetros (%s) para prevenir inyección SQL.

Diseño modular:
Separa la lógica de datos, la conexión y la interfaz en archivos independientes.

Compatibilidad:
Funciona en Windows, macOS y Linux (siempre que se tenga MySQL activo).

👨‍💻 Autor
Desarrollado por Emilio Pérez
Proyecto académico de práctica en Python + Tkinter + MySQL.

🏁 Licencia
Este proyecto es de libre uso con fines educativos.
Puedes modificarlo y adaptarlo a tus necesidades.

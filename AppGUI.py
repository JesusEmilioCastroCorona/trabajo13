# AppGUI.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import csv
# Librerías necesarias para el Ejercicio 14
from PIL import Image, ImageTk, ImageFont 

# Importa la lógica modular
from ConexionDB import ConexionDB, crear_tabla_empleados 
from Empleado import Empleado, EmpleadoManager

# --- Configuración Global de Estilos ---
class CustomStyle:
    """Clase para manejar estilos personalizados y fuente Pixel Art."""
    def __init__(self):
        self.style = ttk.Style()
        
        # Intento de cargar fuente Pixel Art (debe estar en la misma carpeta)
        try:
            # Nota: Solo declaramos el nombre de la fuente aquí para el estilo de ttk
            self.tk_font = ('pixel_font', 16) 
        except:
            # Fuente de fallback
            self.tk_font = ('Consolas', 12) 
            
        self.style.configure('TButton', font=self.tk_font, padding=10)

        # Colores para estilos base
        self.style.configure('Hackear.TButton', background='#c0392b', foreground='white', font=self.tk_font)
        self.style.configure('Mensaje.TButton', background='#2980b9', foreground='white', font=self.tk_font)
        self.style.configure('Añadir.TButton', background='#27ae60', foreground='white', font=self.tk_font)
        self.style.configure('Eliminar.TButton', background='#c0392b', foreground='white', font=self.tk_font)

class AppGUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        
        self.style_manager = CustomStyle()
        self._load_background() # Cargar la imagen de fondo

        # Configuración de la conexión a la DB y el Manager
        self.db = ConexionDB(
            host="localhost", 
            database="registro_empleados", 
            user="root", # ¡ATENCIÓN: REEMPLAZA ESTO!
            password="toor" 
        )
        crear_tabla_empleados(self.db) 
        self.manager = EmpleadoManager(self.db)
        
        self.createWidgets()
        self.cargar_empleados()
        
        self.gif_frame_index = 0
        self.gif_frames = []

    def _load_background(self):
        """Agrega una imagen de fondo a la interfaz principal."""
        try:
            image = Image.open("fondo.png") 
            width, height = 800, 600
            image = image.resize((width, height), Image.Resampling.LANCZOS)
            
            self.bg_image = ImageTk.PhotoImage(image)
            
            bg_label = tk.Label(self.master, image=self.bg_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
            self.grid(sticky="nsew")
            self.config(bg="") # Permite ver el fondo
            
        except FileNotFoundError:
            messagebox.showwarning("Advertencia", "No se encontró 'fondo.png'. Usando fondo oscuro por defecto.")
            self.config(bg="#2c3e50")
            self.grid(sticky="nsew")
        except Exception as e:
            messagebox.showerror("Error de Imagen", f"Error al cargar la imagen de fondo: {e}")
            self.config(bg="#2c3e50")
            self.grid(sticky="nsew")


    def createWidgets(self):
        # Configuración del Notebook (Pestañas)
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Se usan Frames normales con fondo para que los elementos se vean sobre la imagen
        frame_registro = tk.Frame(self.notebook, bg="#34495e", padx=15, pady=15, bd=5, relief=tk.RAISED)
        self.notebook.add(frame_registro, text=' ➕ Registro ')
        self._create_registro_form(frame_registro)

        frame_listado = tk.Frame(self.notebook, bg="#34495e", padx=15, pady=15, bd=5, relief=tk.RAISED)
        self.notebook.add(frame_listado, text=' 📋 Listado ')
        self._create_listado_table(frame_listado)

        # Frame para botones de funciones nuevas (Reorganización de elementos)
        frame_funcionalidades = tk.Frame(self, bg="#2c3e50", padx=10, pady=10)
        frame_funcionalidades.grid(row=1, column=0, pady=(0, 20), sticky="ew")
        frame_funcionalidades.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Botón "Hackear Ilegalmente la Base de Datos"
        btn_hackear = ttk.Button(frame_funcionalidades, text="Hackear Ilegalmente la Base de Datos", 
                                 command=self.exportar_a_csv, style='Hackear.TButton')
        btn_hackear.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self._add_hover_effect(btn_hackear, '#e74c3c') # Rojo más claro en hover
        
        # Botón "Click aquí para mensaje interesante"
        btn_mensaje = ttk.Button(frame_funcionalidades, text="Click aquí para mensaje interesante", 
                                 command=self.mostrar_ventana_secreta, style='Mensaje.TButton')
        btn_mensaje.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self._add_hover_effect(btn_mensaje, '#3498db') # Azul más claro en hover

        # Botón "Cerrar" que se mueve aleatoriamente
        self._crear_boton_esquivo(frame_funcionalidades) 

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def _add_hover_effect(self, widget, hover_color):
        """
        CORRECCIÓN DEL ERROR DE TCL: 
        Implementa el efecto de hover usando ttk.Style.map() para cambiar el background
        cuando el widget está en el estado 'active' (mouse encima o presionado).
        """
        style_name = widget['style']
        
        # Mapea el color de fondo para el estado 'active'.
        self.style_manager.style.map(
            style_name, 
            background=[('active', hover_color)], 
            # Mantiene el texto blanco para el estado activo/hover
            foreground=[('active', 'white')]
        )
        

    def _create_registro_form(self, frame):
        """Crea el formulario para Añadir Empleado."""
        
        tk.Label(frame, text="Nombre:", fg="white", bg="#34495e", font=self.style_manager.tk_font).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_nombre = ttk.Entry(frame, width=40)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        tk.Label(frame, text="Sexo:", fg="white", bg="#34495e", font=self.style_manager.tk_font).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.sexo_var = tk.StringVar(value='Masculino')
        radio_frame = tk.Frame(frame, bg="#34495e")
        radio_frame.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        tk.Radiobutton(radio_frame, text="Masculino", variable=self.sexo_var, value="Masculino", fg="white", bg="#34495e", selectcolor="#2ecc71").pack(side="left", padx=5)
        tk.Radiobutton(radio_frame, text="Femenino", variable=self.sexo_var, value="Femenino", fg="white", bg="#34495e", selectcolor="#2ecc71").pack(side="left")
        
        tk.Label(frame, text="Correo:", fg="white", bg="#34495e", font=self.style_manager.tk_font).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_correo = ttk.Entry(frame, width=40)
        self.entry_correo.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.btn_anadir = ttk.Button(frame, text="Añadir Empleado", command=self.anadir_empleado, style='Añadir.TButton')
        self.btn_anadir.grid(row=3, column=0, columnspan=2, pady=20)
        self._add_hover_effect(self.btn_anadir, '#2ecc71') # Verde más claro en hover
        
        frame.grid_columnconfigure(1, weight=1)

    def _create_listado_table(self, frame):
        """Crea la tabla (Treeview) para Ver y Eliminar Empleados."""
        
        columns = ("id", "nombre", "sexo", "correo")
        self.tree = ttk.Treeview(frame, columns=columns, show='headings', height=10)
        
        self.tree.heading("id", text="ID (Auto)") 
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("sexo", text="Sexo")
        self.tree.heading("correo", text="Correo")
        
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("nombre", width=180)
        self.tree.column("sexo", width=90, anchor="center")
        self.tree.column("correo", width=250)

        self.tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.btn_eliminar = ttk.Button(frame, text="Eliminar Empleado Seleccionado", command=self.eliminar_empleado, style='Eliminar.TButton') 
        self.btn_eliminar.grid(row=1, column=0, columnspan=2, pady=10)
        self._add_hover_effect(self.btn_eliminar, '#e74c3c') # Rojo más claro en hover
        
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        
    def _crear_boton_esquivo(self, parent_frame):
        """Crea el botón 'Cerrar' que se mueve aleatoriamente."""
        
        self.boton_esquivo = tk.Button(parent_frame, text="Cerrar", command=self.master.quit, 
                                        fg='white', bg='#880000', font=self.style_manager.tk_font, bd=0, relief='flat', activebackground='red')
        
        self.boton_esquivo.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        
        self.boton_esquivo.bind("<Enter>", self._mover_boton)

    def _mover_boton(self, event):
        """Lógica para mover el botón aleatoriamente."""
        if self.boton_esquivo.winfo_ismapped():
            parent_width = self.boton_esquivo.master.winfo_width()
            parent_height = self.boton_esquivo.master.winfo_height()
            
            btn_width = self.boton_esquivo.winfo_width()
            btn_height = self.boton_esquivo.winfo_height()
            
            # Calcula nuevas coordenadas aleatorias
            new_x = random.randint(0, max(1, parent_width - btn_width))
            new_y = random.randint(0, max(1, parent_height - btn_height))

            # Lo quita de la rejilla para reposicionarlo con place()
            self.boton_esquivo.grid_forget()
            self.boton_esquivo.place(x=new_x, y=new_y)
            
    # --- Métodos de Interacción (Lógica) ---

    def cargar_empleados(self):
        """Carga los empleados de la DB y actualiza el Treeview (Ver empleados)."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        empleados = self.manager.ver_empleados()
        for emp in empleados:
            self.tree.insert('', tk.END, values=(emp.id, emp.nombre, emp.sexo, emp.correo))

    def anadir_empleado(self):
        """Procesa el formulario para Añadir empleado."""
        nombre = self.entry_nombre.get().strip()
        sexo = self.sexo_var.get()
        correo = self.entry_correo.get().strip()

        if not nombre or not correo:
            messagebox.showerror("Error", "Nombre y Correo no pueden estar vacíos.")
            return

        nuevo_empleado = Empleado(nombre, sexo, correo)
        
        if self.manager.agregar_empleado(nuevo_empleado):
            messagebox.showinfo("Éxito", "Empleado añadido correctamente.")
            self.entry_nombre.delete(0, tk.END)
            self.entry_correo.delete(0, tk.END)
            self.cargar_empleados()
            self.notebook.select(1) 

    def eliminar_empleado(self):
        """Procesa la eliminación del empleado seleccionado."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un empleado para eliminar.")
            return

        empleado_id = self.tree.item(selected_item, 'values')[0]
        
        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar al ID: {empleado_id}?"):
            if self.manager.eliminar_empleado(empleado_id):
                messagebox.showinfo("Éxito", "Empleado eliminado.")
                self.cargar_empleados()

    def exportar_a_csv(self):
        """Función 'Hackear Ilegalmente la Base de Datos' que exporta a CSV."""
        columns, data = self.manager.obtener_todos_para_exportar()
        
        if not data:
            messagebox.showinfo("Exportación Fallida", "No hay datos de empleados para exportar.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Selecciona dónde guardar el archivo CSV"
        )

        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(columns) # Escribe los encabezados
                    writer.writerows(data) # Escribe los datos
                messagebox.showinfo("Hackeo Exitoso", f"Base de datos 'ilegalmente' exportada a:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error de Archivo", f"No se pudo escribir el archivo: {e}")

    def mostrar_ventana_secreta(self):
        """Abre una nueva ventana y muestra un GIF animado."""
        
        new_window = tk.Toplevel(self.master)
        new_window.title("Hola Mundo") 
        new_window.geometry("300x300")
        new_window.config(bg='black')

        gif_label = tk.Label(new_window, bg='black')
        gif_label.pack(expand=True)
        
        try:
            self.gif_frames = []
            img = Image.open("saludo.gif")
            
            for i in range(0, img.n_frames):
                img.seek(i)
                frame = img.copy() 
                frame = frame.resize((200, 200), Image.Resampling.LANCZOS)
                self.gif_frames.append(ImageTk.PhotoImage(frame))
            
            self.gif_frame_index = 0
            self._animate_gif(gif_label)
            
        except FileNotFoundError:
            tk.Label(new_window, text="¡Hola Mundo!\n(GIF no encontrado)", fg="white", bg="black", font=("Arial", 16)).pack(expand=True)
        except Exception as e:
            tk.Label(new_window, text=f"Error cargando GIF: {e}", fg="white", bg="black").pack(expand=True)

    def _animate_gif(self, label):
        """Función recursiva para animar el GIF."""
        if not self.gif_frames:
            return
            
        label.config(image=self.gif_frames[self.gif_frame_index])
        
        self.gif_frame_index = (self.gif_frame_index + 1) % len(self.gif_frames)
        
        label.after(100, lambda: self._animate_gif(label))


# --- Bloque de Ejecución Principal ---

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Registro de Empleados Mejorado (Ejercicio 14)')
    root.geometry("800x600") 
    
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    
    app = AppGUI(master=root)
    root.mainloop()
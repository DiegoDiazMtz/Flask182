import tkinter as tk
from tkinter import ttk
import mysql.connector

conexion = mysql.connector.connect(host="localhost", user="root", database="bebidas")
cursor = conexion.cursor()

def mostrar_registros():
    consulta = """
    SELECT b.id, b.Nombre, b.Precio, c.clasificacion, m.Marca
    FROM Bebidas b
    JOIN Clasificaciones c ON b.id_clasificacion = c.id
    JOIN Marca m ON b.id_marca = m.id
    """
    cursor.execute(consulta)
    bebidas = cursor.fetchall()

    lista_registros = tk.Listbox(pestaña_mostrar, width=100)

    for bebida in bebidas:
        lista_registros.insert(tk.END, "ID: {} | Nombre: {} | Precio: {} | Clasificación: {} | Marca: {}".format(bebida[0], bebida[1], bebida[2], bebida[3], bebida[4]))

    lista_registros.pack()

def agregar_registro():
    etiqueta_nombre = tk.Label(pestaña_agregar, text="Nombre:")
    etiqueta_nombre.pack()
    campo_nombre = tk.Entry(pestaña_agregar)
    campo_nombre.pack()

    etiqueta_precio = tk.Label(pestaña_agregar, text="Precio:")
    etiqueta_precio.pack()
    campo_precio = tk.Entry(pestaña_agregar)
    campo_precio.pack()

    etiqueta_id_clasificacion = tk.Label(pestaña_agregar, text="ID Clasificación:")
    etiqueta_id_clasificacion.pack()
    campo_id_clasificacion = tk.Entry(pestaña_agregar)
    campo_id_clasificacion.pack()

    etiqueta_id_marca = tk.Label(pestaña_agregar, text="ID Marca:")
    etiqueta_id_marca.pack()
    campo_id_marca = tk.Entry(pestaña_agregar)
    campo_id_marca.pack()

    def agregar():
        nombre = campo_nombre.get()
        precio = campo_precio.get()
        id_clasificacion = campo_id_clasificacion.get()
        id_marca = campo_id_marca.get()

        consulta = "INSERT INTO Bebidas (Nombre, Precio, id_clasificacion, id_marca) VALUES ('{}', {}, {}, {})".format(nombre, precio, id_clasificacion, id_marca)
        cursor.execute(consulta)
        conexion.commit()
        print("Registro agregado correctamente.")

        campo_nombre.delete(0, tk.END)
        campo_precio.delete(0, tk.END)
        campo_id_clasificacion.delete(0, tk.END)
        campo_id_marca.delete(0, tk.END)

    boton_agregar = tk.Button(pestaña_agregar, text="Agregar", command=agregar)
    boton_agregar.pack()

def eliminar_registro():
    etiqueta_id = tk.Label(pestaña_eliminar, text="ID del registro a eliminar:")
    etiqueta_id.pack()
    campo_id = tk.Entry(pestaña_eliminar)
    campo_id.pack()

    def eliminar():
        id_registro = campo_id.get()

        consulta = "DELETE FROM Bebidas WHERE id = {}".format(id_registro)
        cursor.execute(consulta)
        conexion.commit()
        print("Registro eliminado correctamente.")

        campo_id.delete(0, tk.END)

    boton_eliminar = tk.Button(pestaña_eliminar, text="Eliminar", command=eliminar)
    boton_eliminar.pack()

def actualizar_registro():
    etiqueta_id = tk.Label(pestaña_actualizar, text="ID del registro a actualizar:")
    etiqueta_id.pack()
    campo_id = tk.Entry(pestaña_actualizar)
    campo_id.pack()

    etiqueta_nuevo_nombre = tk.Label(pestaña_actualizar, text="Nuevo nombre:")
    etiqueta_nuevo_nombre.pack()
    campo_nuevo_nombre = tk.Entry(pestaña_actualizar)
    campo_nuevo_nombre.pack()

    def actualizar():
        id_registro = campo_id.get()
        nuevo_nombre = campo_nuevo_nombre.get()

        consulta = "UPDATE Bebidas SET Nombre = '{}' WHERE id = {}".format(nuevo_nombre, id_registro)
        cursor.execute(consulta)
        conexion.commit()
        print("Registro actualizado correctamente.")

        campo_id.delete(0, tk.END)
        campo_nuevo_nombre.delete(0, tk.END)

    boton_actualizar = tk.Button(pestaña_actualizar, text="Actualizar", command=actualizar)
    boton_actualizar.pack()

ventana_principal = tk.Tk()
ventana_principal.title("Interfaz de Bebidas")

pestañas = ttk.Notebook(ventana_principal)

pestaña_mostrar = ttk.Frame(pestañas)
pestaña_agregar = ttk.Frame(pestañas)
pestaña_eliminar = ttk.Frame(pestañas)
pestaña_actualizar = ttk.Frame(pestañas)

pestañas.add(pestaña_mostrar, text="Mostrar registros")
pestañas.add(pestaña_agregar, text="Agregar registro")
pestañas.add(pestaña_eliminar, text="Eliminar registro")
pestañas.add(pestaña_actualizar, text="Actualizar registro")

pestañas.pack(expand=1, fill="both", padx=10, pady=10)

mostrar_registros()
agregar_registro()
eliminar_registro()
actualizar_registro()

ventana_principal.mainloop()

cursor.close()
conexion.close()

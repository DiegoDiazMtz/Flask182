import tkinter as tk 
from tkinter import ttk
import mysql.connector

# Establecer la conexión con la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    database="bebidas"
)

# Crear el cursor para ejecutar las consultas
cursor = conexion.cursor()

# Declarar la variable global para entidad_registro
entidad_registro = None

def mostrar_registros():
    global entidad_registro

    # Eliminar los registros existentes en la tabla si ya existe
    if entidad_registro:
        entidad_registro.destroy()

    # Consultar los datos de la tabla Bebidas con los nombres de clasificación y marca asociados
    consulta = """
    SELECT b.id, b.Nombre, b.Precio, c.clasificacion, m.Marca
    FROM Bebidas b
    JOIN Clasificaciones c ON b.id_clasificacion = c.id
    JOIN Marca m ON b.id_marca = m.id
    """
    cursor.execute(consulta)
    bebidas = cursor.fetchall()

    # Crear un widget Treeview para mostrar los registros en una tabla
    entidad_registro = ttk.Treeview(pestaña_mostrar, columns=("ID", "Nombre", "Precio", "Clasificación", "Marca"), show="headings")

    # Configurar las columnas de la tabla
    entidad_registro.heading("ID", text="ID")
    entidad_registro.heading("Nombre", text="Nombre")
    entidad_registro.heading("Precio", text="Precio")
    entidad_registro.heading("Clasificación", text="Clasificación")
    entidad_registro.heading("Marca", text="Marca")

    # Mostrar los datos obtenidos en la tabla
    for bebida in bebidas:
        entidad_registro.insert("", tk.END, values=(bebida[0], bebida[1], bebida[2], bebida[3], bebida[4]))

    # Ajustar el tamaño de la tabla al cambiar el tamaño de la ventana
    entidad_registro.pack(fill="both", expand=True)
    entidad_registro.bind("<Configure>", lambda e: entidad_registro.pack_configure(expand=True))

    # Centrar los registros en la tabla
    for column in ("ID", "Nombre", "Precio", "Clasificación", "Marca"):
        entidad_registro.column(column, anchor="center")

    # Establecer el ancho de las columnas de la tabla
    entidad_registro.column("ID", width=50)
    entidad_registro.column("Nombre", width=100)
    entidad_registro.column("Precio", width=80)
    entidad_registro.column("Clasificación", width=100)
    entidad_registro.column("Marca", width=100)


def ingresar_registro():
    # Crear etiquetas y campos de entrada para los datos del nuevo registro
    etiqueta_nombre = tk.Label(pestaña_ingreso, text="Nombre:")
    etiqueta_nombre.pack()
    campo_nombre = tk.Entry(pestaña_ingreso)
    campo_nombre.pack()

    etiqueta_precio = tk.Label(pestaña_ingreso, text="Precio:")
    etiqueta_precio.pack()
    campo_precio = tk.Entry(pestaña_ingreso)
    campo_precio.pack()

    # Obtener las clasificaciones de la base de datos
    cursor.execute("SELECT id, clasificacion FROM Clasificaciones")
    clasificaciones = cursor.fetchall()
    clasificaciones_ids = [clasificacion[0] for clasificacion in clasificaciones]
    clasificaciones_nombres = [clasificacion[1] for clasificacion in clasificaciones]

    # Obtener las marcas de la base de datos
    cursor.execute("SELECT id, Marca FROM Marca")
    marcas = cursor.fetchall()
    marcas_ids = [marca[0] for marca in marcas]
    marcas_nombres = [marca[1] for marca in marcas]

    etiqueta_clasificacion = tk.Label(pestaña_ingreso, text="Clasificación:")
    etiqueta_clasificacion.pack()
    campo_clasificacion = ttk.Combobox(pestaña_ingreso, values=clasificaciones_nombres)
    campo_clasificacion.pack()

    etiqueta_marca = tk.Label(pestaña_ingreso, text="Marca:")
    etiqueta_marca.pack()
    campo_marca = ttk.Combobox(pestaña_ingreso, values=marcas_nombres)
    campo_marca.pack()

    def ingresar():
        nombre = campo_nombre.get()
        precio = campo_precio.get()
        id_clasificacion = clasificaciones_ids[clasificaciones_nombres.index(campo_clasificacion.get())]
        id_marca = marcas_ids[marcas_nombres.index(campo_marca.get())]

        # Insertar el nuevo registro en la tabla Bebidas
        consulta = """
        INSERT INTO Bebidas (Nombre, Precio, id_clasificacion, id_marca)
        VALUES (%s, %s, %s, %s)
        """
        valores = (nombre, precio, id_clasificacion, id_marca)
        cursor.execute(consulta, valores)
        conexion.commit()

        # Mostrar mensaje de confirmación
        etiqueta_confirmacion.config(text="Registro agregado correctamente")

    # Crear un botón para ingresar el registro
    boton_ingresar = tk.Button(pestaña_ingreso, text="ingresar", command=ingresar)
    boton_ingresar.pack()

    # Crear una etiqueta para mostrar mensajes de confirmación
    etiqueta_confirmacion = tk.Label(pestaña_ingreso)
    etiqueta_confirmacion.pack()

campo_id = None  # Variable global para el Combobox

def eliminar_registro():
    campo_id = ttk.Combobox(pestaña_eliminar, values=[])  # Crear Combobox con lista vacía

    def refrescar_combobox():
        # Obtener los registros de la tabla Bebidas con sus IDs
        consulta = "SELECT id, Nombre FROM Bebidas"
        cursor.execute(consulta)
        registros = cursor.fetchall()

        # Crear una lista de registros con sus IDs
        lista_registros = [f"ID: {registro[0]}  {registro[1]}" for registro in registros]

        # Establecer los valores del Combobox
        campo_id['values'] = lista_registros

    # Llamar a la función para actualizar los valores del Combobox al cargar la pestaña
    refrescar_combobox()

    def eliminar():
        # Obtener el valor del registro seleccionado
        seleccion = campo_id.get()

        if seleccion:
            # Obtener el ID del registro seleccionado
            id_registro = seleccion.split('ID: ')[1].split()[0].strip()

            # Eliminar el registro con el ID especificado de la tabla Bebidas
            consulta = "DELETE FROM Bebidas WHERE id = %s"
            valores = (id_registro,)
            cursor.execute(consulta, valores)
            conexion.commit()

            # Mostrar mensaje de confirmación
            etiqueta_confirmacion.config(text="Registro eliminado correctamente")

            # Refrescar el Combobox después de eliminar el registro
            refrescar_combobox()
        else:
            etiqueta_confirmacion.config(text="No se ha seleccionado ningún registro")

    # Crear un Combobox con los registros y sus IDs
    campo_id = ttk.Combobox(pestaña_eliminar)
    campo_id.pack()

    # Crear un botón para refrescar el Combobox
    boton_refrescar = tk.Button(pestaña_eliminar, text="Refrescar", command=refrescar_combobox)
    boton_refrescar.pack()

    # Crear un botón para eliminar el registro
    boton_eliminar = tk.Button(pestaña_eliminar, text="Eliminar", command=eliminar)
    boton_eliminar.pack()

    # Crear una etiqueta para mostrar mensajes de confirmación
    etiqueta_confirmacion = tk.Label(pestaña_eliminar)
    etiqueta_confirmacion.pack()

    # Refrescar el Combobox al cargar la función eliminar_registro()
    refrescar_combobox()


def actualizar_registro():
    # Crear Combobox para seleccionar el registro a actualizar
    campo_id = ttk.Combobox(pestaña_actualizar, values=[], state="readonly")
    campo_id.pack()

    def refrescar_combobox():
        # Obtener los registros de la tabla Bebidas con sus IDs
        consulta = "SELECT id, Nombre FROM Bebidas"
        cursor.execute(consulta)
        registros = cursor.fetchall()

        # Crear una lista de registros con sus IDs
        lista_registros = [f"ID: {registro[0]}  {registro[1]}" for registro in registros]

        # Establecer los valores del Combobox
        campo_id['values'] = lista_registros

    def actualizar():
        seleccion = campo_id.get()
        if seleccion:
            # Obtener el ID del registro seleccionado
            id_registro = seleccion.split(':')[1].strip().split(' ')[0]

            nombre = campo_nombre.get()
            precio = campo_precio.get()
            id_clasificacion = clasificaciones_ids[combobox_clasificacion.current()]
            id_marca = marcas_ids[combobox_marca.current()]

            # Actualizar el registro con los nuevos valores en la tabla Bebidas
            consulta = "UPDATE Bebidas SET Nombre = %s, Precio = %s, id_clasificacion = %s, id_marca = %s WHERE id = %s"
            valores = (nombre, precio, id_clasificacion, id_marca, id_registro)
            cursor.execute(consulta, valores)
            conexion.commit()

            # Mostrar mensaje de confirmación
            etiqueta_confirmacion.config(text="Registro actualizado correctamente")
        else:
            etiqueta_confirmacion.config(text="No se ha seleccionado ningún registro")

    def refrescar():
        refrescar_combobox()
        etiqueta_confirmacion.config(text="")

    etiqueta_nombre = tk.Label(pestaña_actualizar, text="Nuevo nombre:")
    etiqueta_nombre.pack()
    campo_nombre = tk.Entry(pestaña_actualizar)
    campo_nombre.pack()

    etiqueta_precio = tk.Label(pestaña_actualizar, text="Nuevo precio:")
    etiqueta_precio.pack()
    campo_precio = tk.Entry(pestaña_actualizar)
    campo_precio.pack()

    etiqueta_clasificacion = tk.Label(pestaña_actualizar, text="Nueva clasificación:")
    etiqueta_clasificacion.pack()
    combobox_clasificacion = ttk.Combobox(pestaña_actualizar)
    combobox_clasificacion.pack()

    etiqueta_marca = tk.Label(pestaña_actualizar, text="Nueva marca:")
    etiqueta_marca.pack()
    combobox_marca = ttk.Combobox(pestaña_actualizar)
    combobox_marca.pack()

    # Botón de actualizar
    boton_actualizar = tk.Button(pestaña_actualizar, text="Actualizar", command=actualizar)
    boton_actualizar.pack()

    # Botón de refrescar
    boton_refrescar = tk.Button(pestaña_actualizar, text="Refrescar", command=refrescar)
    boton_refrescar.pack()

    # Crear una etiqueta para mostrar mensajes de confirmación
    etiqueta_confirmacion = tk.Label(pestaña_actualizar)
    etiqueta_confirmacion.pack()

    # Obtener las clasificaciones de la base de datos
    cursor.execute("SELECT id, clasificacion FROM Clasificaciones")
    clasificaciones = cursor.fetchall()
    clasificaciones_ids = [clasificacion[0] for clasificacion in clasificaciones]
    clasificaciones_nombres = [clasificacion[1] for clasificacion in clasificaciones]

    # Obtener las marcas de la base de datos
    cursor.execute("SELECT id, Marca FROM Marca")
    marcas = cursor.fetchall()
    marcas_ids = [marca[0] for marca in marcas]
    marcas_nombres = [marca[1] for marca in marcas]

    # Establecer las opciones de clasificación y marca en los comboboxes
    combobox_clasificacion['values'] = clasificaciones_nombres
    combobox_marca['values'] = marcas_nombres

    # Llamar a la función para actualizar los valores del Combobox al cargar la pestaña
    refrescar_combobox()

def calcular_precio_promedio():
    # Limpiar la pestaña antes de calcular el precio promedio
    for widget in pestaña_calcular.winfo_children():
        if widget != boton_calcular:  # Evitar eliminar el botón
            widget.destroy()
    
    # Calcular el precio promedio de las bebidas
    consulta_promedio = "SELECT AVG(Precio) FROM Bebidas"
    cursor.execute(consulta_promedio)
    precio_promedio = cursor.fetchone()[0]

    # Mostrar el resultado del precio promedio en una etiqueta
    etiqueta_promedio = tk.Label(pestaña_calcular)
    etiqueta_promedio.config(text=f"Precio promedio de las bebidas: {round(precio_promedio, 2)}")
    etiqueta_promedio.pack()

    # Consultar la cantidad de bebidas por marca
    consulta_marca = """
    SELECT m.Marca, COUNT(*) AS Cantidad
    FROM Bebidas b
    JOIN Marca m ON b.id_marca = m.id
    GROUP BY m.Marca
    """
    cursor.execute(consulta_marca)
    marcas = cursor.fetchall()

    # Mostrar la cantidad de bebidas por marca en una etiqueta
    etiqueta_marcas = tk.Label(pestaña_calcular)
    etiqueta_marcas.config(text="Cantidad de bebidas por marca:")
    etiqueta_marcas.pack()

    for marca in marcas:
        etiqueta_marca = tk.Label(pestaña_calcular)
        etiqueta_marca.config(text=f"{marca[0]}: {marca[1]} bebidas")
        etiqueta_marca.pack()

    # Consultar la cantidad de bebidas por clasificación
    consulta_clasificacion = """
    SELECT c.clasificacion, COUNT(*) AS Cantidad
    FROM Bebidas b
    JOIN Clasificaciones c ON b.id_clasificacion = c.id
    GROUP BY c.clasificacion
    """
    cursor.execute(consulta_clasificacion)
    clasificaciones = cursor.fetchall()

    # Mostrar la cantidad de bebidas por clasificación en una etiqueta
    etiqueta_clasificaciones = tk.Label(pestaña_calcular)
    etiqueta_clasificaciones.config(text="Cantidad de bebidas por clasificación:")
    etiqueta_clasificaciones.pack()

    for clasificacion in clasificaciones:
        etiqueta_clasificacion = tk.Label(pestaña_calcular)
        etiqueta_clasificacion.config(text=f"{clasificacion[0]}: {clasificacion[1]} bebidas")
        etiqueta_clasificacion.pack()


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Gestión de Bebidas")
ventana.geometry("600x400")

# Crear un control de pestañas para navegar entre las diferentes funcionalidades
pestañas = ttk.Notebook(ventana)

# Crear las pestañas para mostrar, ingresar, eliminar, actualizar y calcular
pestaña_mostrar = ttk.Frame(pestañas)
pestaña_ingreso = ttk.Frame(pestañas)
pestaña_eliminar = ttk.Frame(pestañas)
pestaña_actualizar = ttk.Frame(pestañas)
pestaña_calcular = ttk.Frame(pestañas)

# ingresar las pestañas al control de pestañas
pestañas.add(pestaña_mostrar, text="Consultar Registros Existentes")
pestañas.add(pestaña_ingreso, text="Ingresar Registro")
pestañas.add(pestaña_eliminar, text="Eliminar Registro")
pestañas.add(pestaña_actualizar, text="Actualizar Registro")
pestañas.add(pestaña_calcular, text="Consultas Generales")

# Mostrar el control de pestañas
pestañas.pack(expand=True, fill="both")

# Llamar a las funciones correspondientes para mostrar el contenido en las pestañas
ingresar_registro()
eliminar_registro()
actualizar_registro()

# Crear una etiqueta para mostrar el resultado del cálculo del precio promedio
etiqueta_resultado = tk.Label(pestaña_calcular)
etiqueta_resultado.pack()

# Crear botones para cada funcionalidad
boton_mostrar = tk.Button(pestaña_mostrar, text="Mostrar Registros", command=mostrar_registros)
boton_mostrar.pack()

boton_calcular = tk.Button(pestaña_calcular, text="Consultas generales", command=calcular_precio_promedio)
boton_calcular.pack()

# Iniciar el bucle principal de la aplicación
ventana.mainloop()

# Cerrar la conexión y liberar los recursos
cursor.close()
conexion.close()

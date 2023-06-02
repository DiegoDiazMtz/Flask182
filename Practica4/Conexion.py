import mysql.connector

# Establecer la conexión con la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bebidas"
)

# Crear el cursor para ejecutar las consultas
cursor = conexion.cursor()

# Consultar los datos de la tabla Bebidas
cursor.execute("SELECT * FROM Bebidas")
bebidas = cursor.fetchall()

# Mostrar los datos obtenidos
for bebida in bebidas:
    print("ID:", bebida[0])
    print("Nombre:", bebida[1])
    print("Precio:", bebida[2])
    print("ID Clasificación:", bebida[3])
    print("ID Marca:", bebida[4])
    print()

# Cerrar el cursor y la conexión
cursor.close()
conexion.close()
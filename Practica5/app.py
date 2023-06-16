
from flask import Flask


#inicialización del servidor Flask
app= Flask(__name__)
app.config['MYSQL_HOST']= "localhost"
app.config['MYSQL_USER']= "root"
app.config['MYSQL_PASSWORD']= ""
app.config['MYSQL_DB']= "dbflask"

#--- Declaración de rutas ---

# Ruta index o ruta principal http://localhost:5000
# La ruta se compone de nombre y función

@app.route('/')
def index():
    return "Hola Mundo"

@app.route('/guardar')
def guardar():
    return "Se guardó el album en la BD"

@app.route('/eliminar')
def eliminar():
    return "Se eliminó el album en la BD"




# Ejecución de servidor
if __name__== '__main__':
    app.run(port= 5000, debug=True)


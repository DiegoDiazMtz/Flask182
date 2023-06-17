
from flask import Flask, render_template, request


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
    return render_template('index.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method=='POST':
        titulo= request.form['txtTitulo']
        artista= request.form['txtArtista']
        anio= request.form['txtAnio']
        print(titulo, artista, anio)

    return "La info del Album llego a su ruta Amigo ;)"

@app.route('/eliminar')
def eliminar():
    return "Se eliminó el album en la BD"




# Ejecución de servidor
if __name__== '__main__':
    app.run(port= 5000, debug=True)


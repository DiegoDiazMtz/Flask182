
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


#inicialización del servidor Flask
app= Flask(__name__)
app.config['MYSQL_HOST']= "localhost"
app.config['MYSQL_USER']= "root"
app.config['MYSQL_PASSWORD']= ""
app.config['MYSQL_DB']= "dbflask"

app.secret_key= 'mysecretkey'

mysql= MySQL(app)

#--- Declaración de rutas ---

# Ruta index o ruta principal http://localhost:5000
# La ruta se compone de nombre y función

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method=='POST':
        Vtitulo= request.form['txtTitulo']
        Vartista= request.form['txtArtista']
        Vanio= request.form['txtAnio']
        #print(titulo, artista, anio)
        CS= mysql.connection.cursor()
        CS.execute('insert into albums (titulo, artista, anio) values (%s,%s,%s)', (Vtitulo, Vartista, Vanio))
        mysql.connection.commit()

    flash('Album Agregado Correctamente')    
    return redirect(url_for('index'))



@app.route('/eliminar')
def eliminar():
    return "Se eliminó el album en la BD"



# Ejecución de servidor
if __name__== '__main__':
    app.run(port= 5000, debug=True)


from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


# inicialización del servidor Flask
app = Flask(__name__)
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "dbflask"

app.secret_key = 'mysecretkey'

mysql = MySQL(app)

# --- Declaración de rutas ---

# Ruta index o ruta principal http://localhost:5000
# La ruta se compone de nombre y función


@app.route('/')
def index():
    curSelect = mysql.connection.cursor()
    curSelect.execute('select * from albums')
    consulta = curSelect.fetchall()
    # print(consulta)

    return render_template('index.html', listAlbums=consulta)


@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method == 'POST':
        Vtitulo = request.form['txtTitulo']
        Vartista = request.form['txtArtista']
        Vanio = request.form['txtAnio']

        CS = mysql.connection.cursor()
        CS.execute('insert into albums (titulo, artista, anio) values (%s,%s,%s)',
                   (Vtitulo, Vartista, Vanio))
        mysql.connection.commit()

    flash('Album Agregado Correctamente')
    return redirect(url_for('index'))


@app.route('/editar/<id>')
def editar(id):
    curEditar = mysql.connection.cursor()
    curEditar.execute('select * from albums where id=%s', (id,))
    consultaId = curEditar.fetchone()

    return render_template('editar.html', album=consultaId)


@app.route('/actualizar/<id>', methods=['POST'])
def actualizar(id):
    if request.method == 'POST':
        Vtitulo = request.form['txtTitulo']
        Vartista = request.form['txtArtista']
        Vanio = request.form['txtAnio']

        curAct = mysql.connection.cursor()
        curAct.execute('update albums set titulo=%s, artista=%s, anio=%s where id=%s', (Vtitulo, Vartista, Vanio, id))
        mysql.connection.commit()

    flash('Album Actualizado Correctamente')
    return redirect(url_for('index'))


@app.route('/eliminar/<id>')
def eliminar(id):
    curEliminar = mysql.connection.cursor()
    curEliminar.execute('select * from albums where id=%s', (id,))
    consultaId = curEliminar.fetchone()

    return render_template('eliminar.html', album=consultaId)


@app.route('/borrar/<id>', methods=['POST'])
def borrar(id):
    curBorr = mysql.connection.cursor()
    curBorr.execute('delete from albums where id = %s', (id,))
    mysql.connection.commit()

    flash('Album Eliminado Correctamente')
    return redirect(url_for('index'))


# Ejecución de servidor
if __name__ == '__main__':
    app.run(port=3000, debug=True)

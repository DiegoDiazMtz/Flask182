from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


# inicialización del servidor Flask
app = Flask(__name__)
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "DB_Fruteria"

app.secret_key = 'mysecretkey'

mysql = MySQL(app)

# --- Declaración de rutas ---

# Ruta index o ruta principal http://localhost:5000
# La ruta se compone de nombre y función

@app.route('/buscar')
def buscar():
    if request.method == 'POST':
        vbusqueda = request.form['busqueda']

        curBus = mysql.connection.cursor()
        curBus.execute('select * from tbFrutas where nombre=%s', (vbusqueda))
        consulta = curBus.fetchall()
        mysql.connection.commit()
        if consulta == vbusqueda:
            return render_template('menu.html', bus=consulta)
        else:
            flash('No se encontr´ninguna fruta')
            return redirect(url_for('menu'))


@app.route('/')
def menu():
    return render_template('menu.html')


@app.route('/agregar')
def agregar():
    return render_template('agregar.html')


@app.route('/consulta')
def consulta():
    curSelect = mysql.connection.cursor()
    curSelect.execute('select * from tbFrutas')
    consulta = curSelect.fetchall()

    return render_template('consulta.html', listFrutas=consulta)


@app.route('/index')
def index():
    curSelect = mysql.connection.cursor()
    curSelect.execute('select * from tbFrutas')
    consulta = curSelect.fetchall()

    return render_template('index.html', listFrutas=consulta)


@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method == 'POST':
        vfruta = request.form['fruta']
        vtemporada = request.form['temporada']
        vprecio = request.form['precio']
        vstock = request.form['stock']

        CS = mysql.connection.cursor()
        CS.execute('insert into tbFrutas (fruta, temporada, precio, stock) values (%s,%s,%s,%s)',
                   (vfruta, vtemporada, vprecio, vstock))
        mysql.connection.commit()

    flash('Fruta Agregada Correctamente')
    return redirect(url_for('consulta'))


@app.route('/editar/<id>')
def editar(id):
    curEditar = mysql.connection.cursor()
    curEditar.execute('select * from tbFrutas where id=%s', (id,))
    consultaId = curEditar.fetchone()

    return render_template('editar.html', frut=consultaId)


@app.route('/actualizar/<id>', methods=['POST'])
def actualizar(id):
    if request.method == 'POST':
        vfruta = request.form['fruta']
        vtemporada = request.form['temporada']
        vprecio = request.form['precio']
        vstock = request.form['stock']

        curAct = mysql.connection.cursor()
        curAct.execute('update tbFrutas set fruta=%s, temporada=%s, precio=%s, stock=%s where id=%s', (vfruta, vtemporada, vprecio, vstock, id))
        mysql.connection.commit()

    flash('Fruta Actualizada Correctamente')
    return redirect(url_for('index'))


@app.route('/eliminar/<id>')
def eliminar(id):
    curEliminar = mysql.connection.cursor()
    curEliminar.execute('select * from tbFrutas where id=%s', (id,))
    consultaId = curEliminar.fetchone()

    return render_template('eliminar.html', frut=consultaId)


@app.route('/borrar/<id>', methods=['POST'])
def borrar(id):
    curBorr = mysql.connection.cursor()
    curBorr.execute('delete from tbFrutas where id = %s', (id,))
    mysql.connection.commit()

    flash('Fruta Eliminada Correctamente')
    return redirect(url_for('index'))




# Ejecución de servidor
if __name__ == '__main__':
    app.run(port=5000, debug=True)

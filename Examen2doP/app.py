from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


# inicialización del servidor Flask
app = Flask(__name__)
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "DB_Floreria"

app.secret_key = 'mysecretkey'

mysql = MySQL(app)

# --- Declaración de rutas ---

# Ruta index o ruta principal http://localhost:5000
# La ruta se compone de nombre y función

@app.route('/buscar', methods=['POST'])
def buscar():
    if request.method == 'POST':
        busqueda = request.form['busqueda']

        Cbus = mysql.connection.cursor()
        Cbus.execute('select * from tbFlores where nombre=%s', (busqueda,))
        consulta = Cbus.fetchall()
        mysql.connection.commit()

        if consulta:
            return render_template('consulta.html', listaFlores=consulta)
        else:
            flash('No se encontró ninguna fruta')
            return redirect(url_for('consulta'))

    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/agregar')
def agregar():
    return render_template('agregar.html')


@app.route('/consulta')
def consulta():
    return render_template('consulta.html')


@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        Cing = mysql.connection.cursor()
        Cing.execute('insert into tbFlores (nombre, cantidad, precio) values (%s,%s,%s)',(nombre, cantidad, precio))
        mysql.connection.commit()

    flash('Flor Agregada Correctamente')
    return redirect(url_for('agregar'))


@app.route('/editar/<id>')
def editar(id):
    Cedi = mysql.connection.cursor()
    Cedi.execute('select * from tbFlores where id=%s', (id,))
    id_flor = Cedi.fetchone()

    return render_template('editar.html', flor=id_flor)


@app.route('/actualizar/<id>', methods=['POST'])
def actualizar(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        curAct = mysql.connection.cursor()
        curAct.execute('update tbFlores set nombre=%s, cantidad=%s, precio=%s where id=%s', (nombre, cantidad, precio, id))
        mysql.connection.commit()

    flash('Flor Actualizada Correctamente')
    return redirect(url_for('consulta'))


# Ejecución de servidor
if __name__ == '__main__':
    app.run(port=5000, debug=True)

from flask import Flask, request, session, render_template, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__, static_folder='public', template_folder='templates')
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "yourSpace"
app.secret_key = 'mysecretkey'
mysql = MySQL(app)

# -------------------------------------------------------


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/registros')
def registros():
    if request.method == 'POST':
        vusuario = request.form['usuario']
        vnombre = request.form['nombre']
        vap = request.form['ap']
        vam = request.form['ap']
        vpass = request.form['pass']

        CS= mysql.connection.cursor()
        CS.execute('insert into Personas (usuario, nombre, ap, am, pass) values (%s,%s,%s,%s,%s)', (vusuario, vnombre, vap, vam, vpass))
        mysql.connection.commit()

    flash('Usuario creado correctamente')
    return render_template('registros.html')


@app.route('/ingresar', methods=['POST'])
def ingresar():
    if request.method == 'POST':
        vusuario = request.form['usuario']
        vpass = request.form['pass']

        CS= mysql.connection.cursor()
        consulta = 'select usuario from Personas where usuario =%s and pass = %s'
        CS.execute(consulta (vusuario, vpass))
        resultado = CS.fetchone()
        if resultado is not None:
            flash('Usuario o Contraseña incorrecta')
            return render_template('login.html')
        else:
            return render_template('index.html')
        
    return render_template('login.html')


@app.route('/cursos')
def cursos():
    return render_template('cursos.html')


@app.route('/perfil')
def perfil():
    return render_template('perfil.html')


@app.route('/historial')
def historial():
    return render_template('historial.html')


# -------------------------------------------------------

if __name__ == '__main__':
    app.run(port=1000, debug=True)

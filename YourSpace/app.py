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


@app.route('/comprobar', methods=['POST'])
def comprobar():
    if request.method == 'POST':
        vnombreU = request.form['username']
        vpass = request.form['password']

        curC = mysql.connection.cursor()
        curC.execute('select id from usuarios where nombreU=%s and pass =%s', (vnombreU, vpass))
        consulta = curC.fetchone()

        if consulta: 
            return redirect(url_for('index'))
        else: 
            flash('No se encontró el usuario o contraseña')
            return redirect(url_for('login'))


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/registros', methods=['POST'])
def registros():
    if request.method == 'POST':
        vusuario = request.form['usuario']
        vnombre = request.form['nombre']
        vap = request.form['ap']
        vam = request.form['am']
        vpass = request.form['pass']

        curReg = mysql.connection.cursor()
        curReg.execute('insert into personas (nombreP, ap, am) value (%s, %s, %s)', (vnombre, vap, vam))
        mysql.connection.commit()

        curC = mysql.connection.cursor()
        curC.execute('select id from personas where nombreP=%s and ap=%s and am=%s', (vnombre, vap, vam))
        consulta = curC.fetchone()

        curReg = mysql.connection.cursor()
        curReg.execute('insert into usuarios (nombreU, pass, id_persona) value (%s, %s, %s)', (vusuario, vpass, consulta))
        mysql.connection.commit()

    flash('Usuario registrado correctamente')
    return redirect(url_for('login'))


@app.route('/registrarse')
def registrarse():
    return render_template('registros.html')


@app.route('/cursos')
def cursos():
    return render_template('cursos.html')


@app.route('/historial')
def historial():
    return render_template('historial.html')


@app.route('/perfil')
def perfil():
    return render_template('perfil.html')



# -------------------------------------------------------

if __name__ == '__main__':
    app.run(port=1000, debug=True)

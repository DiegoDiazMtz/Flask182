from flask import Flask, request, session, render_template, redirect, url_for, flash
from flask_session import Session
from flask_mysqldb import MySQL

app = Flask(__name__, static_folder='public', template_folder='templates')
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "yourSpace"
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SESSION_TYPE'] = 'filesystem'

mysql = MySQL(app)
Session(app)

# -------------------------------------------------------

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/comprobar', methods=['POST'])
def comprobar():
    if request.method == 'POST':
        usuario = request.form['usuario']
        pas = request.form['pass']

        Clog = mysql.connection.cursor()
        Clog.execute('select id from usuarios where usuario=%s and pass =%s', (usuario, pas))
        id_usuario = Clog.fetchone()

        if id_usuario:
            session['usuario'] = usuario  # Establecer variable de sesión
            return redirect(url_for('index'))
        else:
            flash('No se encontró el usuario o contraseña')
            return redirect(url_for('login'))
        

@app.route('/index')
def index():
    if 'usuario' in session: # Verificar si el usuario está en la sesión

        Csmsae = mysql.connection.cursor()
        Csmsae.execute('select * from vw_info')
        info = Csmsae.fetchall()
        
        return render_template('index.html', cursos=info)
    else:
        return redirect(url_for('login'))
            

@app.route('/registrarse')
def registrarse():
    return render_template('registros.html')


@app.route('/registros', methods=['POST'])
def registros():
    if request.method == 'POST':
        nombre = request.form['nombre']
        ap = request.form['ap']
        am = request.form['am']
        correo = request.form['correo']
        usuario = request.form['usuario']
        pas = request.form['pass']

        Cper = mysql.connection.cursor()
        Cper.execute('insert into personas (nombre, ap, am, correo) value (%s, %s, %s, %s)', (nombre, ap, am, correo))
        mysql.connection.commit()

        Csper = mysql.connection.cursor()
        Csper.execute('select id from personas where nombre=%s and ap=%s and am=%s and correo=%s', (nombre, ap, am, correo))
        consulta = Csper.fetchone()

        Cusu = mysql.connection.cursor()
        Cusu.execute('insert into usuarios (id_persona, usuario, pass) value (%s, %s, %s)', (consulta, usuario, pas))
        mysql.connection.commit()

    flash('Usuario registrado correctamente')
    return redirect(url_for('login'))


@app.route('/cursos')
def cursos():
    if 'usuario' in session:  # Verificar si el usuario está en la sesión
        id_usuario = session['usuario'] 
        return render_template('cursos.html', id_usu=id_usuario)
    else:
        return redirect(url_for('login'))
    

@app.route('/crearcurso', methods=['POST'])
def crearcurso():
    if 'usuario' in session:  
        if request.method == 'POST':

            usuario = session['usuario']
            
            tipo = request.form['tipo']
            materia = request.form['materia']
            descripcion = request.form['descripcion']
            fechaHora = request.form['fechaHora']
            material = request.form['material']
            lugar = request.form['lugar']
            espe = request.form['espe']

            Cper = mysql.connection.cursor()
            Cper.execute('select p.* from personas p join usuarios u on p.id = u.id_persona where u.usuario = %s', (usuario,))
            id_persona = Cper.fetchone()[0]

            Case = mysql.connection.cursor()
            Case.execute('insert into asesores (id_persona) value (%s)', (id_persona,))
            mysql.connection.commit()

            Csase = mysql.connection.cursor()
            Csase.execute('select id from asesores where id_persona=%s', (id_persona,))
            id_asesor = Csase.fetchone()[0]

            Cesp = mysql.connection.cursor()
            Cesp.execute('insert into espe (espe) value (%s)', (espe,))
            mysql.connection.commit()

            Csesp = mysql.connection.cursor()
            Csesp.execute('select id from espe where espe=%s', (espe,))
            id_espe = Csesp.fetchone()[0]

            Cae = mysql.connection.cursor()
            Cae.execute('insert into asesor_espe (id_asesor, id_espe) value (%s,%s)', (id_asesor, id_espe))
            mysql.connection.commit()

            Csae = mysql.connection.cursor()
            Csae.execute('select id from asesor_espe where id_asesor=%s and id_espe=%s', (id_asesor, id_espe,))
            id_asesor_espe = Csae.fetchone()[0]

            Ctip = mysql.connection.cursor()
            Ctip.execute('insert into tipos (tipo) value (%s)', (tipo,))
            mysql.connection.commit()

            Cstipo = mysql.connection.cursor()
            Cstipo.execute('select id from tipos where tipo=%s', (tipo,))
            id_tipo = Cstipo.fetchone()[0]

            Cser = mysql.connection.cursor()
            Cser.execute('insert into servicios (materia, id_tipo, descripcion) value (%s,%s,%s)', (materia, id_tipo, descripcion))
            mysql.connection.commit()

            Csser = mysql.connection.cursor()
            Csser.execute('select id from servicios where materia=%s and id_tipo=%s and descripcion=%s', (materia, id_tipo, descripcion,))
            id_servicio = Csser.fetchone()[0]

            Csae = mysql.connection.cursor()
            Csae.execute('insert into servicio_asesor_espe (id_servicio, id_asesor_espe, fecha, lugar) value (%s,%s,%s,%s)', (id_servicio, id_asesor_espe, fechaHora, lugar))
            mysql.connection.commit()

            Cssae = mysql.connection.cursor()
            Cssae.execute('select id from servicio_asesor_espe where id_servicio=%s and id_asesor_espe=%s and fecha=%s and lugar=%s', (id_servicio, id_asesor_espe, fechaHora, lugar,))
            id_servicio_asesor_espe = Cssae.fetchone()[0]

            Cmsae = mysql.connection.cursor()
            Cmsae.execute('insert into material_servicio_asesor_espe (id_servicio_asesor_espe, material) value (%s,%s)', (id_servicio_asesor_espe, material))
            mysql.connection.commit()

            flash('Curso creado correctamente')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))



@app.route('/historial')
def historial():
    if 'usuario' in session:  # Verificar si el usuario está en la sesión
        return render_template('historial.html')
    else:
        return redirect(url_for('login'))


@app.route('/perfil')
def perfil():
    if 'usuario' in session:  # Verificar si el usuario está en la sesión
        Vusuario = session['usuario']
        
        cper = mysql.connection.cursor()
        cper.execute('select concat(p.nombre," ", p.ap," ", p.am), correo, u.usuario from usuarios u inner join personas p on u.id_persona = p.id where u.usuario = %s', (Vusuario,))
        VdatU = cper.fetchall()
        return render_template('perfil.html', datosp = VdatU)
    else:
        return redirect(url_for('login'))
    

@app.route('/inscribirse')
def inscribirse():
    return


@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.clear()  # Borrar la sesión
    return redirect(url_for('login'))


# -------------------------------------------------------

if __name__ == '__main__':
    app.run(port=1000, debug=True)

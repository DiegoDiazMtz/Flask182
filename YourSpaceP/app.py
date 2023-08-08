from flask import Flask, request, session, render_template, redirect, url_for, flash
from flask_session import Session
from flask_mysqldb import MySQL
from datetime import datetime

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
    if 'usuario' in session:

        Csinfo = mysql.connection.cursor()
        Csinfo.execute('select * from vw_info')
        info = Csinfo.fetchall()

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
        Cper.execute('insert into personas (nombre, ap, am, correo) values (%s, %s, %s, %s)', (nombre, ap, am, correo))
        mysql.connection.commit()

        Csper = mysql.connection.cursor()
        Csper.execute('select id from personas where nombre=%s and ap=%s and am=%s and correo=%s', (nombre, ap, am, correo))
        consulta = Csper.fetchone()

        Cusu = mysql.connection.cursor()
        Cusu.execute('insert into usuarios (id_persona, usuario, pass) values (%s, %s, %s)', (consulta, usuario, pas))
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

            tipo = request.form['tipo'].capitalize()
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
            Case.execute('insert into asesores (id_persona) values (%s)', (id_persona,))
            mysql.connection.commit()

            Csase = mysql.connection.cursor()
            Csase.execute('select id from asesores where id_persona=%s', (id_persona,))
            id_asesor = Csase.fetchone()[0]

            Cesp = mysql.connection.cursor()
            Cesp.execute('insert into espe (espe) values (%s)', (espe,))
            mysql.connection.commit()

            Csesp = mysql.connection.cursor()
            Csesp.execute('select id from espe where espe=%s', (espe,))
            id_espe = Csesp.fetchone()[0]

            Cae = mysql.connection.cursor()
            Cae.execute('insert into asesor_espe (id_asesor, id_espe) values (%s,%s)', (id_asesor, id_espe))
            mysql.connection.commit()

            Csae = mysql.connection.cursor()
            Csae.execute('select id from asesor_espe where id_asesor=%s and id_espe=%s', (id_asesor, id_espe,))
            id_asesor_espe = Csae.fetchone()[0]

            Ctip = mysql.connection.cursor()
            Ctip.execute('insert into tipos (tipo) values (%s)', (tipo,))
            mysql.connection.commit()

            Cstipo = mysql.connection.cursor()
            Cstipo.execute('select id from tipos where tipo=%s', (tipo,))
            id_tipo = Cstipo.fetchone()[0]

            Cser = mysql.connection.cursor()
            Cser.execute('insert into servicios (materia, id_tipo, descripcion) values (%s,%s,%s)', (materia, id_tipo, descripcion))
            mysql.connection.commit()

            Csser = mysql.connection.cursor()
            Csser.execute('select id from servicios where materia=%s and id_tipo=%s and descripcion=%s', (materia, id_tipo, descripcion,))
            id_servicio = Csser.fetchone()[0]

            Csae = mysql.connection.cursor()
            Csae.execute('insert into servicio_asesor_espe (id_servicio, id_asesor_espe, fecha, lugar) values (%s,%s,%s,%s)', (id_servicio, id_asesor_espe, fechaHora, lugar))
            mysql.connection.commit()

            Cssae = mysql.connection.cursor()
            Cssae.execute('select id from servicio_asesor_espe where id_servicio=%s and id_asesor_espe=%s and fecha=%s and lugar=%s', (id_servicio, id_asesor_espe, fechaHora, lugar,))
            id_servicio_asesor_espe = Cssae.fetchone()[0]

            Cmsae = mysql.connection.cursor()
            Cmsae.execute('insert into material_servicio_asesor_espe (id_servicio_asesor_espe, material) values (%s,%s)', (id_servicio_asesor_espe, material))
            mysql.connection.commit()

            flash('Curso creado correctamente')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/cinscrito')
def cinscrito():
    if 'usuario' in session:  # Verificar si el usuario está en la sesión
        usuario = session['usuario']
        
        Cscc = mysql.connection.cursor()
        Cscc.execute('select * from vw_allinfo where usuario_estudiante=%s', (usuario,))
        ccreado = Cscc.fetchall()

        return render_template('cinscrito.html', cc=ccreado)
    else:
        return redirect(url_for('login'))
    

@app.route('/ccreado')
def ccreado():
    if 'usuario' in session:  # Verificar si el usuario está en la sesión
        usuario = session['usuario']
        
        Cscc = mysql.connection.cursor()
        Cscc.execute('select * from vw_info where usuario=%s', (usuario,))
        ccreado = Cscc.fetchall()

        return render_template('ccreado.html', cc=ccreado)
    else:
        return redirect(url_for('login'))


@app.route('/perfil')
def perfil():
    if 'usuario' in session:  # Verificar si el usuario está en la sesión
        usuario = session['usuario']
        
        cper = mysql.connection.cursor()
        cper.execute('select concat(p.nombre," ", p.ap," ", p.am), correo, u.usuario from usuarios u inner join personas p on u.id_persona = p.id where u.usuario = %s', (usuario,))
        datosp = cper.fetchall()

        return render_template('plantilla.html', perf=datosp)
    else:
        return redirect(url_for('login'))
    

@app.route('/inscribirse/<id>')
def inscribirse(id):
    Csins = mysql.connection.cursor()
    Csins.execute('select * from vw_info where id=%s', (id,))
    idsins = Csins.fetchone()

    return render_template('inscribirse.html', idins=idsins)


@app.route('/inscribir/<id>', methods=['POST'])
def inscribir(id):
    if 'usuario' in session:  
        if request.method == 'POST':
            usuario = session['usuario']

            carrera = request.form['carrera']  
            cuatri = int(request.form['cuatri'])
            time = datetime.now()

            Ccar = mysql.connection.cursor()
            Ccar.execute('insert into carreras (carrera) values (%s)', (carrera,))
            mysql.connection.commit()

            Cscar = mysql.connection.cursor()
            Cscar.execute('select id from carreras where carrera=%s', (carrera,))
            id_carrera = Cscar.fetchone()[0]

            Cper = mysql.connection.cursor()
            Cper.execute('select p.* from personas p join usuarios u on p.id = u.id_persona where u.usuario = %s', (usuario,))
            id_persona = Cper.fetchone()[0]

            Cest = mysql.connection.cursor()
            Cest.execute('insert into estudiantes (id_carrera, id_persona, cuatri) values (%s,%s,%s)', (id_carrera, id_persona, cuatri,))
            mysql.connection.commit()

            Csest = mysql.connection.cursor()
            Csest.execute('select id from estudiantes where id_carrera=%s and id_persona=%s and cuatri=%s', (id_carrera, id_persona, cuatri,))
            id_estudiante = Csest.fetchone()[0]

            Cins = mysql.connection.cursor()
            Cins.execute('insert into servicio_estudiante (id_servicio, id_estudiante, fecha) values (%s,%s,%s)', (id, id_estudiante, time,))
            mysql.connection.commit()

            flash('Has sido inscrito correctamente')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/editar/<id>')
def editar(id):
    if 'usuario' in session:  
        curEditar = mysql.connection.cursor()
        curEditar.execute('select * from vw_info where id=%s', (id,))
        consultaId = curEditar.fetchall()[0]

        return render_template('editarc.html', cur=consultaId)
    else:
        return redirect(url_for('login'))


@app.route('/actualizar/<id>', methods=['POST'])
def actualizar(id):
    if 'usuario' in session:
        if request.method == 'POST':
            tipo = request.form['tipo'].capitalize()
            materia = request.form['materia']
            descripcion = request.form['descripcion']
            fechaHora = request.form['fechaHora']
            material = request.form['material']
            lugar = request.form['lugar']
            espe = request.form['espe']

            curActualizar = mysql.connection.cursor()
            curActualizar.execute('update servicios s ' +
                                  'join tipos t on s.id_tipo = t.id ' +
                                  'join servicio_asesor_espe sae on s.id = sae.id_servicio ' +
                                  'join material_servicio_asesor_espe msae on sae.id = msae.id_servicio_asesor_espe ' +
                                  'set t.tipo = %s, s.materia = %s, s.descripcion = %s, sae.fecha = %s, sae.lugar = %s, msae.material = %s ' +
                                  'where s.id = %s',
                                  (tipo, materia, descripcion, fechaHora, lugar, material, id))
            mysql.connection.commit()

            flash('Curso actualizado correctamente')
            return redirect(url_for('ccreado'))
    else:
        return redirect(url_for('login'))

    

@app.route('/eliminar/<id>')
def eliminar(id):
    if 'usuario' in session:  
        curEliminar = mysql.connection.cursor()
        curEliminar.execute('select * from vw_info where id=%s', (id,))
        cursoe = curEliminar.fetchone()

        return render_template('eliminarc.html', ce=cursoe)
    else:
        return redirect(url_for('login'))
    

@app.route('/borrar/<id>', methods=['POST'])
def borrar(id):
    if 'usuario' in session:  
        curBorr = mysql.connection.cursor()
        curBorr.execute('delete from material_servicio_asesor_espe where id=%s', (id,))
        mysql.connection.commit()

        flash('Curso Eliminado Correctamente')
        return redirect(url_for('ccreado'))
    else:
        return redirect(url_for('login'))
    

@app.route('/eliminarins/<id>')
def eliminarins(id):
    if 'usuario' in session:  
        curEliminar = mysql.connection.cursor()
        curEliminar.execute('select * from vw_allinfo where id=%s', (id,))
        cursoe = curEliminar.fetchone()

        return render_template('eliminarins.html', ci=cursoe)
    else:
        return redirect(url_for('login'))
    

'''@app.route('/borrari/<id>', methods=['POST'])
def borrar(id):
    if 'usuario' in session:  
        curBorr = mysql.connection.cursor()
        curBorr.execute('delete from material_servicio_asesor_espe where id=%s', (id,))
        mysql.connection.commit()

        flash('Has sido dado de baja Correctamente')
        return redirect(url_for('cinscrito'))
    else:
        return redirect(url_for('login'))'''


@app.route('/search', methods=['POST'])
def search():
    if 'usuario' in session:  
        if request.method == 'POST':
            busq = request.form['busq']

            Cser = mysql.connection.cursor()
            Cser.execute('select * from vw_info where material=%s or lugar=%s or espe=%s or usuario=%s or correo=%s or tipo=%s or materia=%s or descripcion=%s', (busq,busq,busq,busq,busq,busq,busq,busq,))
            info = Cser.fetchall()

        return render_template('index.html', cursos=info)
    else:
        return redirect(url_for('login'))


@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.clear()  # Borrar la sesión
    return redirect(url_for('login'))


# -------------------------------------------------------

if __name__ == '__main__':
    app.run(port=2000, debug=True)
    
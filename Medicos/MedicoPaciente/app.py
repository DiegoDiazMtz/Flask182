from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask_session import Session
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import blue, black

# Inicialización del servidor Flask
app = Flask(__name__, static_folder='public', template_folder='templates')
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "consultorio"
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SESSION_TYPE'] = 'filesystem'

mysql = MySQL(app)

# -----------------------------------------------------------------------------

@app.route('/')
def login():
    session.clear()
    return render_template('Index.html')

@app.route('/ingresar', methods=['POST'])
def ingresar():
    if request.method == 'POST':
        Vrfc = request.form['rfc']
        pas = request.form['password']
        
        Clog = mysql.connection.cursor()
        Clog.execute('select id from datos_meds where RFC=%s and contraseña =%s', (Vrfc, pas))
        id_usuario = Clog.fetchone()
        
        if id_usuario:
            session['usuario'] = id_usuario  # Establecer variable de sesión
        else:
            flash('No se encontró el usuario o contraseña', 'error')
            return redirect(url_for('login'))
        
        ccargo = mysql.connection.cursor()
        ccargo.execute('select Rol from Datos_meds where RFC = %s and contraseña = %s', (Vrfc, pas))
        rol_usuario = ccargo.fetchone()
        
        if rol_usuario:
            session['rol'] = rol_usuario # Establecer la variable rol del usuario
            print(rol_usuario)
            return redirect(url_for('ConsultaPacientes'))
        else:
            flash('Hubo un error con el rol')
            return redirect(url_for('login'))

@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.clear()  # Borrar la sesión
    return redirect(url_for('login'))

@app.route('/ingresarpaciente', methods=['POST'])
def ingresarpaciente():
    
    if 'usuario' in session:
    
        if request.method=='POST':
            VnombreP= request.form['nombreP']
            VapellidoPP= request.form['apellidoPP']
            VapellidoPM= request.form['apellidoPM']
            VfechaNP= request.form['fechaNP']
            VEnfermedadesP= request.form['EnfermedadesP']
            ValergiasP= request.form['alergiasP']
            VantecedentesP= request.form['antecedentesP']
            idM= session['usuario']
            print(idM)

            CS= mysql.connection.cursor()
            CS.execute('insert into Pacientes (Nombres, ApellidoP, ApellidoM, Fecha_nac) values (%s,%s,%s,%s)', (VnombreP, VapellidoPP, VapellidoPM, VfechaNP))        
            mysql.connection.commit()
            
            CS= mysql.connection.cursor()
            CS.execute('select id from Pacientes where Nombres=%s and ApellidoP=%s and ApellidoM=%s and Fecha_nac=%s',(VnombreP, VapellidoPP, VapellidoPM, VfechaNP))
            idP = CS.fetchone()
            
            CS= mysql.connection.cursor()
            CS.execute('insert into Expedientes (id_paciente, id_medico, Enfermedades_cronicas, Alergias, Antecedentes_familiares) values(%s,%s,%s,%s,%s)', (idP, idM, VEnfermedadesP, ValergiasP, VantecedentesP))
            mysql.connection.commit()


        flash('Paciente Agregado Correctamente')    
        return redirect(url_for('RegPas'))
    
    else:
        return redirect(url_for('login'))

@app.route('/ingresarmedico', methods=['POST'])
def ingresarmedico():
    if 'usuario' in session:
        
        if request.method=='POST':
            Vrfc= request.form['RFC']
            Vnombres= request.form['nombre']
            VapellidoP= request.form['apellidoP']
            VapellidoM= request.form['apellidoM']
            Vrol= request.form['rol']
            VcedulaP= request.form['cedulaP']
            Vcorreo= request.form['correo']
            Vcontraseña = request.form['contraseña']

            CS= mysql.connection.cursor()
            CS.execute('insert into Datos_meds (RFC, nombres, apellidoP, apellidoM, rol, Cedula_prof, Correo, contraseña) values (%s,%s,%s,%s,%s,%s,%s,%s)', (Vrfc, Vnombres, VapellidoP, VapellidoM, Vrol, VcedulaP, Vcorreo, Vcontraseña))        
            mysql.connection.commit()

            flash('Medico Agregado Correctamente')    
            return render_template('AgregarMed.html')
    
    else:
        return redirect(url_for('login'))

@app.route('/RegPas')
def RegPas():
    
    if 'usuario' in session:
        return render_template('RegPas.html')
    else:
        return redirect(url_for('login'))


@app.route('/AgregrarMed')
def AgregrarMed():
    
    if 'usuario' in session:
        return render_template('AgregarMed.html')
    else:
        return redirect(url_for('login'))


@app.route('/IExploYDiagnost/<id>')
def IExploYDiagnost(id):
    
    if 'usuario' in session:
        
        Cexpdiag = mysql.connection.cursor()
        Cexpdiag.execute('SELECT nombres, ApellidoP, ApellidoM FROM Pacientes WHERE id=%s', (id,))
        paciente_data = Cexpdiag.fetchone()

        # Convertir la tupla en una lista y agregar el ID como un nuevo elemento
        paciente_data_list = list(paciente_data)
        paciente_data_list.append(id)

        return render_template('Exploracion.html', nameid = paciente_data_list)
    else:
        return redirect(url_for('login'))
    
@app.route('/GuardarExploracion', methods=['POST'])
def GuardarExploracion():
    if 'usuario' in session:
        if request.method == 'POST':
            Vid_paciente = request.form['id']
            Vpeso = request.form['peso']
            Valtura = request.form['altura']
            Vtemperatura = request.form['temperatura']
            Vlm = request.form['l/m']
            Vso = request.form['so']
            Vglucosa = request.form['glucosa']
            
            Vfecha = datetime.today()
            
            CsaveExplo = mysql.connection.cursor()
            CsaveExplo.execute('INSERT INTO Exploraciones (id_paciente, Fecha, Peso, Altura, Temperatura, Latidos_minuto, Saturacion_oxigeno, Glucosa) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (Vid_paciente, Vfecha, Vpeso, Valtura, Vtemperatura, Vlm, Vso, Vglucosa))
            mysql.connection.commit()
            
            idexplo = CsaveExplo.lastrowid
            idexploracion = int(idexplo)
            
            return render_template('Diagnostico.html', idexp = idexploracion)
    
    else:
        return redirect(url_for('login'))

    

    
    
@app.route('/Diagnostico', methods=['POST'])
def Diagnostico():
    if 'usuario' in session:
        if request.method == 'POST':
            Videxp = request.form['idexploracion']
            Vsintomas = request.form['sintomas']
            Vtratamiento = request.form['tratamiento']
            Vestudios = request.form['estudios']
            
            CDiagnostico = mysql.connection.cursor()
            CDiagnostico.execute('INSERT INTO Diagnosticos (id_exploracion, Sintomas, Tratamiento, Estudios) VALUES (%s, %s, %s, %s)', (Videxp, Vsintomas, Vtratamiento, Vestudios))
            mysql.connection.commit()
            
            VidDiag = CDiagnostico.lastrowid
            idDiag = int(VidDiag)
            
            Crecetas = mysql.connection.cursor()
            Crecetas.execute('insert into recetas (id_exploracion, id_diagnostico) values(%s,%s)', (Videxp, idDiag))
            mysql.connection.commit()
            
            flash('Se guardaron correctamente los datos', 'success')
            return redirect(url_for('consultarRecetas'))
            
    else:
        return redirect(url_for('login'))



@app.route('/ConsultaPacientes')
def ConsultaPacientes():
    
    if 'usuario' in session:
        return render_template('ConsultaPacientes.html')
    else:
        return redirect(url_for('login'))


@app.route('/consultarRecetas')
def consultarRecetas():
    
    if 'usuario' in session:
        return render_template('consultarRecetas.html') 
    else:
        return redirect(url_for('login'))
    
@app.route('/receta', methods=['POST'])
def receta():
    if 'usuario' in session:
        if request.method == 'POST':
            Vnombre = request.form.get('nombre', '').strip()
            Vfecha = request.form.get('fecha', '').strip()
            Vnombre = f"%{Vnombre}%"

            if not Vnombre and not Vfecha:
                
                flash('ingrese al menos un criterio de busqueda')
                return redirect(url_for('consultarRecetas'))

            # Construir la consulta base
            consulta = "SELECT CONCAT(pac.Nombres, ' ', pac.ApellidoP, ' ', pac.ApellidoM) AS nombreCom, expl.fecha, expl.Peso, expl.Altura, expl.Temperatura, expl.Latidos_minuto, expl.Saturacion_oxigeno, Glucosa, diag.sintomas, diag.tratamiento, diag.estudios, dat.Nombres, dat.ApellidoP, dat.ApellidoM, re.id FROM Recetas re INNER JOIN Exploraciones expl ON re.id_exploracion = expl.id INNER JOIN Diagnosticos diag ON re.id_diagnostico = diag.id INNER JOIN Expedientes expe ON expl.id_paciente = expe.id_paciente INNER JOIN Pacientes pac ON expe.id_paciente = pac.id INNER JOIN datos_meds dat ON dat.id = expe.id_medico where"

            if Vfecha and Vnombre:
                consulta += " pac.nombres LIKE %s OR pac.apellidoP LIKE %s OR pac.apellidoM LIKE %s and  date(expl.fecha) = %s"
                parametros = (Vnombre, Vnombre, Vnombre, Vfecha)

            elif Vfecha:
                consulta += " date(expl.fecha) = %s"
                parametros = (Vfecha,)
                
            elif Vnombre:
                consulta += " pac.nombres LIKE %s OR pac.apellidoP LIKE %s OR pac.apellidoM LIKE %s"
                parametros = (Vnombre, Vnombre, Vnombre)
            
            Creceta = mysql.connection.cursor()
            Creceta.execute(consulta, parametros)
            datos_receta = Creceta.fetchall()

            if datos_receta:
                return render_template('consultarRecetas.html', datos=datos_receta)
            else:
                flash('No se encontraron resultados')
                return render_template('consultarRecetas.html')

    else:
        return redirect(url_for('login'))

@app.route('/imprimirReceta/<id>')
def imprimirReceta(id):
    if 'usuario' in session:
        id = int(id)
        CimpRec = mysql.connection.cursor()
        CimpRec.execute("SELECT concat(dat.Nombres, ' ',dat.ApellidoP, ' ', dat.ApellidoM) as nombreDoc, CONCAT(pac.Nombres, ' ', pac.ApellidoP, ' ', pac.ApellidoM) AS nombreCom, expl.fecha, expl.Peso, expl.Altura, expl.Temperatura, expl.Latidos_minuto, expl.Saturacion_oxigeno, Glucosa, diag.sintomas, diag.tratamiento, diag.estudios FROM Recetas re INNER JOIN Exploraciones expl ON re.id_exploracion = expl.id INNER JOIN Diagnosticos diag ON re.id_diagnostico = diag.id INNER JOIN Expedientes expe ON expl.id_paciente = expe.id_paciente INNER JOIN Pacientes pac ON expe.id_paciente = pac.id INNER JOIN datos_meds dat ON dat.id = expe.id_medico where re.id =%s", (id,))
        datosReceta = CimpRec.fetchone()
    
        c = canvas.Canvas(f"Receta-{datosReceta[1]}.pdf", pagesize=letter)
        
        page_width, page_height = letter
        margin = 50  # 1 pulgada en puntos (72 puntos por pulgada)
        margin_cm = 28.3465  # 1 centímetro en puntos (28.3465 puntos por centímetro)

        # Definir dimensiones del cuadro
        box_width = page_width - 2 * margin  # Ancho completo de la página
        box_height = (page_height - 2 * margin) / 2  # Mitad del alto de la página

        # Definir posición para el texto dentro del cuadro
        x_position = margin + 10  # 10 puntos desde la izquierda
        y_position = page_height - margin - 10  # 10 puntos desde arriba

         # Dibujar la imagen de fondo dentro del cuadro
        image_path = "C:/laragon/www/CENTROMEDICO2.0/MedicoPaciente/public/images/R.jpg"
        img_width = box_width  # Ajustar el ancho de la imagen para que encaje en el cuadro
        img_height = box_height  # Ajustar el alto de la imagen para que encaje en el cuadro
        c.drawImage(image_path, margin, page_height - margin - box_height, width=img_width, height=img_height)

        listaDatosReceta = list(datosReceta)
        listaDatosReceta = [str(item) for item in listaDatosReceta]
        
        color = black

        # Ajustar posición y formato del primer dato
        first_dato = listaDatosReceta[0]
        c.setFont('Helvetica-Bold', 13)  # Fuente en negritas y tamaño 16
        c.setFillColor(color)  # Color azul
        c.drawString(154, y_position - 35 , first_dato)  # Ajustar la posición X para centrar
        
        # Ajustar posición y formato del primer dato
        second_dato = listaDatosReceta[1]
        c.setFont('Helvetica', 12)  # Restablecer la fuente a tamaño 12
        c.setFillColor(color)  # Color azul
        c.drawString(146, y_position - 96 , second_dato)  # Ajustar la posición X para centrar
        
        # Ajustar posición y formato del primer dato
        second_dato = listaDatosReceta[2]
        c.setFillColor(color)  # Color azul
        c.drawString(400, y_position - 116 , second_dato)  # Ajustar la posición X para centrar
        
        # Ajustar posición y formato del primer dato
        second_dato = listaDatosReceta[3]
        c.setFillColor(color)  # Color azul
        c.drawString(202, y_position - 121 , second_dato)  # Ajustar la posición X para centrar
        
        # Ajustar posición y formato del primer dato
        second_dato = listaDatosReceta[4]
        c.setFillColor(color)  # Color azul
        c.drawString(123, y_position - 121 , second_dato)  # Ajustar la posición X para centrar
        
        # Ajustar posición y formato del primer dato
        second_dato = listaDatosReceta[5]
        c.setFillColor(color)  # Color azul
        c.drawString(460, y_position - 96 , second_dato)  # Ajustar la posición X para centrar
        
        second_dato = listaDatosReceta[9]
        c.setFillColor(color)  # Color azul
        c.drawString(190, y_position - 154 , second_dato)  # Ajustar la posición X para centrar
        
        second_dato = listaDatosReceta[10]
        c.setFillColor(color)  # Color azul
        c.drawString(190, y_position - 208 , second_dato)  # Ajustar la posición X para centrar



        # Agregar el resto de los datos
        """for dato in listaDatosReceta[6:]:
            c.setFont('Helvetica', 12)  # Restablecer la fuente a tamaño 12
            c.setFillColor(blue)  # Cambiar el color de nuevo a negro
            c.drawString(100, y_position, dato)
            y_position -= 20 """

        # Guardar el contenido y cerrar el archivo PDF
        c.save()
            
        return redirect(url_for('consultarRecetas'))

        
    else:
        return redirect(url_for('login'))


@app.route('/ListaDr')
def ListaDr():
    if 'usuario' in session:
        cLisDoc = mysql.connection.cursor()
        cLisDoc.execute('select id, RFC, nombres, apellidoP, apellidoM, Cedula_prof, Correo, Rol from datos_meds')
        datosmeds = cLisDoc.fetchall()
        
        return render_template('ListaDr.html', result = datosmeds)
    else:
        return redirect(url_for('login'))


@app.route('/BuscarDoctor', methods=['POST'])
def BuscarDoctor():
    if 'usuario' in session:
        if request.method=='POST':
            VnombreDoc = request.form['NombreDoc']
            
            CBusDoc = mysql.connection.cursor()
            patron_busqueda = f"%{VnombreDoc}%"
            consulta_sql = f"select id, RFC, nombres, apellidoP, apellidoM, Cedula_prof, Correo, Rol from datos_meds where nombres like '{patron_busqueda}' or apellidoP like '{patron_busqueda}' or apellidoM like '{patron_busqueda}';"
            CBusDoc.execute(consulta_sql)
        
            resultados = CBusDoc.fetchall()
            if resultados:
                return render_template('ListaDr.html', result = resultados)
            else:
                flash('No se encotraron resultados')
                return render_template('ListaDr.html')
    else:
        return redirect(url_for('login'))
    
@app.route('/actualizarDatosDocForm',  methods=['POST']) 
def actualizarDatosDocForm():
    if 'usuario' in session:
        if request.method=='POST':
            Vid = request.form['doctor_id']
            
            cactDatDoc = mysql.connection.cursor()
            cactDatDoc.execute('Select * from datos_meds where id = %s', (Vid,))
            datosDoc = cactDatDoc.fetchone()
            
            return render_template('ActualizarDatosDoc.html', medico = datosDoc)
        
    else:
        return redirect(url_for('login'))


@app.route('/actualizarDatosDoc', methods=['POST'])
def actualizarDatosDoc():
    if 'usuario' in session:
        
        if request.method=='POST':
            
            Vid= request.form['id']
            Vrfc= request.form['RFC']
            Vnombres= request.form['nombre']
            VapellidoP= request.form['apellidoP']
            VapellidoM= request.form['apellidoM']
            Vrol= request.form['rol']
            VcedulaP= request.form['cedulaP']
            Vcorreo= request.form['correo']
            Vcontraseña = request.form['contraseña']

            CS= mysql.connection.cursor()
            CS.execute('update Datos_meds set RFC=%s , nombres=%s, apellidoP=%s, apellidoM=%s, rol=%s, Cedula_prof=%s, Correo=%s, contraseña=%s where id =%s', (Vrfc, Vnombres, VapellidoP, VapellidoM, Vrol, VcedulaP, Vcorreo, Vcontraseña, Vid))        
            mysql.connection.commit()

            flash('Se han actualizado los datos correctamente')    
            return redirect(url_for('ListaDr'))
    
    else:
        return redirect(url_for('login'))


@app.route('/confirmarEliminar' , methods=['POST'])
def confirmarEliminar():
    if 'usuario' in session:
        if request.method == 'POST':
            Vid = request.form['doctor_id']
            return redirect(url_for('eliminarDoctor', doctor_id=Vid))
        else:
            flash('¿!!!Esta seguro que desea eliminar!!!?')
    else:
        return redirect(url_for('login'))

@app.route('/eliminarDoctor',  methods=['POST'])
def eliminarDoctor():
    if 'usuario' in session:
        if request.method == 'POST':
            Vid = request.form['doctor_id']
            
            CEliminarDoc = mysql.connection.cursor()
            CEliminarDoc.execute('DELETE FROM datos_meds WHERE id = %s', (Vid,))
            mysql.connection.commit()
            
            flash('Se eliminaron los datos del doctor correctamente!!')
            return redirect(url_for('ListaDr'))
    else:
        return redirect(url_for('login'))
    

@app.route('/buscarPaciente', methods=['POST'])
def buscarPaciente():
    if 'usuario' in session:
        if request.method == 'POST':
            VnombM = request.form['NombMe']
            VnombP = request.form['NombPa']

            # Verificar si se proporciona un criterio de búsqueda válido
            if not VnombM.strip() and not VnombP.strip():
                flash('Ingrese al menos un criterio de búsqueda')
                return render_template('ConsultaPacientes.html')

            VnombMBus = f"%{VnombM}%" if VnombM.strip() else None
            VnombPBus = f"%{VnombP}%" if VnombP.strip() else None

            # Modificar la consulta para aplicar el filtrado solo si se proporcionan valores válidos
            consulta = "SELECT pac.id, CONCAT(pac.Nombres, ' ', pac.ApellidoP, ' ', pac.ApellidoM) AS Nombre_pac, pac.Fecha_nac, expe.Enfermedades_cronicas, expe.Alergias, expe.Antecedentes_familiares, concat(datmed.nombres,' ', datmed.apellidoP, ' ', datmed.apellidoM) as Nombre_med FROM Pacientes pac INNER JOIN Expedientes expe ON pac.id = expe.id_paciente INNER JOIN Datos_meds datmed ON expe.id_medico = datmed.id WHERE"

            condiciones = []
            parametros = []

            if VnombPBus:
                condiciones.append("(pac.Nombres LIKE %s OR pac.ApellidoP LIKE %s OR pac.ApellidoM LIKE %s)")
                parametros.extend([VnombPBus, VnombPBus, VnombPBus])

            if VnombMBus:
                condiciones.append("(datmed.Nombres LIKE %s OR datmed.ApellidoP LIKE %s OR datmed.ApellidoM LIKE %s)")
                parametros.extend([VnombMBus, VnombMBus, VnombMBus])

            if condiciones:
                consulta += " " + "AND".join(condiciones)

            consulta += " GROUP BY pac.id;"

            Cbuspa = mysql.connection.cursor()
            Cbuspa.execute(consulta, parametros)
            datosConsulta = Cbuspa.fetchall()

            if datosConsulta:
                return render_template('ConsultaPacientes.html', pacientes_data=datosConsulta)
            else:
                flash('No se encontraron resultados')
                return render_template('ConsultaPacientes.html')

    else:
        return redirect(url_for('login'))




        


# -----------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(port=4000, debug=True)


from flask import Flask, request, session, render_template, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__, static_folder='public', template_folder='templates')
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "yourSpace"

app.secret_key = 'mysecretkey'

mysql = MySQL(app)

#-------------------------------------------------------

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/ingresar', methods=['POST'])
def ingresar():
    if request.method == 'POST':
        Vusername = request.form['username']
        Vpassword = request.form['password']
        Vrol = request.form['rol']

    usu = {
        'diego_d': '1234',
        'maya_g': '4321'
    }

    if Vusername in usu and usu[Vusername] == Vpassword:
        session['username'] = Vusername
        if Vusername == 'diego_d':
            if Vrol == 'student':
                return redirect(url_for('indexS'))
            else: 
                return redirect(url_for('indexT'))
        elif Vusername == Vusername:
            if Vrol == 'student':
                return redirect(url_for('indexS'))
            else: 
                return redirect(url_for('indexT'))
    else:
        flash('Usuario o contraseña incorrectos')

    return redirect(url_for('login'))

@app.route('/indexS')
def indexS():
    return render_template('indexS.html')

@app.route('/indexT')
def indexT():
    return render_template('indexT.html')

#-------------------------------------------------------

if __name__ == '__main__':
    app.run(port=1000, debug=True)


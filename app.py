from flask import Flask, render_template, redirect, request, Response, session, url_for
from flask_mysqldb import MySQL, MySQLdb
from config import config

app = Flask(__name__,template_folder='templates')
app.static_folder = 'static'

app.config['MYSQL_HOST']='database-1.ctq4miuy6qln.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER']='admin'
app.config['MYSQL_PASSWORD']='password'#borrar contraseña si la utiliza Jose Pillo
app.config['MYSQL_DB']='greenhouse'
app.config['MYSQL_CURORCLASS']='DictCursor'
mysql=MySQL(app)

@app.route('/')
def infor():
    return render_template('infor.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/home')
def control():
    return render_template('home.html')

@app.route('/temperatura')
def temperatura():
    return render_template('temperatura.html')

@app.route('/iluminacion')
def iluminacion():
    return render_template('iluminacion.html')

@app.route('/humedad')
def humedad():
    return render_template('humedad.html')

@app.route('/recuperar')
def recuperar():
    return render_template('recuperar.html')

#login...............................
@app.route('/login', methods=["GET", "POST"])
def login():

    if request.method == 'POST' and 'txtUsername' in request.form and 'txtPassword' in request.form:
        _username = request.form['txtUsername']
        _password = request.form['txtPassword']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE Username = %s AND Password = %s', (_username, _password,))
        account = cur.fetchone()

        if account:
            session['logueado'] = True
            session['id'] = account[0]

            return render_template("home.html")
        else:
            return render_template('index.html', mensaje="Usuario o contraseña incorrecto")
    else:
        return render_template('index.html')
#---------------------------------------------------
@app.route('/acerca_de_nosotros')
def acerca_de_nosotros():
    return render_template('acerca_de_nosotros.html')

#@app.route('/login')
#def login():
#    return render_template('auth/login.html')

#registro....
@app.route('/sign')
def sign():
    return render_template('auth/sign.html')

@app.route('/sign-registro', methods=["GET", "POST"])
def sign_registro():


    email=request.form['txtEmail']
    password=request.form['txtPassword']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (email,password,id_rol) Values (%s, %s, '1')",(email,password))
    mysql.connection.commit()

    return render_template("auth/login.html",mensaje2="Usuario registrado exitosamente")

#--------------------------------------------
if __name__== '__main__':
    app.secret_key="jose_el_pillo"

    app.run(debug=True,port=5000, threaded=True)
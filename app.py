from flask import Flask, render_template, redirect, request, Response, session, url_for, make_response
from flask_mysqldb import MySQL, MySQLdb
from config import config
import mysql.connector
import pdfkit
from humedad import consultar_ultimos_registros  
from temperatura import consultar_ultimos_registros  

app = Flask(__name__,template_folder='templates')
app.static_folder = 'static'

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''#borrar contraseña si la utiliza Jose Pillo
app.config['MYSQL_DB']='PI'
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
    ids, temperatura, fecha = consultar_ultimos_registros()

    if ids is None or temperatura is None:
        return 'Error al obtener los datos de la base de datos'

    return render_template('temperatura.html', ids=ids, temperatura=temperatura, fecha=fecha)


@app.route('/iluminacion')
def iluminacion():
    return render_template('iluminacion.html')

@app.route('/humedad')
def humedad():
    ids, humedades, fecha = consultar_ultimos_registros()

    if ids is None or humedades is None:
        return 'Error al obtener los datos de la base de datos'

    return render_template('humedad.html', ids=ids, humedades=humedades, fecha=fecha)



@app.route('/recuperar')
def recuperar():
    return render_template('recuperar.html')

#--------------------------------------------

path_to_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
options = {
    'no-outline': None,
    'disable-smart-shrinking': None,
    'no-stop-slow-scripts': None,
    'enable-local-file-access': None,
}

@app.route('/download_report')
def download_report():
    rendered = render_template('reporte.html')
    pdf = pdfkit.from_string(rendered, False, configuration=config, options=options)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'
    return response

#--------------------------------------------

#login...............................
@app.route('/login', methods=["GET", "POST"])
def login():

    if request.method == 'POST' and 'txtEmail' in request.form and 'txtPassword' in request.form:
        _email = request.form['txtEmail']
        _password = request.form['txtPassword']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE email = %s AND password = %s', (_email, _password,))
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


#--------------------------------------------------------------




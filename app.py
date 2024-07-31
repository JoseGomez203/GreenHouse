from flask import Flask, jsonify, render_template, redirect, request, Response, session, url_for, make_response
from flask_mysqldb import MySQL, MySQLdb
from config import config
import mysql.connector
import pdfkit
from humedad import consultar_ultimos_registros  
from temperatura import consultar_ultimos_registros  
from werkzeug.security import check_password_hash
from datetime import datetime

app = Flask(__name__, template_folder='templates')
app.static_folder = 'static'

app.config['MYSQL_HOST'] = 'database-1.ctq4miuy6qln.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'greenhouse'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def infor():
    return render_template('index.html')

@app.route('/sensor-data', methods=['POST'])
def receive_data():
    try:
        data = request.get_data(as_text=True)
        print(f'Datos recibidos: {data}')
        
        datos = data.split(', ')
        sensor_data = {}
        for d in datos:
            key, value = d.split(': ')
            sensor_data[key.strip()] = float(value.strip())
        
        humedad_tierra = sensor_data.get('HumedadTierra', None)
        iluminacion = sensor_data.get('Luz', None)
        humedad_ambiente = sensor_data.get('HumedadAmbiente', None)
        temperatura = sensor_data.get('Temp', None)
        
        if None in (humedad_tierra, iluminacion, humedad_ambiente, temperatura):
            raise ValueError("Faltan datos en la entrada recibida")

        fecha = datetime.now()
        IDCultivo = 1
        
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO lectura (IDCultivo, Temperatura, Humedad, Iluminacion, Fecha, Humedad_Tierra) VALUES (%s, %s, %s, %s, %s, %s)",
            (IDCultivo, temperatura, humedad_ambiente, iluminacion, fecha, humedad_tierra)
        )
        mysql.connection.commit()
        cur.close()
        
        return 'Datos recibidos y almacenados en la base de datos', 200
    except Exception as e:
        print(f'Error al recibir datos: {e}')
        return 'Error en la solicitud', 400

@app.route('/')
def index():
    return render_template('index.html')

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
    if request.method == 'POST' and 'Username' in request.form and 'txtPassword' in request.form:
        _Username = request.form['Username']
        _password = request.form['txtPassword']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE Username = %s AND Password = %s', (_Username, _password,))
        account = cur.fetchone()

        if account:
            session['logueado'] = True
            session['id'] = account['IDUsuarios']  # Asumiendo que 'ID' es la columna con el identificador del usuario en la tabla 'usuarios'
            return render_template("home.html")
        else:
            return render_template('auth/login.html', mensaje="Usuario o contraseña incorrecto")
    else:
        return render_template('auth/login.html')


@app.route('/home')
def home():
    if 'logueado' in session:
        return render_template("home.html")
    return redirect(url_for('home.html'))

#---------------------------------------------------
@app.route('/acerca_de_nosotros')
def acerca_de_nosotros():
    return render_template('acerca_de_nosotros.html')

#registro....
@app.route('/sign')
def sign():
    return render_template('auth/sign.html')

@app.route('/sign-registro', methods=["GET", "POST"])
def sign_registro():
    email = request.form['txtEmail']
    password = request.form['txtPassword']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (email,password,id_rol) Values (%s, %s, '1')", (email, password))
    mysql.connection.commit()

    return render_template("auth/login.html", mensaje2="Usuario registrado exitosamente")

#--------------------------------------------
if __name__ == '__main__':
    app.secret_key = "jose_el_pillo"
    app.run(host='0.0.0.0', port=8080, debug=True)

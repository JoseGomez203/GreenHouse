from flask import Flask, jsonify, render_template, redirect, request, Response, session, url_for, make_response
from flask_mysqldb import MySQL, MySQLdb
from config import config
import mysql.connector
import pdfkit
from humedad import consultar_ultimos_registros  
from temperatura import consultar_ultimos_registros
from iluminacion import consultar_ultimos_registros    
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
    return render_template('Auth/login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'logueado' in session:
        cur = mysql.connection.cursor()
        
        if request.method == 'POST':
            cultivo_id = request.form.get('cultivo_id')
            if cultivo_id:
                cur.execute("SELECT * FROM cultivo WHERE IDCultivo = %s AND IDUsuarios = %s", (cultivo_id, session['id']))
            else:
                cur.execute("SELECT * FROM cultivo WHERE IDUsuarios = %s", (session['id'],))
        else:
            cultivo_id = request.args.get('cultivo_id')
            if cultivo_id:
                cur.execute("SELECT * FROM cultivo WHERE IDCultivo = %s AND IDUsuarios = %s", (cultivo_id, session['id']))
            else:
                cur.execute("SELECT * FROM cultivo WHERE IDUsuarios = %s", (session['id'],))
        
        cultivos = cur.fetchall()
        cur.close()
        
        if cultivos:
            # Asumimos que tomamos el primer cultivo para mostrar si no se seleccionó ninguno
            cultivo = cultivos[0]
            
            # Obtén cultivos relacionados (mismos usuarios pero diferentes IDs)
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM cultivo WHERE IDUsuarios = %s AND IDCultivo != %s", (session['id'], cultivo['IDCultivo']))
            related_cultivos = cur.fetchall()
            cur.close()

            # Depuración
            print(f'Related Cultivos: {related_cultivos}')
            
            return render_template("home.html", cultivo=cultivo, related_cultivos=related_cultivos)
        else:
            return 'No hay cultivos registrados para este usuario'
    return redirect(url_for('login'))



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

@app.route('/temperatura')
def temperatura():
    ids, temperatura, fecha = consultar_ultimos_registros()

    if ids is None or temperatura is None:
        return 'Error al obtener los datos de la base de datos'

    return render_template('temperatura.html', ids=ids, temperatura=temperatura, fecha=fecha)

@app.route('/iluminacion')
def iluminacion():
    ids, iluminacion, fecha = consultar_ultimos_registros()

    if ids is None or iluminacion is None:
        return 'Error al obtener los datos de la base de datos'

    return render_template('iluminacion.html', ids=ids, iluminacion=iluminacion, fecha=fecha)

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
            session['id'] = account['IDUsuarios']
            return redirect(url_for('home'))
        else:
            return render_template('auth/login.html', mensaje="Usuario o contraseña incorrecto")
    else:
        return render_template('auth/login.html')
    
@app.route('/logout')
def logout():
    # Limpia la sesión del usuario
    session.clear()
    return redirect(url_for('login'))


#---------------------------------------------------
@app.route('/acerca_de_nosotros')
def acerca_de_nosotros():
    return render_template('acerca_de_nosotros.html')

#Cultivos CRUD


@app.route('/cultivos')
def lista_cultivos():
    if 'logueado' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM cultivo WHERE IDUsuarios = %s", (session['id'],))
        cultivos = cur.fetchall()
        cur.close()
        return render_template('cultivos.html', cultivos=cultivos)
    return redirect(url_for('login'))



@app.route('/cultivo/agregar', methods=['GET', 'POST'])
def add_cultivo():
    if 'logueado' in session:
        if request.method == 'POST':
            nombre = request.form['nombre']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO cultivo (Nombre_Cultivo, IDUsuarios) VALUES (%s, %s)", (nombre, session['id']))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('lista_cultivos'))
        return render_template('agregar_cultivo.html')
    return redirect(url_for('login'))

@app.route('/cultivo/editar/<int:cultivo_id>', methods=['GET', 'POST'])
def editar_cultivo(cultivo_id):
    if 'logueado' in session:
        cur = mysql.connection.cursor()
        if request.method == 'POST':
            nombre = request.form['nombre']
            cur.execute("UPDATE cultivo SET Nombre_Cultivo = %s WHERE IDCultivo = %s AND IDUsuarios = %s", (nombre, cultivo_id, session['id']))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('lista_cultivos'))
        cur.execute("SELECT * FROM cultivo WHERE IDCultivo = %s AND IDUsuarios = %s", (cultivo_id, session['id']))
        cultivo = cur.fetchone()
        cur.close()
        return render_template('editar_cultivo.html', cultivo=cultivo)
    return redirect(url_for('login'))


@app.route('/cultivo/borrar/<int:cultivo_id>')
def borrar_cultivo(cultivo_id):
    if 'logueado' in session:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM cultivo WHERE IDCultivo = %s AND IDUsuarios = %s", (cultivo_id, session['id']))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('lista_cultivos'))
    return redirect(url_for('login'))



#--------------------------------------------



if __name__ == '__main__':
    app.secret_key = "jose_el_pillo"
    app.run(host='0.0.0.0', port=8080, debug=True)

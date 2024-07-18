from flask import Flask, render_template, redirect, request, Response, session, url_for, make_response
from flask_mysqldb import MySQL, MySQLdb
import pdfkit
import mysql.connector
from flask import Flask
app = Flask(__name__)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#MODULO TEMPERATURA// DESAROLLADOR ALMA ANGELICA DURAN HENRANDEZ 
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
def consultar_ultimos_registros():
    try:
        # Conectar a la base de datos
        conn = mysql.connector.connect(
            host='database-1.ctq4miuy6qln.us-east-1.rds.amazonaws.com',
            user='admin',
            password='password',
            database='greenhouse'
        )
        
        if conn.is_connected():
            print('Conexión exitosa a la base de datos')
        else:
            print('No se pudo conectar a la base de datos')

        cursor = conn.cursor()

        
        cursor.execute("SHOW TABLES LIKE 'lectura'")
        table_exists = cursor.fetchone()

        if not table_exists:
            print('La tabla "lectura" no existe en la base de datos')

       
        cursor.execute("SELECT IDLectura, Temperatura, Fecha FROM lectura ORDER BY IDLectura DESC LIMIT 5")
        registros = cursor.fetchall()

        
        cursor.close()
        conn.close()

        
        ids = [registro[0] for registro in registros]
        temperaturas = [registro[1] for registro in registros]
        fecha = [registro[2] for registro in registros]

        return ids, temperaturas, fecha

    except mysql.connector.Error as e:
        print(f'Error al conectar a la base de datos: {e}')
        return None, None

@app.route('/temperatura')
def temperatura():
    ids, temperatura, fecha = consultar_ultimos_registros()

    if ids is None or temperatura is None:
        return 'Error al obtener los datos de la base de datos'

    return render_template('temperatura', ids=ids, temperatura=temperatura, fecha=fecha)

if __name__ == '__main__':
    app.run(debug=True)



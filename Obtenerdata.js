const express = require('express');
const cors = require('cors');
const mysql = require('mysql');

const app = express();
app.use(cors());

const db = mysql.createConnection({
  host: 'database-1.ctq4miuy6qln.us-east-1.rds.amazonaws.com',
  user: 'admin',
  password: 'password',
  database: 'greenhouse'
});

db.connect((err) => {
  if (err) throw err;
  console.log('Conectado a la base de datos');
});

app.get('/api/humedad', (req, res) => {
  const query = `
    SELECT fecha, AVG(Humedad) AS promedio
    FROM lectura
    GROUP BY fecha
    ORDER BY fecha DESC
    LIMIT 5;
  `;
  db.query(query, (err, results) => {
    if (err) throw err;
    res.json(results);
  });
});

app.get('/api/iluminacion', (req, res) => {
  const query = `
    SELECT fecha, AVG(Iluminacion) AS promedio
    FROM lectura
    GROUP BY fecha
    ORDER BY fecha DESC
    LIMIT 5;
  `;
  db.query(query, (err, results) => {
    if (err) throw err;
    res.json(results);
  });
});

app.get('/api/humedad-suelo', (req, res) => {
  const query = `
    SELECT fecha, AVG(Temperatura) AS promedio
    FROM lectura
    GROUP BY fecha
    ORDER BY fecha DESC
    LIMIT 5;
  `;
  db.query(query, (err, results) => {
    if (err) throw err;
    res.json(results);
  });
});

app.listen(3000, () => {
  console.log('Servidor corriendo en el puerto 3000');
});

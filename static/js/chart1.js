document.addEventListener('DOMContentLoaded', (event) => {
  if (document.getElementById('myChart')) {
    fetchHumedadData();
  } else if (document.getElementById('Chart1')) {
    fetchIluminacionData();
  } else if (document.getElementById('Chart2')) {
    fetchHumedadSueloData();
  }
});

async function fetchHumedadData() {
  try {
    const response = await fetch('http://localhost:3000/api/humedad');
    const data = await response.json();

    const labels = data.map((_, index) => `Smn ${index + 1}`);
    const humidities = data.map(item => item.promedio);

    const ctx = document.getElementById('myChart').getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Humedad Promedio (%)',
          data: humidities,
          borderColor: 'green',    // Color de la línea
          borderWidth: 3,           // Grosor de la línea
          
          fill: true                // Relleno bajo la línea
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: false,
            ticks: {
              color: 'white',        // Color de las etiquetas en el eje Y
              font: {
                size: 14            // Tamaño de fuente de las etiquetas en el eje Y
              }
            }
          },
          x: {
            ticks: {
              color: 'white',        // Color de las etiquetas en el eje X
              font: {
                size: 14            // Tamaño de fuente de las etiquetas en el eje X
              }
            }
          }
        },
        plugins: {
          legend: {
            labels: {
              color: 'white',        // Color de las etiquetas de la leyenda
              font: {
                size: 18            // Tamaño de fuente de las etiquetas de la leyenda
              }
            }
          }
        }
      }
    });
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}

async function fetchIluminacionData() {
  try {
    const response = await fetch('http://localhost:3000/api/iluminacion');
    const data = await response.json();

    const labels = data.map((_, index) => `Smn ${index + 1}`);
    const iluminacion = data.map(item => item.promedio);

    const ctx = document.getElementById('Chart1').getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Iluminación Promedio (lux)',
          data: iluminacion,
          borderColor: 'green',    // Color de la línea
          
          borderWidth: 3,           // Grosor de la línea
          
          fill: true                // Relleno bajo la línea
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: false,
            ticks: {
              color: 'white',        // Color de las etiquetas en el eje Y
              font: {
                size: 14            // Tamaño de fuente de las etiquetas en el eje Y
              }
            }
          },
          x: {
            ticks: {
              color: 'white',        // Color de las etiquetas en el eje X
              font: {
                size: 14            // Tamaño de fuente de las etiquetas en el eje X
              }
            }
          }
        },
        plugins: {
          legend: {
            labels: {
              color: 'white',        // Color de las etiquetas de la leyenda
              font: {
                size: 18            // Tamaño de fuente de las etiquetas de la leyenda
              }
            }
          }
        }
      }
    });
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}

async function fetchHumedadSueloData() {
  try {
    const response = await fetch('http://localhost:3000/api/humedad-suelo');
    const data = await response.json();

    const labels = data.map((_, index) => `Smn ${index + 1}`);
    const humedadSuelo = data.map(item => item.promedio);

    const ctx = document.getElementById('Chart2').getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Humedad del Suelo Promedio (%)',
          data: humedadSuelo,
          borderColor: 'green',    // Color de la línea
          borderWidth: 3,           // Grosor de la línea

          fill: true                // Relleno bajo la línea
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: false,
            ticks: {
              color: 'white',        // Color de las etiquetas en el eje Y
              font: {
                size: 14            // Tamaño de fuente de las etiquetas en el eje Y
              }
            }
          },
          x: {
            ticks: {
              color: 'white',        // Color de las etiquetas en el eje X
              font: {
                size: 14            // Tamaño de fuente de las etiquetas en el eje X
              }
            }
          }
        },
        plugins: {
          legend: {
            labels: {
              color: 'white',        // Color de las etiquetas de la leyenda
              font: {
                size: 18            // Tamaño de fuente de las etiquetas de la leyenda
              }
            }
          }
        }
      }
    });
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}

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

    const labels = data.map(item => new Date(item.fecha).toLocaleString());
    const humidities = data.map(item => item.promedio);

    const ctx = document.getElementById('myChart').getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Humedad Promedio (%)',
          data: humidities,
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: false
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

    const labels = data.map(item => new Date(item.fecha).toLocaleString());
    const iluminacion = data.map(item => item.promedio);

    const ctx = document.getElementById('Chart1').getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Iluminación Promedio (lux)',
          data: iluminacion,
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: false
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

    const labels = data.map(item => new Date(item.fecha).toLocaleString());
    const humedadSuelo = data.map(item => item.promedio);

    const ctx = document.getElementById('Chart2').getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Humedad del Suelo Promedio (%)',
          data: humedadSuelo,
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: false
          }
        }
      }
    });
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}

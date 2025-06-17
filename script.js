// Include annotation plugin in your HTML file:
// <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation@1.4.0"></script>

fetch('data/sample.json')
  .then(response => response.json())
  .then(data => {
    const labels = data.map(entry => entry.date);
    const entry = data[0]; // assuming single entry for simplicity

    document.getElementById("reportDate").textContent = `Report Date: ${labels[0]}`;

    function createChart(canvasId, cardId, label, value, color, suggestedMin, suggestedMax, clinicalMin, clinicalMax) {
      const ctx = document.getElementById(canvasId).getContext('2d');

      if (value == null) {
        console.warn(`No data for ${label}`);
        return;
      }

      // Add alert class to card if value is outside clinical range
      if (value < clinicalMin || value > clinicalMax) {
        document.getElementById(cardId).classList.add('alert');
      }

      new Chart(ctx, {
        type: 'line',
        data: {
          labels: [labels[0]],
          datasets: [{
            label: label,
            data: [value],
            borderColor: color,
            borderWidth: 2,
            fill: false,
            tension: 0.3,
            pointBackgroundColor: value < clinicalMin || value > clinicalMax ? 'red' : color,
            pointRadius: 6
          }]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: `${label} Over Time`
            },
            annotation: {
              annotations: {
                range: {
                  type: 'box',
                  yMin: clinicalMin,
                  yMax: clinicalMax,
                  backgroundColor: 'rgba(0, 255, 0, 0.1)',
                  borderWidth: 0
                }
              }
            }
          },
          scales: {
            y: {
              suggestedMin: suggestedMin,
              suggestedMax: suggestedMax
            }
          }
        }
      });
    }

    // Call chart for each biomarker
    createChart('totalCholesterolChart', 'totalCholesterolCard', 'Total Cholesterol (mg/dL)', entry.total_cholesterol, 'blue', 100, 300, 125, 200);
    createChart('ldlChart', 'ldlCard', 'LDL (mg/dL)', entry.ldl, 'red', 50, 200, 0, 130);
    createChart('hdlChart', 'hdlCard', 'HDL (mg/dL)', entry.hdl, 'green', 20, 80, 40, 60);
    createChart('triglyceridesChart', 'triglyceridesCard', 'Triglycerides (mg/dL)', entry.triglycerides, 'orange', 50, 250, 50, 150);
    createChart('creatinineChart', 'creatinineCard', 'Creatinine (mg/dL)', entry.creatinine, 'brown', 0, 2, 0.6, 1.3);
    createChart('vitaminDChart', 'vitaminDCard', 'Vitamin D (ng/mL)', entry.vitamin_d, 'teal', 10, 80, 20, 50);
    createChart('vitaminB12Chart', 'vitaminB12Card', 'Vitamin B12 (pg/mL)', entry.vitamin_b12, 'purple', 100, 1200, 200, 900);
    createChart('hba1cChart', 'hba1cCard', 'HbA1c (%)', entry.hba1c, 'pink', 4, 10, 4, 5.6);
  })
  .catch(error => console.error('Error loading JSON:', error));

fetch('data/sample.json')
  .then(response => response.json())
  .then(data => {
    const labels = data.map(entry => entry.date);

    // Update date text
    document.getElementById("reportDate").textContent = `Report Date: ${labels[0]}`;

    function createChart(canvasId, label, values, color, suggestedMin, suggestedMax, clinicalMin, clinicalMax) {
      if (!values || values.every(v => v == null)) {
        console.warn(`Skipping ${label} — no valid data.`);
        return;
      }

      const ctx = document.getElementById(canvasId).getContext('2d');

      new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: label,
            data: values,
            borderColor: color,
            borderWidth: 2,
            tension: 0.3,
            fill: false,
            pointBackgroundColor: values.map(v =>
              v < clinicalMin || v > clinicalMax ? 'red' : color
            ),
            pointRadius: 5
          }]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: `${label} Over Time`
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

    // Call createChart for all biomarkers
    createChart('totalCholesterolChart', 'Total Cholesterol (mg/dL)', data.map(d => d.total_cholesterol), 'blue', 100, 300, 125, 200);
    createChart('ldlChart', 'LDL (mg/dL)', data.map(d => d.ldl), 'red', 50, 200, 0, 130);
    createChart('hdlChart', 'HDL (mg/dL)', data.map(d => d.hdl), 'green', 20, 80, 40, 60);
    createChart('triglyceridesChart', 'Triglycerides (mg/dL)', data.map(d => d.triglycerides), 'orange', 50, 250, 50, 150);
    createChart('creatinineChart', 'Creatinine (mg/dL)', data.map(d => d.creatinine), 'brown', 0, 2, 0.6, 1.3);
    createChart('vitaminDChart', 'Vitamin D (ng/mL)', data.map(d => d.vitamin_d), 'teal', 10, 80, 20, 50);
    createChart('vitaminB12Chart', 'Vitamin B12 (pg/mL)', data.map(d => d.vitamin_b12), 'purple', 100, 1200, 200, 900);
    createChart('hba1cChart', 'HbA1c (%)', data.map(d => d.hba1c), 'pink', 4, 10, 4, 5.6);
  })
  .catch(error => console.error('Error loading JSON:', error));


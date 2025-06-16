// Load the sample data
fetch('data/sample.json')
  .then(response => response.json())
  .then(data => {
    function createChart(canvasId, label, dataValues, color, suggestedMin, suggestedMax, normalMin = null, normalMax = null) {
  const labels = data.map(entry => entry.date);
  const ctx = document.getElementById(canvasId).getContext('2d');

  const config = {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: label,
        data: dataValues,
        borderColor: color,
        borderWidth: 2,
        fill: false,
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: label + ' Over Time'
        },
        annotation: {
          annotations: {}
        }
      },
      scales: {
        y: {
          suggestedMin: suggestedMin,
          suggestedMax: suggestedMax
        }
      }
    }
  };

  //  clinical range is provided, shading added
  if (normalMin !== null && normalMax !== null) {
    config.options.plugins.annotation.annotations['normalRange'] = {
      type: 'box',
      yMin: normalMin,
      yMax: normalMax,
      backgroundColor: 'rgba(0, 255, 0, 0.1)',
      borderWidth: 0
    };
  }

  new Chart(ctx, config);
}

 // call the function
    createChart('ldlChart', 'LDL (mg/dL)', data.map(e => e.ldl), 'red', 50, 200, 0, 130);
    createChart('hdlChart', 'HDL (mg/dL)', data.map(e => e.hdl), 'green', 20, 80, 40, 60);
    createChart('cholesterolChart', 'Total Cholesterol (mg/dL)', data.map(e => e.total_cholesterol), 'blue', 100, 300, 125, 200);
    createChart('vitaminDChart','Vitamin D (ng/mL)',data.map(e => e.vitamin_d),'orange',10, 80, 20, 50);
    createChart('b12Chart','Vitamin B12 (pg/mL)',data.map(e => e.vitamin_b12),'purple',100, 1200, 200, 900);
    createChart('creatinineChart','Creatinine (mg/dL)',data.map(e => e.creatinine),'brown',0, 2, 0.6, 1.3);
    createChart('hba1cChart','HbA1c (%)',data.map(e => e.hba1c),'teal',4, 10, 4, 5.6);
    createChart('triglyceridesChart','Triglycerides (mg/dL)',data.map(e => e.triglycerides),'pink',50, 250, 50, 150);
  })
 
  .catch(error => console.error('Error loading data:', error));

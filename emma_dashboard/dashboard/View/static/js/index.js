function createChart(chartJSON) {

    switch(chartJSON['graph_type']) {
        case 'line':
            createLineChart(chartJSON);
            break;
        default:
            console.log("Error: Could not load chart of type: " + chartJSON['graph_type'])
    }
}

function createLineChart(chartJSON) {

  var ctx = document.getElementById(chartJSON['chart_id']);
  
  var min_date_cutoff = new Date(chartJSON['datasets'][0]['data'].slice(-1)[0]['x'])
  min_date_cutoff.setMonth(min_date_cutoff.getMonth() - 1)
  min_date_cutoff.setHours(min_date_cutoff.getHours() - 12)

  const chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: chartJSON['labels'],
        datasets: chartJSON['datasets'],
      },
      options: {
       
        maintainAspectRatio: false,
        responsive: true,

        scales: {
            y: { beginAtZero: true},
            
            x: {
              type: 'time',
              time: {
                unit: 'day'
              },
              min: min_date_cutoff,

              ticks: {
                stepSize: 7,
              }
            }
          },

      plugins: {
          title: {
              display: true,
              text: chartJSON['title'],
              color: 'black',
              font: {
                size: 14,
                family: 'Courier New'
              }
          },
          legend: {
              labels: {
                  // This more specific font property overrides the global property
                  font: {
                    size: 12,
                    family: 'Courier New'
                  }
              }
          }
      }
  }
  });


}

// Get the canvas element
const ctx = document.getElementById('progress-bar').getContext('2d');
const progress = document.getElementById('progress_percentage').value;
const label = document.getElementById('course_name').value

// Data for the graph
const data = {
  labels: [label,'','',''],
  datasets: [{
    label: 'Progress',
    data: [progress,null,null,null], // Replace with actual progress data (0-100)
    backgroundColor: [
      'rgba(1, 41, 112, 1)' // Dark Navy Blue
    ],
    borderColor: [
      'rgba(1, 41, 112, 1)', //Dark Navy Blue
    ],
    borderWidth: 1,
  }]
};

// Options for the graph
const options = {
  type: 'bar',
  data: data,
  options: {
    scales: {
      x: {
        display: true,
      },
      y: {
        display:true,
        beginAtZero: true,
        max: 100,
        ticks: {
          stepSize: 10,
        },
      },
    },
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
    },
  },
};

// Create the chart
const chart = new Chart(ctx, options);

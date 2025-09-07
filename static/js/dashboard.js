const ctx1 = document.getElementById('lineChart');
new Chart(ctx1, {
  type: 'line',
  data: {
    labels: ['Mon','Tue','Wed','Thu','Fri'],
    datasets: [{
      label: 'Scans',
      data: [12, 19, 8, 17, 22],
      borderColor: varAccent(),
      fill: false
    }]
  }
});

const ctx2 = document.getElementById('donutChart');
new Chart(ctx2, {
  type: 'doughnut',
  data: {
    labels: ['Admin','Config','Uploads'],
    datasets: [{
      data: [5, 2, 3],
      backgroundColor: [varAccent(), '#10B981', '#F59E0B']
    }]
  }
});

const ctx3 = document.getElementById('barChart');
new Chart(ctx3, {
  type: 'bar',
  data: {
    labels: ['Team A','Team B','Team C'],
    datasets: [{
      label: 'Performance',
      data: [65, 59, 80],
      backgroundColor: varAccent()
    }]
  }
});

function varAccent(){
  return getComputedStyle(document.documentElement).getPropertyValue('--accent-blue');
}

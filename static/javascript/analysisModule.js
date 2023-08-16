export function dualLineChart(title, data1, data2, label1, label2) {
  var ctx = document.getElementById("lineChart").getContext("2d");

  var data1 = data1;
  var data2 = data2;

  var chartData = {
    datasets: [
      {
        type: "line",
        label: label1,
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        borderColor: "rgba(255, 99, 132, 1)",
        borderWidth: 1,
        yAxisID: "bar-y-axis",
        data: data1,
      },
      {
        type: "line",
        label: label2,
        backgroundColor: "rgba(54, 162, 235, 0.2)",
        borderColor: "rgba(54, 162, 235, 1)",
        borderWidth: 1,
        yAxisID: "line-y-axis",
        data: data2,
      },
    ],
  };

  var chartOptions = {
    responsive: true,
    scales: {
      x: {
        display: false, // Hide x-axis labels
      },
      y: {
        display: false, // Hide y-axis labels
      },
    },
    plugins: {
      title: {
        display: true,
        text: title,
        font: {
          size: 18,
        },
      },
    },
  };

  var myChart = new Chart(ctx, {
    type: "line",
    data: chartData,
    options: chartOptions,
  });
}

// Call the function to create the chart

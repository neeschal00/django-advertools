export function dualLineChart(title, data1, data2, label1, label2) {
  var ctx = document.getElementById("lineChart").getContext("2d");

  const labels = Array.from({ length: data1.length }, (_, i) => i + 1);

  var chartData = {
    labels: labels,
    datasets: [
      {
        label: label1,
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        borderColor: "rgba(255, 99, 132, 1)",
        borderWidth: 1,
        data: data1,
        yAxisID: "y-axis-1",
      },
      {
        label: label2,
        backgroundColor: "rgba(54, 162, 235, 0.2)",
        borderColor: "rgba(54, 162, 235, 1)",
        borderWidth: 1,
        data: data2,
        yAxisID: "y-axis-2",
      },
    ],
  };

  var chartOptions = {
    responsive: true,
    scales: {
      y: [
        {
          id: "y-axis-1",
          type: "linear",
          position: "left",
          // ticks: {
          //   beginAtZero: true,
          // },
        },
        {
          id: "y-axis-2",
          type: "linear",
          position: "right",
          // ticks: {
          //   beginAtZero: true,
          // },
        },
      ],
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

// donut chart func
export function createDonutChart(
  jsonData,
  title = "Donut Chart",
  label = "label",
  elementId = ""
) {
  var ctx = document.getElementById(elementId).getContext("2d");
  if (typeof jsonData === "string") {
    jsonData = JSON.parse(jsonData);
  }
  var labels = Object.keys(jsonData);
  // console.log(labels)
  var length = labels.length;

  var data = Object.values(jsonData);

  var colors = generateRandomColors(length);
  // Define the chart data
  var data = {
    labels: labels,
    datasets: [
      {
        label: label,
        backgroundColor: colors,
        data: data,
      },
    ],
  };

  // Create the chart
  var donutChart = new Chart(document.getElementById(elementId), {
    type: "doughnut",
    data: data,
    options: {
      cutoutPercentage: 70, // Adjust the size of the hole in the middle (optional)
      responsive: true,
      plugins: {
        afterDraw: function (chart) {
          var width = chart.chart.width;
          var height = chart.chart.height;
          var ctx = chart.chart.ctx;

          ctx.restore();
          var fontSize = (height / 114).toFixed(2);
          ctx.font = fontSize + "em sans-serif";
          ctx.textBaseline = "middle";

          var text = "Status Frequencies";
          var textX = Math.round((width - ctx.measureText(text).width) / 2);
          var textY = height / 2;

          ctx.fillText(text, textX, textY);
          ctx.save();
        },
        title: {
          display: true,
          text: title,
          font: {
            size: 18,
          },
        },
      },
    },
  });
  // Apply ellipsis and hover display for labels
}

//create a pie chart functionality
export function createPieChart(
  jsonData,
  title = "Pie Chart",
  label = "label",
  elementId = ""
) {
  var ctx = document.getElementById(elementId).getContext("2d");
  if (typeof jsonData === "string") {
    jsonData = JSON.parse(jsonData);
  }
  var labels = Object.keys(jsonData);
  // console.log(labels)
  var length = labels.length;

  var data = Object.values(jsonData);

  var colors = generateRandomColors(length);
  // Define the chart data
  var data = {
    labels: labels,
    datasets: [
      {
        label: label,
        backgroundColor: colors,
        data: data,
      },
    ],
  };

  // Create the chart
  var pieChart = new Chart(document.getElementById(elementId), {
    type: "pie",
    data: data,
    options: {
      cutoutPercentage: 70, // Adjust the size of the hole in the middle (optional)
      responsive: true,
      plugins: {
        afterDraw: function (chart) {
          var width = chart.chart.width;
          var height = chart.chart.height;
          var ctx = chart.chart.ctx;

          ctx.restore();
          var fontSize = (height / 114).toFixed(2);
          ctx.font = fontSize + "em sans-serif";
          ctx.textBaseline = "middle";

          var text = "Status Frequencies";
          var textX = Math.round((width - ctx.measureText(text).width) / 2);
          var textY = height / 2;

          ctx.fillText(text, textX, textY);
          ctx.save();
        },
        title: {
          display: true,
          text: title,
          font: {
            size: 18,
          },
        },
      },
    },
  });
}

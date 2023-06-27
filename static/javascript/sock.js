// Replace <task_id> with the actual value
var random_id = "test";

// random_id = random_id();

// For key value
function createDonutChart(
  jsonData,
  title = "Donut Chart",
  label = "label",
  elementId = ""
) {
  var ctx = document.getElementById(elementId).getContext("2d");
  if (typeof jsonData === 'string'){
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
}

function createPieChart(
  jsonData,
  title = "Pie Chart",
  label = "label",
  elementId = ""
) {
  var ctx = document.getElementById(elementId).getContext("2d");
  if (typeof jsonData === 'string'){
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

if (random_id) {
  // Create the WebSocket connection
  var socket = new WebSocket(
    "ws://" + window.location.host + "/ws/group/" + random_id + "/"
  );

  // Event handler for successful connection
  socket.onopen = function (event) {
    console.log("WebSocket connection established");

    // You can perform any necessary actions after the connection is established
  };

  // Event handler for receiving messages
  socket.onmessage = function (event) {
    var message = JSON.parse(event.data);
    console.log(message);
    // console.log(typeof message)
    console.log(message.type);
    if (message.task_id) {
      console.log(message.task_id);
    }
    console.log("Received message:", message);

    if (message.type === "analysisComplete") {
      console.log("Analysis complete");
      console.log(message.task_id);
      var url = "/api/analysis/" + message.task_id + "/";
      console.log(url);
      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          console.log(data.status);
          console.log(data);
          // const content = JSON.parse(data);

          createDonutChart(
            data.result.logs_message,
            "Types of Messages in Logs",
            "Messages Received",
            "donutChart1"
          );
          // createDonutChart(data.result.logs_message,"Types of Messages in Logs","Messages Received","donutChart1")
          createPieChart(
            data.result.logs_mi,
            "Types of Middleware in Logs",
            "Middlewares Used ",
            "pieChart"
          )
          const element = document.getElementById("analysisResp");
          element.innerHTML = data.result.logs_dt;
          applyDataTablesFormatting(element);
          // initializeDatatables();
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    }

    if (message.type === "crawlRead") {
      console.log("Crawl Read");
      console.log(message.task_id);
      var url = "/api/result/" + message.task_id + "/";
      console.log(url);
      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          console.log(data.status);
          // const content = JSON.parse(data);
          const element = document.getElementById("testResp");
          element.innerHTML = data.result.crawlDf;
          applyDataTablesFormatting(element);
          // initializeDatatables();
        })

        .catch((error) => {
          console.error("Error:", error);
        });
    }

    // if (message.type != "data_converted") {
    //     window.alert(message.result);
    // }

    // Handle the received message as needed
  };

  // Event handler for connection close
  socket.onclose = function (event) {
    console.log("WebSocket connection closed");

    // You can perform any necessary actions after the connection is closed
  };
}

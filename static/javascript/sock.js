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
  // Apply ellipsis and hover display for labels
  
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


function generateDynamicContent(data) {
  // Get the container element
  var container = document.getElementById('dynamicContent');
  console.log(container);

  // Create the HTML content
  var html = ``;
  html += `<h2 class="h2 mb-2 text-center">${data.title}</h2>`;

  

  html += `
  <div class="col-md-4 col-xl-4">
    <div class="card bg-c-green order-card">
      <div class="card-block">
        <h6 class="m-b-20">URLs found</h6>
        <h2 class="text-right">
          <i class="fa fa-link f-left"></i
          ><span class="px-2">${ data.urls.overview.num_urls }</span>
        </h2>
        <p class="m-b-0">
          Urls per body<span class="f-right"
            >${ (data.urls.overview.urls_per_post).toFixed(4) }</span
          >
        </p>
        <p class="m-b-0">
          Unique Urls<span class="f-right"
            >${ data.urls.overview.unique_urls }</span
          >
        </p>
      </div>
    </div>
  </div>
  `
  html += `
  <div class="col-md-4 col-xl-4">
    <div class="card bg-c-yellow order-card">
      <div class="card-block">
        <h6 class="m-b-20">Mentions found</h6>
        <h2 class="text-right">
          <i class="fa fa-quote-left f-left"></i
          ><span class="px-2">${ data.mentions.overview.num_mentions}</span>
        </h2>
        <p class="m-b-0">
          Mentions per body<span class="f-right"
            >${ (data.mentions.overview.mentions_per_post).toFixed(4) }</span
          >
        </p>
        <p class="m-b-0">
          Unique Mentions<span class="f-right"
            >${ data.mentions.overview.unique_mentions }</span
          >
        </p>
      </div>
    </div>
  </div>
  `
  html += `
  <div class="col-md-4 col-xl-4">
    <div class="card bg-c-pink order-card">
      <div class="card-block">
        <h6 class="m-b-20">Questions found</h6>
        <h2 class="text-right">
          <i class="fa fa-question f-left"></i
          ><span class="px-2"
            >${ data.questions.overview.num_question_marks}</span
          >
        </h2>
        <p class="m-b-0">
          Questions per body<span class="f-right"
            >${ (data.questions.overview.question_marks_per_post).toFixed(4)}</span
          >
        </p>
        <p class="m-b-0">
          Unique Questions<span class="f-right"
            >${ data.questions.overview.unique_question_marks }</span
          >
        </p>
      </div>
    </div>
  </div>
  `
  html += `
  <div class="col-md-4 col-xl-4">
    <div class="card bg-c-blue order-card">
      <div class="card-block">
        <h6 class="m-b-20">Hashtags found</h6>
        <h2 class="text-right">
          <i class="fa fa-hashtag f-left"></i
          ><span class="px-2">${ data.hashtags.overview.num_hashtags}</span>
        </h2>
        <p class="m-b-0">
          Hashtags per body<span class="f-right"
            >${ (data.hashtags.overview.hashtags_per_post).toFixed(4)}</span
          >
        </p>
        <p class="m-b-0">
          Unique Hashtags<span class="f-right"
            >${ data.hashtags.overview.unique_hashtags }</span
          >
        </p>
      </div>
    </div>
  </div>
  `
  html += `
  <div class="col-md-4 col-xl-4">
    <div class="card bg-c-green order-card">
      <div class="card-block">
        <h6 class="m-b-20">Numbers found</h6>
        <h2 class="text-right">
          <i class="fa fa-arrow-up f-left"></i
          ><span class="px-2">${ data.numbers.overview.num_numbers}</span>
        </h2>
        <p class="m-b-0">
          Numbers per body<span class="f-right"
            >${(data.numbers.overview.numbers_per_post).toFixed(4)}</span
          >
        </p>
        <p class="m-b-0">
          Unique Numbers<span class="f-right"
            >${data.numbers.overview.unique_numbers }</span
          >
        </p>
      </div>
    </div>
  </div>
  `

  html+= `
  <div class="col-md-4 col-xl-4">
    <div class="card bg-c-yellow order-card">
      <div class="card-block">
        <h6 class="m-b-20">Intense Words found</h6>
        <h2 class="text-right">
          <i class="fa fa-repeat f-left"></i
          ><span class="px-2"
            >${ data.intense_words.overview.num_intense_words}</span
          >
        </h2>
        <p class="m-b-0">
          Intense Words per body<span class="f-right"
            >${ (data.intense_words.overview.intense_words_per_post).toFixed(4)}</span
          >
        </p>
        <p class="m-b-0">
          Unique Intense Words<span class="f-right"
            >${ data.intense_words.overview.unique_intense_words }</span
          >
        </p>
      </div>
    </div>
  </div>
  `

  // Set the HTML content in the container
  container.innerHTML = html;
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
    // console.log(message);
    // console.log(typeof message)
    // console.log(message.type);
    if (message.task_id) {
      console.log("Task id: "+message.task_id);
    }
    // console.log("Received message:", message);

    if (message.type === "analysisComplete" && message.task_name === "crawlLogs") {
      console.log("Analysis complete");
      console.log(message.task_id);
      var url = "/api/analysis/" + message.task_id + "/";
      console.log(url);
      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          // console.log(data.status);
          // console.log(data);
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


    if (message.type === "analysisComplete" && message.task_name === "contentAnalysis") {
      console.log("Analysis complete");
      // console.log(message.task_id);
      var url = "/api/analysis/" + message.task_id + "/";
      // console.log(url);
      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          console.log(data.status);
          
          if(data.status === "completed"){
            const result = data.result;

            // console.log(result);

            generateDynamicContent(result);
          }
          // const content = JSON.parse(data);

          // initializeDatatables();
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    }

    if (message.type === "crawlRead") {
      console.log("Crawl Read");
      // console.log(message.task_id);
      var url = "/api/result/" + message.task_id + "/";
      console.log(url);
      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          // console.log(data.status);
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

    // if (message.type == "data_converted") {
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

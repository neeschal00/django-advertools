// Replace <task_id> with the actual value
import { dualLineChart } from "./analysisModule.js";



function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}
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
  // console.log(container);

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

function createToast(type,heading,message){
  let toast = document.getElementById("liveToast");
  if (!type){
    toast.innerHTML = `
    <div class="toast-header">
      <img src="${infoImg}" class="rounded me-2 img img-fluid" width="24px" height="24px" alt="info" />
      <strong class="me-auto">${heading}</strong>
      <small>few seconds ago</small>
      <button
        type="button"
        class="btn-close"
        data-bs-dismiss="toast"
        aria-label="Close"
      ></button>
    </div>
    <div class="toast-body">${message}</div>
    `;
  }
  if (type === "error"){
    toast.innerHTML = `
    <div class="toast-header">
      <span class="fw-bold text-danger">Eror: X</span>
      <strong class="me-auto text-danger">${heading}</strong>
      <small>Just Now</small>
      <button
        type="button"
        class="btn-close"
        data-bs-dismiss="toast"
        aria-label="Close"
      ></button>
    </div>
    <div class="toast-body">${message}</div>
    `;
  }

  $('#liveToast').toast('show');
}

var random_id = getCookie("socket_id");
console.log("Socket Id is from sock.js "+ random_id);

var isSecure = window.location.protocol === 'https:';
console.log("Is secutr "+ isSecure);
if (random_id) {
  // Create the WebSocket connection
  
  // Create the WebSocket connection
  var socketProtocol = (window.location.protocol === "https:") ? "wss:" : "ws:";
  var socketURL = socketProtocol + "//" + window.location.host + "/ws/group/" + random_id + "/";
  var socket = new WebSocket(
    socketURL
  );
  let toast = document.getElementById("liveToast");
  // Event handler for successful connection
  socket.onopen = function (event) {
    console.log("WebSocket connection established");


    // You can perform any necessary actions after the connection is established
  };

  // Event handler for receiving messages
  socket.onmessage = function (event) {
    var message = JSON.parse(event.data);
    console.log(message);
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
          createToast("","Analysis Complete","Completed for types of Middleware logs");
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

            generateDynamicContent(result);
            
            
          }
          
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    }

    if (message.type === "analysisComplete" && message.task_name === "titleAnalysis") {
      console.log("Analysis complete");
      // console.log(message.task_id);
      var url = "/api/analysis/" + message.task_id + "/";
      // console.log(url);
      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          console.log(data.status);
          
          if(data.status === "success"){
            const result = data.result;
            console.log(result);
            const element = document.getElementById("titleAnalysis");
            element.innerHTML = `
              <h3 class="text-secondary">Title Analysis</h3>
              <p>Title length is ${result.length}</p>
              <h5 class="text-primary">${result.title}</h5>
              <p>${result.description}</p>
              <p><span class="fw-bold">Keywords found: </span> ${result.keywords.join(", ")} </p>
            `;
            
           
          }
          
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    }


    if (message.type === "analysisComplete" && message.task_name === "metaDescripton") {
      console.log("Analysis complete");
      // console.log(message.task_id);
      var url = "/api/analysis/" + message.task_id + "/";
      // console.log(url);
      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          console.log(data.status);
          
          if(data.status === "success"){
            const result = data.result;
            console.log(result);
            const element = document.getElementById("metaAnalysis");
            if (result.keywords){
              html = `
                <h3 class="text-secondary">Meta Description Analysis</h3>
                <p>Description length is ${result.length} </p>
                <p class="text-primary fw-bold">${result.description_meta}</p>
                <p>${result.description}</p>
                <p><span class="fw-bold">Keywords found: </span> ${result.keywords.join(", ")} </p>
              `;
            }
            else{
              html = `
              <h3 class="text-secondary">Meta Description Analysis</h3>
              <p>Description length is ${result.length} </p>
              <p class="text-primary fw-bold">${result.description_meta}</p>
              <p>${result.description}</p>
            `;
            }
            
            element.innerHTML = html
          }
          
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    }

    if (message.type === "analysisComplete" && message.task_name === "audit") {
      console.log("Audit complete");
      document.getElementById("loadingModal").style.display = "none";
      var url = "/api/analysis/" + message.task_id + "/";

      fetch(url)
      .then((response) => response.json())
      .then((data) => {
        if(data.status === "success"){
          
          const overview = data.result.audit.overview;
          const brokenlinks = data.result.audit.links["broken_links"];
          const head = data.result.audit.head;

          console.log(JSON.stringify(data));

          console.log(brokenlinks);
          const elemOverview = document.querySelector("#overview .row");
          const elemBrokenLinks = document.getElementById("broken-links");
          const keys = Object.keys(overview);
          
          var html = ``;
          keys.forEach((key)=>{
            // console.log(key);
            // console.log(overview[key]);
            let unit = "bytes";
            let type = "content"
            let bg = "bg-primary"
            if(key === "latency"){
              unit = "seconds";
              type = "downloaded content";
              bg = "bg-success"
            }
             html += `
               <div class="col-md-6">
                <div class="card ${bg} text-white">
                  <div class="container m-2">
                    <h5 class="h5 card-title fw-bold">${key} Overview</h5>
                    <div class="card-body">
                      <b>Average ${key} of ${type}:</b> ${ overview[key].mean.toFixed(3) } ${unit}.
                    </div>
                    <div class="card-body">
                      <b>Max ${key} of ${type}:</b> ${ overview[key].max.toFixed(3)} ${unit}.
                    </div>
                    <div class="card-body">
                      <b>Minimum ${key} of ${type}:</b>  ${ overview[key].min.toFixed(3)} ${unit}.
                    </div>
                  </div>
                </div>
              </div>
             `
          })
          elemOverview.innerHTML = html;

          let linkHtml = `<h5 class="h5 text-primary">${brokenlinks.length} Broken Links were found</h5>`;
          if( brokenlinks.length > 1){
            brokenlinks.forEach((value) =>{
              
              linkHtml +=`
                <li class="list-group-item"><a href="${value}" class="text-decoration-none">${value}</a></li>
              `
            });

          }

          elemBrokenLinks.innerHTML = linkHtml;

          document.getElementById("meta-overview").innerHTML = `
          <div class="card bg-primary text-white">
            <div class="container m-2">
              <h5 class="h5 card-title fw-bold">Meta Description Length Overview</h5>
              <div class="card-body">
                <b>Average length of Description:</b> ${ head["meta_desc"]["length_overview"].mean.toFixed(2) } characters.
              </div>
              <div class="card-body">
                <b>Max length of Description:</b> ${ head["meta_desc"]["length_overview"].max.toFixed(2)} characters.
              </div>
              <div class="card-body">
                <b>Minimum length of Description:</b>  ${ head["meta_desc"]["length_overview"].min.toFixed(2)} characters.
              </div>
            </div>
          </div>
          `;

          let missingMeta = `<h5 class="h5 text-primary">Missing Meta Description in total ${head["meta_desc"]["missing"]["count"]}<h5>`;
          
          head["meta_desc"]["missing"]["urls"].forEach((value) => {
            missingMeta += ` <li class="list-group-item"><a href="${value}" class="text-decoration-none">${value}</a></li>
            `
          })

          document.getElementById("meta-missing").innerHTML = missingMeta;

          document.getElementById("titleAnalysis").innerHTML = `
          <h4 class="h4 text-primary">Title was missing in ${head["title"]["missing"]["count"]} out of ${head["title"]["length_overview"]["count"]}</h4>
          <div class="col-md-6">
            <div class="card bg-primary text-white">
              <div class="container m-2">
                <h5 class="h5 card-title fw-bold">Title Length Overview</h5>
                <div class="card-body">
                  <b>Average length of Title:</b> ${ head["title"]["length_overview"].mean.toFixed(2) } characters.
                </div>
                <div class="card-body">
                  <b>Max length of Title:</b> ${ head["title"]["length_overview"].max.toFixed(2)} characters.
                </div>
                <div class="card-body">
                  <b>Minimum length of Title:</b>  ${ head["title"]["length_overview"].min.toFixed(2)} characters.
                </div>
              </div>
            </div>
          </div>
          
          `;

          document.getElementById("canonicalAnalysis").innerHTML = `
          <h4 class="h4 text-primary">Canonical Links was missing in ${head["canonical"]["missing"]["count"]} out of ${head["title"]["length_overview"]["count"]}</h4>
          <p class="p">Canonical Links were different in <b>${head["canonical"]["different"]["count"]}</b> and similar in <b>${head["canonical"]["similar"]["count"]}</b></p>
          `;
          
        }
      });
    }

    if (message.type === "analysisComplete" && message.task_name === "bodyTextAnalysis") {
      console.log("Body Text Analysis complete");
      document.getElementById("loadingModal").style.display = "none";
      var url = "/api/analysis/" + message.task_id + "/";

      fetch(url)
      .then((response) => response.json())
      .then((data) => {
        if(data.status === "success"){
          console.log(data);
          const body = data.result.body;
          const keywords = body["keywords"];
          console.log(keywords);
          const firstTwe = Object.fromEntries(Object.entries(keywords).slice(0, 20));
            // const sortedData = Object.entries(result).sort(function(a, b) {
            //   return b[1] - a[1];
            // });
            // console.log(sortedData);
          const element = document.getElementById("keywords-view");

          let html = '<h3 class="text-secondary fw-bold">Keywords</h3>';
          for (var value in firstTwe){
            // console.log(value);
            html += `<li class="list-group-item">${value} : ${keywords[value]} <span style="float:right;">See in <a class="text-end text-primary text-decoration-none" href="https://trends.google.com/trends/explore?date=now%201-d&geo=US&q=${value.trim()}&hl=en" target="_blank">Google Trends</a></span></li>`;
          } 
          element.innerHTML = html;

          const commonWords = body["commonWords"];
          // console.log(commonWords);
          const cfirstTwe = Object.fromEntries(Object.entries(commonWords).slice(0, 20));
          const cElem = document.getElementById("common-view");
          html = '<h3 class="text-secondary fw-bold">Common Words</h3>';
          for (var value in cfirstTwe){
            // console.log(value);
            html += `<li class="list-group-item">${value} : ${commonWords[value]} <span style="float:right;">See in <a class="text-end text-primary text-decoration-none" href="https://trends.google.com/trends/explore?date=now%201-d&geo=US&q=${value.trim()}&hl=en" target="_blank">Google Trends</a></span></li>`;
          } 
          cElem.innerHTML = html;

          dualLineChart("Body Text Word Count and readability",body["wordCount"],body["readability"],"Word Count","Readability")

        }
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

          if (message.task_name == "serpCrawl"){
            const element = document.getElementById("testResp");
            element.innerHTML = data.result.crawlDf;
            applyDataTablesFormatting(element);
          }
          if(message.task_name == "seoCrawler"){
            console.log(data);
            const tableElem = document.getElementById("tbody");

            const headingData = data.result.headings;
            const headingKeys = Object.keys(headingData);

            htmlCont = "";
            headingKeys.forEach(function(heading, index) {
              let names = headingData[heading];
              names.forEach(function(headingName,index){
                htmlCont += `
                <tr>
                  <th scope="row">${heading}</th>
                  <td>${headingName}</td>
                </tr>
                `
              });
            });

            tableElem.innerHTML = htmlCont;

            const contentElem = document.getElementById("contentDesc");

            contentElem.innerHTML = `
                <div class="col-md-6">
                    <div class="card bg-primary text-white">
                      <div class="container m-2">
                        <h5 class="h5 card-title fw-bold">Content Load Overview</h5>
                        <div class="card-body">
                          <b>Download Latency:</b> ${data.result.latency} sec.
                        </div>
                        <div class="card-body">
                          <b>Content Size:</b> ${data.result.content_size} Kb. and avg html size is of 33Kb.
                        </div>
                      </div>
                    </div>
                </div>
            `



          }
          
        })

        .catch((error) => {
          console.error("Error:", error);
        });
    }
    if (message.type === "getKeywords") {
      console.log(message.result)
      console.log("Analysis complete");

      var url = "/api/keywords/" + message.task_id + "/";
      // console.log(url);
      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          console.log(data.status);
          
          if(data.status === "success"){
            const result = data.keywords;
            // console.log(result);
            const firstTwe = result.slice(0, 20);
            // const sortedData = Object.entries(result).sort(function(a, b) {
            //   return b[1] - a[1];
            // });
            // console.log(sortedData);
            const element = document.getElementById("keywords-view");
            html = '<h3 class="text-secondary fw-bold">Keywords</h3>';
            for (var value in firstTwe){
              // console.log(value);
              html += `<li class="list-group-item">${result[value][0]} : ${result[value][1]} <span style="float:right;">See in <a class="text-end text-primary text-decoration-none" href="https://trends.google.com/trends/explore?date=now%201-d&geo=US&q=${result[value][0].trim()}&hl=en" target="_blank">Google Trends</a></span></li>`;
            } 
            element.innerHTML = html;
            document.getElementById("loadingModal").style.display = "none";
            document.querySelector('button[type="submit"]').disabled = false;
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    }

    // if (message.type == "data_converted") {
    //     window.alert(message.result);
    // }

    if (message.type === "task_completed") {
      createToast("","Task Complete",message.result)
      
    }

    if (message.type === "data_converted") {
      console.log("Report Generated")
      createToast("","Profiling Report Completed",message.result)
    }

    if (message.type === "report_failed") {
      createToast("error","Profiling Report Failed",message.result)
      var profileBtn = document.getElementById("profile-report");
      profileBtn.disabled = True;
    }
    
    // Handle the received message as needed
  };

  // Event handler for connection close
  socket.onclose = function (event) {
    console.log("WebSocket connection closed");
  };
}

// Replace <task_id> with the actual value

import { createToast, getCookie } from "./utils.js";
import {
  analysisCrawlLogs,
  analysisContent,
  analysisTitle,
  analysisMetaDescription,
  analysisAudit,
  analysisBodyText,
  analysisSiteMap,
  analysisRobotsTxt,
  analysisInternalLinks,
} from "./processJson.js";

function fetchDataAndProcess(url, successCallback, errorCallback) {
  fetch(url)
    .then((response) => response.json())
    .then(successCallback)
    .catch(errorCallback);
}

var random_id = getCookie("socket_id");
console.log("Socket Id is from sock.js " + random_id);

var isSecure = window.location.protocol === "https:";
console.log("Is secutr " + isSecure);
if (random_id) {
  // Create the WebSocket connection

  // Create the WebSocket connection
  var socketProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  var socketURL =
    socketProtocol +
    "//" +
    window.location.host +
    "/ws/group/" +
    random_id +
    "/";
  var socket = new WebSocket(socketURL);
  let toast = document.getElementById("liveToast");
  // Event handler for successful connection
  socket.onopen = function (event) {
    console.log("WebSocket connection established");
  };

  // Event handler for receiving messages
  socket.onmessage = function (event) {
    var message = JSON.parse(event.data);
    console.log(message);
    if (message.task_id) {
      console.log("Task id: " + message.task_id);
    }
    

    if (
      message.type === "analysisComplete" &&
      message.task_name === "crawlLogs"
    ) {
      console.log("Crawl logs Analysis complete");

      var url = "/api/analysis/" + message.task_id + "/";
      console.log(url);
      fetchDataAndProcess(url, analysisCrawlLogs, (error) =>
        console.error("Error:", error)
      );
    }

    if (
      message.type === "analysisComplete" &&
      message.task_name === "contentAnalysis"
    ) {
      console.log("Analysis complete");

      var url = "/api/analysis/" + message.task_id + "/";
      
      fetchDataAndProcess(url, analysisContent, (error) =>
        console.error("Error:", error)
      );
    }

    if (
      message.type === "analysisComplete" &&
      message.task_name === "internalLinksAnalysis"
    ) {
      console.log("InternalLinks Analysis complete");

      var url = "/api/analysis/" + message.task_id + "/";
      // console.log(url);
      setTimeout(() => {
        fetchDataAndProcess(url, analysisInternalLinks, (error) =>
          console.error("Error:", error)
        );
      }, 3000);
    }

    if (
      message.type === "analysisComplete" &&
      message.task_name === "titleAnalysis"
    ) {
      console.log("Analysis complete");
      // console.log(message.task_id);
      var url = "/api/analysis/" + message.task_id + "/";
      // console.log(url);
      fetchDataAndProcess(url, analysisTitle, (error) =>
        console.error("Error:", error)
      );
    }

    if (
      message.type === "analysisComplete" &&
      message.task_name === "metaDescripton"
    ) {
      console.log("Analysis complete");
      // console.log(message.task_id);
      var url = "/api/analysis/" + message.task_id + "/";
      // console.log(url);
      fetchDataAndProcess(url, analysisMetaDescription, (error) =>
        console.error("Error:", error)
      );
    }

    if (message.type === "analysisComplete" && message.task_name === "audit") {
      console.log("Audit complete");
      document.getElementById("loadingModal").style.display = "none";
      var url = "/api/analysis/" + message.task_id + "/";

      setTimeout(() => {
        fetchDataAndProcess(url, analysisAudit, (error) =>
          console.log("Error:", error)
        );
      }, 3000);
    }

    if (
      message.type === "analysisComplete" &&
      message.task_name === "bodyTextAnalysis"
    ) {
      console.log("Body Text Analysis complete");

      document.getElementById("loadingChart").style.display = "none";
      var url = "/api/analysis/" + message.task_id + "/";
      setTimeout(() => {
        fetchDataAndProcess(url, analysisBodyText, (error) =>
          console.log("Error:", error)
        );
      }, 3000);
    }

    if (
      message.type === "analysisComplete" &&
      message.task_name === "SitemapAnalysis"
    ) {
      console.log("Sitemap txt analysis");
      // console.log(message.task_id);
      var url = "/api/result/" + message.task_id + "/";
      console.log(url);

      fetchDataAndProcess(url, analysisSiteMap, (error) =>
        console.log("Error:", error)
      );
    }

    if (
      message.type === "analysisComplete" &&
      message.task_name === "RobotsTextAnalysis"
    ) {
      console.log("Crawl Read");
      // console.log(message.task_id);
      var url = "/api/result/" + message.task_id + "/";
      console.log(url);
      fetchDataAndProcess(url, analysisRobotsTxt, (error) =>
        console.log("Error:", error)
      );
    }

    if (message.type === "crawlRead") {
      console.log("Crawl Read");
      // console.log(message.task_id);
      var url = "/api/result/" + message.task_id + "/";
      console.log(url);
      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          if (message.task_name == "serpCrawl") {
            const element = document.getElementById("testResp");
            element.innerHTML = data.result.crawlDf;
            applyDataTablesFormatting(element);
          }
          if (message.task_name == "seoCrawler") {
            console.log(data);
            const tableElem = document.getElementById("tbody");

            const headingData = data.result.headings;
            const headingKeys = Object.keys(headingData);

            htmlCont = "";
            headingKeys.forEach(function (heading, index) {
              let names = headingData[heading];
              names.forEach(function (headingName, index) {
                htmlCont += `
                <tr>
                  <th scope="row">${heading}</th>
                  <td>${headingName}</td>
                </tr>
                `;
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
            `;
          }
        })

        .catch((error) => {
          console.error("Error:", error);
        });
    }
    if (message.type === "getKeywords") {
      console.log(message.result);
      console.log("Analysis complete");

      var url = "/api/keywords/" + message.task_id + "/";
      // console.log(url);
      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          console.log(data.status);

          if (data.status === "success") {
            const result = data.keywords;
            // console.log(result);
            const firstTwe = result.slice(0, 20);
            // const sortedData = Object.entries(result).sort(function(a, b) {
            //   return b[1] - a[1];
            // });
            // console.log(sortedData);
            const element = document.getElementById("keywords-view");
            html = '<h3 class="text-secondary fw-bold">Keywords</h3>';
            for (var value in firstTwe) {
              // console.log(value);
              html += `<li class="list-group-item">${result[value][0]} : ${
                result[value][1]
              } <span style="float:right;">See in <a class="text-end text-primary text-decoration-none" href="https://trends.google.com/trends/explore?date=now%201-d&geo=US&q=${result[
                value
              ][0].trim()}&hl=en" target="_blank">Google Trends</a></span></li>`;
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
      createToast("", "Task Complete", message.result);
    }

    if (message.type === "task_started") {
      console.log("Crawling Started");
      createToast("", "Task started", message.result);
    }

    if (message.type === "data_converted") {
      console.log("Report Generated");
      createToast("", "Profiling Report Completed", message.result);
    }

    if (message.type === "report_failed") {
      createToast("error", "Profiling Report Failed", message.result);
      var profileBtn = document.getElementById("profile-report");
      profileBtn.disabled = True;
    }

    if (message.type === "crawl_failed") {
      createToast("error", "Crawling The site Failed", message.result);
    }

    if (message.type === "task_failed") {
      createToast("error", "Task Failed", message.result);
    }

    if (
      message.type === "analysisFailed" &&
      message.task_name === "bodyTextAnalysis"
    ) {
      createToast("error", "bodyTextAnalysis Failed", message.result);
    }

    // Handle the received message as needed
  };

  // Event handler for connection close
  socket.onclose = function (event) {
    console.log("WebSocket connection closed");
  };
}

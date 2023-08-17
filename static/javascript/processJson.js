import {
  dualLineChart,
  createDonutChart,
  createPieChart,
} from "./chartFunctions.js";
import { generateDynamicContent, createToast } from "./utils.js";

// Analyze the Crawl Logs and create response based on it
export function analysisCrawlLogs(data) {
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
  );
  const element = document.getElementById("analysisResp");
  element.innerHTML = data.result.logs_dt;
  applyDataTablesFormatting(element);
  createToast(
    "",
    "Analysis Complete",
    "Completed for types of Middleware logs"
  );
}

// Analyze the content where the result is formatted based on the api response
export function analysisContent(data) {
  console.log(data.status);

  if (data.status === "completed") {
    const result = data.result;

    generateDynamicContent(result, "dynamicContent");
  }
}

// Analyze the title content With keywords and short overview
export function analysisTitle(data) {
  console.log(data.status);

  if (data.status === "success") {
    const result = data.result;
    console.log(result);
    const element = document.getElementById("titleAnalysis");
    element.innerHTML = `
              <h3 class="text-secondary">Title Analysis</h3>
              <p>Title length is ${result.length}</p>
              <h5 class="text-primary">${result.title}</h5>
              <p>${result.description}</p>
              <p><span class="fw-bold">Keywords found: </span> ${result.keywords.join(
                ", "
              )} </p>
            `;
  }
}

export function analysisMetaDescription(data) {
  console.log(data.status);

  if (data.status === "success") {
    const result = data.result;
    console.log(result);
    const element = document.getElementById("metaAnalysis");
    if (result.keywords) {
      html = `
                <h3 class="text-secondary">Meta Description Analysis</h3>
                <p>Description length is ${result.length} </p>
                <p class="text-primary fw-bold">${result.description_meta}</p>
                <p>${result.description}</p>
                <p><span class="fw-bold">Keywords found: </span> ${result.keywords.join(
                  ", "
                )} </p>
              `;
    } else {
      html = `
              <h3 class="text-secondary">Meta Description Analysis</h3>
              <p>Description length is ${result.length} </p>
              <p class="text-primary fw-bold">${result.description_meta}</p>
              <p>${result.description}</p>
            `;
    }

    element.innerHTML = html;
  }
}

// Audit Analysis from Site Audit
export function analysisAudit(data) {
  if (data.status === "success") {
    const overview = data.result.audit.overview;
    const brokenlinks = data.result.audit.links["broken_links"];
    const head = data.result.audit.head;

    // console.log(JSON.stringify(data));

    // console.log(brokenlinks);
    const elemOverview = document.querySelector("#overview .row");
    const elemBrokenLinks = document.getElementById("broken-links");
    const keys = Object.keys(overview);

    var html = ``;
    keys.forEach((key) => {
      // console.log(key);
      // console.log(overview[key]);
      let unit = "bytes";
      let type = "content";
      let bg = "bg-primary";
      if (key === "latency") {
        unit = "seconds";
        type = "downloaded content";
        bg = "bg-success";
      }
      html += `
             <div class="col-md-6">
              <div class="card ${bg} text-white">
                <div class="container m-2">
                  <h5 class="h5 card-title fw-bold">${key} Overview</h5>
                  <div class="card-body">
                    <b>Average ${key} of ${type}:</b> ${overview[
        key
      ].mean.toFixed(3)} ${unit}.
                  </div>
                  <div class="card-body">
                    <b>Max ${key} of ${type}:</b> ${overview[key].max.toFixed(
        3
      )} ${unit}.
                  </div>
                  <div class="card-body">
                    <b>Minimum ${key} of ${type}:</b>  ${overview[
        key
      ].min.toFixed(3)} ${unit}.
                  </div>
                </div>
              </div>
            </div>
           `;
    });
    elemOverview.innerHTML = html;

    let linkHtml = `<h5 class="h5 text-primary">${brokenlinks.length} Broken Links were found</h5>`;
    if (brokenlinks.length > 1) {
      brokenlinks.forEach((value) => {
        linkHtml += `
              <li class="list-group-item"><a href="${value}" class="text-decoration-none">${value}</a></li>
            `;
      });
    }

    elemBrokenLinks.innerHTML = linkHtml;

    let missingMeta = `<h5 class="h5 text-primary">Missing Meta Description in total ${head["meta_desc"]["missing"]["count"]}<h5>`;

    missingMeta += `
        <div class="card bg-primary text-white">
          <div class="container m-2">
            <h5 class="h5 card-title fw-bold">Meta Description Length Overview</h5>
            <div class="card-body">
              <b>Average length of Description:</b> ${head["meta_desc"][
                "length_overview"
              ].mean.toFixed(2)} characters.
            </div>
            <div class="card-body">
              <b>Max length of Description:</b> ${head["meta_desc"][
                "length_overview"
              ].max.toFixed(2)} characters.
            </div>
            <div class="card-body">
              <b>Minimum length of Description:</b>  ${head["meta_desc"][
                "length_overview"
              ].min.toFixed(2)} characters.
            </div>
          </div>
        </div>
       `;

    document.getElementById("meta-overview").innerHTML = missingMeta;

    document.getElementById("titleAnalysis").innerHTML = `
          <h4 class="h4 text-primary">Title was missing in ${
            head["title"]["missing"]["count"]
          } out of ${head["title"]["length_overview"]["count"]}</h4>
          <div class="card bg-primary text-white">
            <div class="container m-2">
              <h5 class="h5 card-title fw-bold">Title Length Overview</h5>
              <div class="card-body">
                <b>Average length of Title:</b> ${head["title"][
                  "length_overview"
                ].mean.toFixed(2)} characters.
              </div>
              <div class="card-body">
                <b>Max length of Title:</b> ${head["title"][
                  "length_overview"
                ].max.toFixed(2)} characters.
              </div>
              <div class="card-body">
                <b>Minimum length of Title:</b>  ${head["title"][
                  "length_overview"
                ].min.toFixed(2)} characters.
              </div>
            </div>
          </div>
        `;

    document.getElementById("canonicalAnalysis").innerHTML = `
        <h4 class="h4 text-primary">Canonical Links was missing in ${head["canonical"]["missing"]["count"]} out of ${head["title"]["length_overview"]["count"]}</h4>
        <p class="p">Canonical Links were different in <b>${head["canonical"]["different"]["count"]}</b> and similar in <b>${head["canonical"]["similar"]["count"]}</b></p>
        `;
  }
}

// Body text anlysis from site-audit feature
export function analysisBodyText(data) {
  if (data.status === "success") {
    // console.log(data);
    const body = data.result.body;
    const keywords = body["keywords"];
    // console.log(keywords);
    const firstTwe = Object.fromEntries(Object.entries(keywords).slice(0, 20));
    // const sortedData = Object.entries(result).sort(function(a, b) {
    //   return b[1] - a[1];
    // });
    // console.log(sortedData);
    const element = document.getElementById("keywords-view");

    let html = '<h3 class="text-secondary fw-bold">Keywords</h3>';
    for (var value in firstTwe) {
      // console.log(value);
      html += `<li class="list-group-item">${value} : ${
        keywords[value]
      } <span style="float:right;">See in <a class="text-end text-primary text-decoration-none" href="https://trends.google.com/trends/explore?date=now%201-d&geo=US&q=${value.trim()}&hl=en" target="_blank">Google Trends</a></span></li>`;
    }
    element.innerHTML = html;

    const commonWords = body["commonWords"];
    // console.log(commonWords);
    const cfirstTwe = Object.fromEntries(
      Object.entries(commonWords).slice(0, 20)
    );
    const cElem = document.getElementById("common-view");
    html = '<h3 class="text-secondary fw-bold">Common Words</h3>';
    for (var value in cfirstTwe) {
      // console.log(value);
      html += `<li class="list-group-item">${value} : ${
        commonWords[value]
      } <span style="float:right;">See in <a class="text-end text-primary text-decoration-none" href="https://trends.google.com/trends/explore?date=now%201-d&geo=US&q=${value.trim()}&hl=en" target="_blank">Google Trends</a></span></li>`;
    }
    cElem.innerHTML = html;
    // console.log(body["wordCount"]);
    // console.log(body["readability"]);
    dualLineChart(
      "Body Text Word Count and readability",
      body["wordCount"],
      body["readability"],
      "Word Count",
      "Readability"
    );
  }
}

// Sitemap analysis of Site-Audit Feature
export function analysisSiteMap(data) {
  if (data.status === "success") {
    // console.log(data);
    const result = data.result;

    document.getElementById(
      "sitemap-overview"
    ).innerHTML = `<h5>Total Sitemap Urls Found is <b>${result["overview"]["count"]}</b> with unique <b>${result["overview"]["unique"]}</b></h5>`;

    let sitemapHtml = `<h6>Urls Missing in Sitemap but found in Crawl <b>${result["missing"]["sitemap"]["count"]}</b></h6>`;

    if (result["missing"]["sitemap"]["urls"].length > 1) {
      result["missing"]["sitemap"]["urls"].forEach((value) => {
        sitemapHtml += `
              <li class="list-group-item"><a href="${value}" class="text-decoration-none">${value}</a></li>
            `;
      });
    }

    document.getElementById("sitemap-crawl").innerHTML = sitemapHtml;

    let crawlHtml = `<h6>Urls Missing in Crawled but found in Sitemap <b>${result["missing"]["crawl"]["count"]}</b></h6>`;

    if (result["missing"]["crawl"]["urls"].length > 1) {
      result["missing"]["crawl"]["urls"].forEach((value) => {
        crawlHtml += `
              <li class="list-group-item"><a href="${value}" class="text-decoration-none">${value}</a></li>
            `;
      });
    }
    document.getElementById("crawl-sitemap").innerHTML = crawlHtml;
  }
}

// Robots text analysis Site-Audit

export function analysisRobotsTxt(data) {
  if (data.status === "success") {
    console.log(data);
    const robots = data.result.robots;

    let robotsElem = `<h5 class="h5 text-primary">Total Test performed in Robots Txt <b>${robots["totalTested"]}</b> where blocked pages were found to be <b>${robots["count"]}</b></h5>`;

    if (robots["blocked"].length > 1) {
      robots["blocked"].forEach((value) => {
        robotsElem += `
              <li class="list-group-item"><a href="${value}" class="text-decoration-none">${value}</a></li>
            `;
      });
    }

    document.getElementById("robots-test").innerHTML = robotsElem;
  }
}

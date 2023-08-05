from celery import shared_task
import logging
import os
from ydata_profiling import ProfileReport
from django.core.cache import cache
from collections import Counter

import pandas as pd
import re
from advertools import (
    crawl_headers,
    crawl,
    crawllogs_to_df,
    extract_intense_words,
    extract_hashtags,
    extract_mentions,
    extract_numbers,
    extract_questions,
    extract_urls,
    stopwords,
)
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json

channel_layer = get_channel_layer()

logger = logging.getLogger(__name__)

@shared_task
def generateReport(group_id, df, minimal=False, title="Profile Report"):
    task_id = generateReport.request.id
    print(f"Socket ID received in socket is {group_id}")
    logger.info("Socket Id"+group_id+"task id in generateReport " + task_id)
    load_df = pd.read_json(df)

    try:
        if minimal:
            profile = ProfileReport(load_df, minimal=True, title=title)
        else:
            profile = ProfileReport(load_df, minimal=False, title=title)
    except Exception as e:
        print(e)
        logger.info("Socket Id"+group_id+" "+e+" for task " + task_id)
        async_to_sync(channel_layer.group_send)(
            "group_" + group_id, {"type": "report_failed"}
        )
        return e

    try:
        profile.to_file(os.path.join("templates", "report.html"))
        logger.info("Socket Id"+group_id+" Profile report generated for task " + task_id)
        async_to_sync(channel_layer.group_send)(
            "group_" + group_id,
            {
                "type": "data_converted",
                "result": "Report generated successfully. for Id " + group_id,
            },
        )
        return "Report Has been generated successfully"

    except Exception as e:
        print(e)
        logger.info("Socket Id"+group_id+" "+e+" for task " + task_id)
        async_to_sync(channel_layer.group_send)(
            "group_" + group_id, {"type": "report_failed"}
        )
        return e


@shared_task
def add(a, b):
    return a + b


@shared_task
def serpCrawlHeaders(group_id, links: list):
    
    links = list(links)
    
    try:
        if os.path.exists("output/serp_crawl_headers_output.jl"):
            os.remove("output/serp_crawl_headers_output.jl")
    except PermissionError:
        logger.info("Socket Id"+group_id+" The output file is being used ")
        return False

    crawl_headers(
        url_list=links,
        output_file="output/serp_crawl_headers_output.jl",
        custom_settings={"LOG_FILE": "logs/crawlLogs/headerCrawl.log"},
    )
    # serpReadDf.delay(group_id, "headers")
    df = pd.read_json("output/serp_crawl_headers_output.jl", lines=True)

    logger.info("Socket Id"+group_id+" Crawl Headers complete")

    analyzeCrawlLogs.delay(group_id, "headers")

   

    async_to_sync(channel_layer.group_send)(
        "group_" + group_id, {"type": "task_completed", "result": "headers crawled"}
    )
    return {
        "status": "completed",
        "result": {
            "crawlDf": df.to_html(classes="table table-striped", justify="center"),
            "json": df.to_json(orient="records"),
        },
    }


@shared_task
def serpCrawlFull(group_id, links: list):
    try:
        if os.path.exists("output/serp_crawl_output.jl"):
            os.remove("output/serp_crawl_output.jl")
    except PermissionError:
        return False

    task_id = serpCrawlFull.request.id

    crawl(
        url_list=links,
        output_file="output/serp_crawl_output.jl",
        custom_settings={"LOG_FILE": "logs/crawlLogs/fullCrawl.log"},
    )
    logger.info("Socket Id"+group_id+" Crawl Full complete")
    async_to_sync(channel_layer.group_send)(
        "group_" + group_id, {"type": "task_completed", "result": "full crawled"}
    )
    df = pd.read_json("output/serp_crawl_output.jl", lines=True)
    task_idr = analyzeCrawlLogs.delay(group_id, "full")
    
    logger.info("Socket Id"+group_id+" Read crawl output for task "+ task_id)
    listCol = df[df["body_text"].notna()]
    listCol = listCol["body_text"].to_list()
    analyzeContent.delay(group_id,listCol,"Body Content Analysis")

    async_to_sync(channel_layer.group_send)(
        "group_" + group_id, {"type": "crawlRead", "task_id": task_id,"task_name":"serpCrawl"}
    )
    return {
        "status": "completed",
        "result": {
            "crawlDf": df.to_html(classes="table table-striped", justify="center"),
            "json": df.to_json(orient="records"),
        },
    }


@shared_task
def serpReadDf(group_id, type: str):
    if type == "headers":
        df = pd.read_json("output/serp_crawl_headers_output.jl", lines=True)
    else:
        df = pd.read_json("output/serp_crawl_output.jl", lines=True)

    data = df.to_json(orient="records")
    # print(type(data))
    logger.info("Socket Id"+group_id+" Read cawl output")
    async_to_sync(channel_layer.group_send)(
        "group_" + group_id, {"type": "data_converted", "result": data}
    )

    return True


@shared_task
def analyzeCrawlLogs(group_id, type):
    task_id = analyzeCrawlLogs.request.id
    # print("analyze crawl logs")
    # print(task_id)
    if type == "headers":
        logsDf = crawllogs_to_df(logs_file_path="logs/crawlLogs/headerCrawl.log")
    else:
        logsDf = crawllogs_to_df(logs_file_path="logs/crawlLogs/fullCrawl.log")
    
    logger.info("Socket Id"+group_id+" Crawl Logs load complete")
    async_to_sync(channel_layer.group_send)(
        "group_" + group_id, {"type": "task_completed", "result": "Crawl logs loaded"}
    )
    logs_m = logsDf["message"].value_counts().to_json()
    logs_s = logsDf["status"].value_counts().to_json()
    logs_mi = logsDf["middleware"].value_counts().to_json()

    logsDf = logsDf.reset_index(drop=True).to_html(
        classes="table table-primary table-striped text-center", justify="center"
    )

    logger.info("Socket Id"+group_id+" Analysis of crawl logs complete")
    async_to_sync(channel_layer.group_send)(
        "group_" + group_id,
        {"type": "analysisComplete", "task_id": task_id, "task_name": "crawlLogs"},
    )

    return {
        "status": "completed",
        "result": {
            "logs_message": logs_m,
            "logs_status": logs_s,
            "logs_mi": logs_mi,
            "logs_dt": logsDf,
        },
    }


@shared_task
def analyzeContent(group_id, content: list,title="Overview Analysis"):
    task_id = analyzeContent.request.id
    print("Analyze Content")
    # print(task_id)
    try:
        listCol = list(content)
        urls = extract_urls(listCol)

        mentions = extract_mentions(listCol)

        questions = extract_questions(listCol)

        numbers = extract_numbers(listCol)

        hashtags = extract_hashtags(listCol)

        intense_words = extract_intense_words(
            listCol, min_reps=3
        )  # minimum repertition of words 3

        logger.info("Socket Id"+group_id+" Content analysis complete")
        async_to_sync(channel_layer.group_send)(
            "group_" + group_id,
            {"type": "analysisComplete", "task_id": task_id, "task_name": "contentAnalysis"},
        )
        return {
            "status":"completed",
            "result":{
                "title":title,
                "urls": urls,
                "mentions": mentions,
                "questions": questions,
                "numbers": numbers,
                "hashtags": hashtags,
                "intense_words": intense_words,
            }
        }
    except Exception as e:
        logger.info("Socket Id"+group_id + " analysis failed: "+str(e))
        return {
            "status":"failed",
            "result": {
                "message": e
            }
        }

@shared_task
def get_keywords(group_id,body_text):

    task_id = get_keywords.request.id
    body_text = body_text.lower()
    pattern = r'[^a-zA-Z0-9@\s]'
    body_text = re.sub(pattern,"",body_text)
    numPattern = r'\d+'
    body_text = re.sub(numPattern,"",body_text)
    body_text = re.sub(r'\b\w\b', '', body_text)
    whiteSpacePattern = r'\s+'
    body_text = re.sub(whiteSpacePattern," ",body_text)
    for text in stopwords["english"]:
        body_text = body_text.replace(" "+text.lower()+" "," ")
    keywords = body_text.split()
    keywords = dict(Counter(keywords))
    keywords = sorted(keywords.items(),key=lambda x: x[1])[::-1]

    logger.info("Socket Id"+group_id+" Keywords Retrieved")
    async_to_sync(channel_layer.group_send)(
        "group_" + group_id, {"type": "getKeywords", "task_id": task_id}
    )
    return {
        "status": "success",
        "keywords": keywords
    }



@shared_task
def titleAnalysis(group_id,title = None):
    task_id = titleAnalysis.request.id
    
    if title:
        lengthT = len(title)
        keywords = re.sub(r'[^a-zA-Z0-9@\s]','',title.lower())
        # keywords = re.sub(r'\b\w\b', '', keywords)
        whiteSpacePattern = r'\s+'
        keywords = re.sub(whiteSpacePattern," ",keywords)
        for text in stopwords["english"]:
            keywords = keywords.replace(" "+text.lower()+" "," ")
        keywords = keywords.split()
        logger.info("Socket Id"+group_id+" Title analysis complete")
        async_to_sync(channel_layer.group_send)(
            "group_" + group_id, {"type": "analysisComplete", "task_id": task_id,"task_name":"titleAnalysis"}
        )

        if lengthT > 50 and lengthT < 70:
            return {
                "status": "success",
                "result": {
                    "title": title,
                    "length": lengthT,
                    "keywords": keywords,
                    "appropriate": True,
                    "description": f"The title is set and the length being {lengthT} is appropriate for title length which must be approx. 50-70 chars long."
                }
            }
        else:
            return {
                "status": "success",
                "result": {
                    "title": title,
                    "length": lengthT,
                    "keywords": keywords,
                    "appropriate": False,
                    "description": f"The title is set and the length being {lengthT} is not appropriate for title length which must be approx. 50-70 chars long."
                }
            }
    else:
        logger.info("Socket Id"+group_id+" Content analysis complete")
        async_to_sync(channel_layer.group_send)(
            "group_" + group_id, {"type": "analysisComplete", "task_id": task_id,"task_name":"titleAnalysis"}
        )
        return {

                "status": "failed",
                "result":{
                    "title": title,
                    "length": None,
                    "appropriate": False,
                    "description": f"The title is not set and title length which must be approx. 50-70 chars long."
                }
            }

@shared_task
def metaDescripton(group_id,description):
    task_id = metaDescripton.request.id
    
    if description:
        keywords = re.sub(r'[^a-zA-Z0-9@\s]','',description.lower())
        # keywords = re.sub(r'\b\w\b', '', keywords)
        whiteSpacePattern = r'\s+'
        keywords = re.sub(whiteSpacePattern," ",keywords)
        for text in stopwords["english"]:
            keywords = keywords.replace(" "+text.lower()+" "," ")
        keywords = keywords.split()
        lengthT = len(description)
        async_to_sync(channel_layer.group_send)(
            "group_" + group_id, {"type": "analysisComplete", "task_id": task_id,"task_name":"metaDescripton"}
        )
        if lengthT > 150 and lengthT < 170:
            return {
                "status": "success",
                "result":{
                    "description_meta": description,
                    "length": lengthT,
                    "keywords":keywords,
                    "appropriate": True,
                    "description": f"The description is set and the length being {lengthT} is appropriate for description length which must be approx. 150-170 chars long."
                }
            }
        else:
            return {
                "status": "success",
                "result":{
                    "description_meta": description,
                    "length": lengthT,
                    "keywords": keywords,
                    "appropriate": False,
                    "description": f"The description is set and the length being {lengthT} is not appropriate for description length which must be approx. 150-170 chars long."
                }
            }
    else:
        return {
                "status": "failed",
                "result": {
                    "description_meta": description,
                    "length": None,
                    "appropriate": False,
                    "description": f"The description is not set and description length which must be approx. 150-170 chars long."
                }
            }

@shared_task
def readLogFile(group_id):
    logsDf = crawllogs_to_df(logs_file_path="logs/crawlLogs/output_file.log")

    checkRobots = logsDf["url"][0]
    status = logsDf["status"][0]
    print(checkRobots)
    robotsFound = "Robots.txt wasn't found"
    if checkRobots.endswith("robots.txt") and (str(status) == "200"):
        robotsFound = "Robots.txt was found "+ checkRobots

    return {
        "status":"success",
        "result":{
            "robots": robotsFound
        }
    }


@shared_task
def runCrawler(group_id,url):

    task_id = runCrawler.request.id

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "LOG_FILE": "logs/crawlLogs/output_file.log",
    }
    try:
        if os.path.exists("output/seo_crawler.jl"):
            os.remove("output/seo_crawler.jl")
    except PermissionError:
        return False
    crawlDf = crawl(
            url,
            output_file="output/seo_crawler.jl",
            follow_links=False,
            custom_settings=custom_settings,
        )
    
    async_to_sync(channel_layer.group_send)(
        "group_" + group_id, {"type": "task_completed", "result": "Crawling Completed"}
    )
    logger.info("Socket Id"+group_id+" SEO crawl one complete")
    crawlDf = pd.read_json("output/seo_crawler.jl",lines=True)
    content_size = str(int(crawlDf["size"][0])/1000)
    latency = crawlDf["download_latency"][0]
    body_text = crawlDf["body_text"][0]
    crawled_dt = crawlDf["crawl_time"][0]
    content_type = crawlDf["resp_headers_content-type"][0]
    server = crawlDf["resp_headers_server"][0]

    get_keywords.delay(group_id,body_text)

    readLogFile.delay(group_id)

    titleAnalysis.delay(group_id,crawlDf["title"][0])
    desc = crawlDf["meta_desc"][0] if crawlDf["meta_desc"][0] else ""
    metaDescripton.delay(group_id,desc)

    hTitles = ["h1","h2","h3","h4","h6"]

    headings = {}

    for title in hTitles:
        if title in crawlDf.columns:
            headings[title] = crawlDf[title].iloc[0].split("@@")

    async_to_sync(channel_layer.group_send)(
        "group_" + group_id, {"type": "crawlRead", "task_id": task_id,"task_name":"seoCrawler"}
    )

    return {
        "status":"success",
        "result":{
            "content_size": content_size,
            "latency": latency,
            "headings": headings,
            "crawledOn": crawled_dt,
            "contentType": content_type
        }
    }



from celery import shared_task
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


@shared_task
def generateReport(group_id, df, minimal=False, title="Profile Report"):
    task_id = generateReport.request.id
    print("taks id in generateReport " + task_id)
    load_df = pd.read_json(df)

    # try:
    if minimal:
        profile = ProfileReport(load_df, minimal=True, title=title)
    else:
        profile = ProfileReport(load_df, minimal=False, title=title)

    try:
        profile.to_file(os.path.join("templates", "report.html"))
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
        async_to_sync(channel_layer.group_send)(
            "group_" + group_id, {"type": "report_failed"}
        )
        return e


@shared_task
def add(a, b):
    return a + b


@shared_task
def serpCrawlHeaders(group_id, links: list):
    # print(links)
    links = list(links)
    # print(links)
    try:
        if os.path.exists("output/serp_crawl_headers_output.jl"):
            os.remove("output/serp_crawl_headers_output.jl")
    except PermissionError:
        return False

    crawl_headers(
        url_list=links,
        output_file="output/serp_crawl_headers_output.jl",
        custom_settings={"LOG_FILE": "logs/crawlLogs/headerCrawl.log"},
    )
    # serpReadDf.delay(group_id, "headers")
    df = pd.read_json("output/serp_crawl_headers_output.jl", lines=True)

    analyzeCrawlLogs.delay(group_id, "headers")

    # listCol = df[df["body_text"].notna()]
    # listCol = listCol["body_text"].to_list()
    # analysis.delay(group_id,listCol)

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
    async_to_sync(channel_layer.group_send)(
        "group_" + group_id, {"type": "task_completed", "result": "full crawled"}
    )
    df = pd.read_json("output/serp_crawl_output.jl", lines=True)
    task_idr = analyzeCrawlLogs.delay(group_id, "full")
    # print("main id" + task_idr.id)

    # print(df)
    listCol = df[df["body_text"].notna()]
    listCol = listCol["body_text"].to_list()
    analyzeContent.delay(group_id,listCol,"Body Content Analysis")

    async_to_sync(channel_layer.group_send)(
        "group_" + group_id, {"type": "crawlRead", "task_id": task_id}
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
    async_to_sync(channel_layer.group_send)(
        "group_" + group_id, {"type": "data_converted", "result": data}
    )

    return True


@shared_task
def analyzeCrawlLogs(group_id, type):
    task_id = analyzeCrawlLogs.request.id
    print("analyze crawl logs")
    print(task_id)
    if type == "headers":
        logsDf = crawllogs_to_df(logs_file_path="logs/crawlLogs/headerCrawl.log")
    else:
        logsDf = crawllogs_to_df(logs_file_path="logs/crawlLogs/fullCrawl.log")
    async_to_sync(channel_layer.group_send)(
        "group_" + group_id, {"type": "task_completed", "result": "Crawl logs loaded"}
    )
    logs_m = logsDf["message"].value_counts().to_json()
    logs_s = logsDf["status"].value_counts().to_json()
    logs_mi = logsDf["middleware"].value_counts().to_json()

    logsDf = logsDf.reset_index(drop=True).to_html(
        classes="table table-primary table-striped text-center", justify="center"
    )

    # logsDf = logsDf.replace(
    #     'class="dataframe table"',
    #     'class="table table-primary table-striped text-center"',
    # )
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
    # try:
    listCol = list(content)
    urls = extract_urls(listCol)

    mentions = extract_mentions(listCol)

    questions = extract_questions(listCol)

    numbers = extract_numbers(listCol)

    hashtags = extract_hashtags(listCol)

    intense_words = extract_intense_words(
        listCol, min_reps=3
    )  # minimum repertition of words 3

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
    # except Exception as e:
    #     return {
    #         "status":"failed",
    #         "result": {
    #             "message": e
    #         }
    #     }

@shared_task
def get_keywords(group_id,body_text):

    task_id = get_keywords.request.id()
    body_text = body_text.lower()
    pattern = r'[^a-zA-Z0-9@\s]'
    body_text = re.sub(pattern,"",body_text)
    for text in stopwords["english"]:
        body_text = body_text.replace(" "+text.lower()+" ","")
    keywords = body_text.split()
    keywords = dict(Counter(keywords))
    keywords = sorted(keywords.items(),key=lambda x: x[1],reverse=True)
    async_to_sync(channel_layer.group_send)(
        "group_" + group_id, {"type": "getKeywords", "task_id": task_id}
    )
    return {
        "status": "success",
        "keywords": dict(keywords)
    }



@shared_task
def titleAnalysis(title = None):
    if title:
        lengthT = len(title)
        if lengthT > 50 and lengthT < 70:
            return {
                "status": "success",
                "title": title,
                "length": lengthT,
                "appropriate": True,
                "description": f"The title is set and the length being {lengthT} is appropriate for title length which must be approx. 50-70 chars long."
            }
        else:
            return {
                "status": "success",
                "title": title,
                "length": lengthT,
                "appropriate": False,
                "description": f"The title is set and the length being {lengthT} is not appropriate for title length which must be approx. 50-70 chars long."
            }
    else:
        return {
                "status": "failed",
                "title": title,
                "length": None,
                "appropriate": False,
                "description": f"The title is not set and title length which must be approx. 50-70 chars long."
            }

@shared_task
def metaDescripton(description):
    if description:
        lengthT = len(description)
        if lengthT > 150 and lengthT < 170:
            return {
                "status": "success",
                "description": description,
                "length": lengthT,
                "appropriate": True,
                "description": f"The description is set and the length being {lengthT} is appropriate for description length which must be approx. 150-170 chars long."
            }
        else:
            return {
                "status": "success",
                "description": description,
                "length": lengthT,
                "appropriate": False,
                "description": f"The description is set and the length being {lengthT} is not appropriate for description length which must be approx. 150-170 chars long."
            }
    else:
        return {
                "status": "failed",
                "description": description,
                "length": None,
                "appropriate": False,
                "description": f"The description is not set and description length which must be approx. 150-170 chars long."
            }

@shared_task
def runCrawler(group_id,url):

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "LOG_FILE": "logs/crawlLogs/output_file.log",
    }
    crawlDf = crawl(
            url,
            output_file="output/seo_crawler.jl",
            follow_links=False,
            custom_settings=custom_settings,
        )
    
    async_to_sync(channel_layer.group_send)(
        "group_" + group_id, {"type": "task_completed", "result": "Crawling Completed"}
    )
    crawlDf = pd.read_json("output/seo_crawler.jl",lines=True)
    
    body_text = crawlDf["body_text"][0]
    get_keywords.delay(group_id,body_text)


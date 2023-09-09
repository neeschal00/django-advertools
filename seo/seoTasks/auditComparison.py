
from celery import shared_task
from celery.exceptions import Retry
import logging
import os

# import time
from django.core.cache import cache
from collections import Counter
from memory_profiler import profile

import pandas as pd
import re
import tracemalloc
from advertools import (
    crawl,
    robotstxt_test,
    sitemap_to_df,
    crawllogs_to_df,
    url_to_df,
)
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from seo.utils import (
    extract_stopwords,
    extract_words,
    extract_keywords,
    text_readability,
    get_word_count,

    syllable_count,
    internal_links,
    flatten
)

channel_layer = get_channel_layer()

logger = logging.getLogger(__name__)


@shared_task
def robotsAnalysis(group_id, robots_url, url_list):
    task_id = robotsAnalysis.request.id
    tracemalloc.start()
    logger.info("Robots Analysis started with memory "+ str())
    print(task_id)
    pages = pd.DataFrame({"url": url_list})
    try:
        # robots_df = robotstxt_to_df(robots_url)
        test_df = robotstxt_test(
            robots_url,
            user_agents=[
                "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/W.X.Y.Z Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
            ],
            urls=pages["url"],
        )
        blocked_pages = test_df[test_df["can_fetch"] == False]
    except Exception as e:
        async_to_sync(channel_layer.group_send)(
            "group_" + group_id,
            {
                "type": "analysisFailed",
                "result": "Robots Txt analysis failed",
                "task_id": task_id,
                "task_name": "robotsAnalysis",
            },
        )
        return {
            "status": "failed",
            "result": {"error": "Unable to find the sitemap url"},
        }

    async_to_sync(channel_layer.group_send)(
        "group_" + group_id,
        {
            "type": "analysisComplete",
            "task_id": task_id,
            "task_name": "RobotsTextAnalysis",
        },
    )

    return {
        "status": "success",
        "result": {
            "robots": {
                "blocked": blocked_pages["url_path"].to_list(),
                "count": len(blocked_pages),
                "totalTested": len(test_df),
            }
        },
    }


@shared_task
def sitemapAnalysis(group_id, robots_url, url_list):
    task_id = sitemapAnalysis.request.id
    pages = pd.DataFrame({"url": url_list})
    logger.info("Sitemap Analysis started ")
    print(task_id)
    try:
        sitemap_df = sitemap_to_df(robots_url)
        missing_in_sitemap = set(pages["url"]) - set(sitemap_df["loc"])
        missing_in_crawl = set(sitemap_df["loc"]) - set(pages["url"])

    except ValueError:
        try:
            sitemap_df = sitemap_df(robots_url.replace("robots.txt", "sitemap.xml"))
            missing_in_sitemap = set(pages["url"]) - set(sitemap_df["loc"])
            missing_in_crawl = set(sitemap_df["loc"]) - set(pages["url"])
        except Exception as e:
            print(e)
            async_to_sync(channel_layer.group_send)(
                "group_" + group_id,
                {
                    "type": "analysisFailed",
                    "result": "Sitemap analysis failed",
                    "task_id": task_id,
                    "task_name": "sitemapAnalysis",
                },
            )
            return {"status": "failed", "result": {"message": e}}

    overview = sitemap_df["loc"].describe().to_dict()

    async_to_sync(channel_layer.group_send)(
        "group_" + group_id,
        {
            "type": "analysisComplete",
            "task_id": task_id,
            "task_name": "SitemapAnalysis",
        },
    )

    return {
        "status": "success",
        "result": {
            "missing": {
                "sitemap": {
                    "urls": list(missing_in_sitemap),
                    "count": len(missing_in_sitemap),
                },
                "crawl": {
                    "urls": list(missing_in_crawl),
                    "count": len(missing_in_crawl),
                },
            },
            "overview": overview,
        },
    }


@shared_task
def urlAnalysis(group_id, url_dict):
    task_id = urlAnalysis.request.id


@shared_task
def internalLinksAnalysis(group_id,url_links):
    print("Entered internal link analysis")
    task_id = internalLinksAnalysis.request.id

    converted_urls = list(map(internal_links,url_links))

    countPerUrl = list(map(len,converted_urls))
    flatten_urls = list(flatten(converted_urls))
    count_urls = dict(Counter(flatten_urls).most_common(10))

    async_to_sync(channel_layer.group_send)(
        "group_" + group_id,
        {
            "type": "analysisComplete",
            "task_id": task_id,
            "task_name": "internalLinksAnalysis",
        },
    )

    return {
        "status": "success",
        "result": {
            "top10": count_urls,
            "overview": {
                "count": len(url_links),
                "countPerUrl": countPerUrl
            }
        }
    }


@shared_task
def bodyTextAnalysis(group_id, body_text):
    task_id = bodyTextAnalysis.request.id
    print(type(body_text))
    try:
        body_text = pd.read_json(body_text)

        body_text["body_text"].fillna(" ",inplace=True)

        body_text["word_count"] = body_text["body_text"].apply(get_word_count)
        body_text["readability"] = body_text["body_text"].apply(text_readability)
        body_text["keywords"] = body_text["body_text"].apply(extract_keywords)
        body_text["commonKeywords"] = body_text["keywords"].apply(lambda x: dict(Counter.most_common(x)))
        # dict(Counter(all_keywords).most_common())


        response = body_text[["word_count","readability","keywords","commonKeywords"]]

    except Exception as e:
        # print(e)

        async_to_sync(channel_layer.group_send)(
            "group_" + group_id,
            {
                "type": "analysisFailed",
                "task_id": task_id,
                "task_name": "bodyTextAnalysis",
                "result": str(e),
            },
        )
        return {
            "status": "error",
            "result": "Analysis failed",
        }

    async_to_sync(channel_layer.group_send)(
        "group_" + group_id,
        {
            "type": "analysisComplete",
            "task_id": task_id,
            "task_name": "bodyTextAnalysis",
        },
    )

    return {
        "status": "success",
        "result": response
    }


@shared_task
def logsDataAnalysis(group_id):
    task_id = logsDataAnalysis.request.id

   
    logsDf = crawllogs_to_df(logs_file_path="logs/crawlLogs/fullCrawl.log")

    logger.info("Socket Id" + group_id + " Crawl Logs load complete")
    async_to_sync(channel_layer.group_send)(
        "group_" + group_id, {"type": "task_completed", "result": "Crawl logs loaded"}
    )


    logsDf["url"].fillna(" ",inplace=True)
    robots_df = logsDf.loc[logsDf['url'].str.endswith("robots.txt")]["url"]

    robotsAnalysis.delay(group_id,robots_df)



    logs_m = logsDf["message"].value_counts().to_json()
    logs_s = logsDf["status"].value_counts().to_json()
    logs_mi = logsDf["middleware"].value_counts().to_json()

    logsDf = logsDf.reset_index(drop=True).to_html(
        classes="table table-primary table-striped text-center", justify="center"
    )

    logger.info("Socket Id" + group_id + " Analysis of crawl logs complete")
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
def audit(group_id, url):
    task_id = audit.request.id

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/W.X.Y.Z Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "LOG_FILE": "logs/crawlLogs/output_file.log",
        "CLOSESPIDER_PAGECOUNT": 1000,
    }
    try:
        if os.path.exists("logs/crawlLogs/output_file.log"):
            os.remove("logs/crawlLogs/output_file.log")
        if os.path.exists("output/seo_crawler.jl"):
            os.remove("output/seo_crawler.jl")
    except PermissionError:
        return False

    try:
        # print("Crawling")
        async_to_sync(channel_layer.group_send)(
            "group_" + group_id, {"type": "task_started", "result": "Crawling started"}
        )
        crawlDf = crawl(
            url,
            output_file="output/seo_crawler.jl",
            follow_links=True,
            custom_settings=custom_settings,
        )
    except Exception as e:
        async_to_sync(channel_layer.group_send)(
            "group_" + group_id, {"type": "crawl_failed", "result": str(e)}
        )
        return e

    async_to_sync(channel_layer.group_send)(
        "group_" + group_id, {"type": "task_completed", "result": "Crawling Completed"}
    )

    logger.info("Socket Id" + group_id + " SEO crawl one complete for task " + task_id)
    columns_to_select =  [
        "url",
        "body_text",
        "download_latency",
        "size",
        "status",
        "title",
        "meta_desc",
        "canonical",
        "links_url"
    ]
    pages = pd.read_json(
        "output/seo_crawler.jl",
        dtype={
            "status":"int32",
        },
        lines=True,
    )[columns_to_select]

    

    
    logsDataAnalysis.delay(group_id)

    pages["links_url"].fillna(" ",inplace=True)
    internal_links = pages["links_url"].to_list()

    #internal_links analysis
    internalLinksAnalysis.delay(group_id,internal_links)



    ## Creation of Columns based based on functionalities

    # if len(url_list) > 900:

    #  async_to_sync(channel_layer.group_send)(
    #     "group_" + group_id,
    #     {"type": "analysisFailed", "task_id": task_id, "task_name": "audit","result":"Too many urls to process fo body"},
    # )

    # else:

    body_text = pages[["body_text","url"]]
    # body_text = body_text.to_dict()
    body_text = body_text.to_json()
    
    # body_text = {"body_text": body_text}
    bodyTextAnalysis.delay(group_id, body_text)

    latency = pages["download_latency"].describe().to_dict()
    # print(latency)
    content_size = pages["size"].describe().to_dict()
    broken_links = pages[(pages["status"] >= 400)]["url"].to_list()
    # print(content_size)

    try:
        # Get character counts of SEO desc , title
        pages["title"].fillna(" ",inplace=True)
        pages["title_length"] = pages["title"].apply(len)

        missing_title = pages[(pages["title"].isna())]["url"].to_list()
        title_length = pages["title_length"].describe().to_dict()

        title_json = {
            "length_overview": title_length,
            "missing": {"urls": missing_title, "count": len(missing_title)},
        }
    except Exception as e:
        title_json = {"Error": str(e)}

    try:
        pages["meta_desc"].fillna(" ",inplace=True)
        pages["desc_length"] = pages["meta_desc"].apply(len)

        missing_meta_desc = pages[(pages["meta_desc"].isna())]["url"].to_list()
        desc_length = pages["desc_length"].describe().to_dict()

        meta_json = {
            "length_overview": desc_length,
            "missing": {
                "urls": missing_meta_desc,
                "count": len(missing_meta_desc),
            },
        }
    except Exception as e:
        meta_json = {"Error": str(e)}
    
    try:
        # check if canonical is equal to canonical link
        pages["canonical"].fillna(" ",inplace=True)
        missing_canonical = pages[(pages["canonical"].isna())]["url"].to_list()
        pages["canonical_link"] = pages["url"] == pages["canonical"]
        condition1 = pages["canonical_link"] == False
        condition2 = pages["canonical"] != " "

        filtered_canonical = pages[condition1 & condition2]
        filtered_canonical = filtered_canonical[["url", "canonical"]]

        filtered_canonical_sim = pages[pages["canonical_link"] == True]
        filtered_canonical_sim = filtered_canonical_sim[["url", "canonical"]]

        canonicalData = {
            "missing": {
                "urls": missing_canonical,
                "count": len(missing_canonical),
            },
            "similar": {
                "values": filtered_canonical_sim.reset_index(drop=True).to_dict(),
                "count": len(filtered_canonical_sim),
            },
            "different": {
                "values": filtered_canonical.reset_index(drop=True).to_dict(),
                "count": len(filtered_canonical),
            },
        }
    except Exception as e:
        canonicalData = {"error": str(e)}

    del pages

    async_to_sync(channel_layer.group_send)(
        "group_" + group_id,
        {"type": "analysisComplete", "task_id": task_id, "task_name": "audit"},
    )

    return {
        "status": "success",
        "result": {
            "audit": {
                "head": {
                    "meta_desc": meta_json,
                    "title": title_json,
                    "canonical": canonicalData,
                },
                "links": {
                    "broken_links": broken_links,
                },
                "overview": {
                    "latency": latency,
                    "content_size": content_size,
                },
            }
        },
    }








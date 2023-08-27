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
    crawl_headers,
    crawl,
    crawllogs_to_df,
    robotstxt_to_df,
    robotstxt_test,
    extract_intense_words,
    extract_hashtags,
    extract_mentions,
    extract_numbers,
    sitemap_to_df,
    extract_questions,
    extract_urls,
    stopwords,
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
)

channel_layer = get_channel_layer()

logger = logging.getLogger(__name__)


@shared_task
def robotsAnalysis(group_id, robots_url, url_dict):
    task_id = robotsAnalysis.request.id
    tracemalloc.start()
    logger.info("Robots Analysis started with memory "+ str())
    print(task_id)
    pages = pd.DataFrame({"url": url_dict})
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

def sitemapAnalysis(group_id, robots_url, url_dict):
    task_id = sitemapAnalysis.request.id
    pages = pd.DataFrame({"url": url_dict})
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


"""
# @shared_task(bind=True, retry_kwargs={'max_retries': 3, 'countdown': 6})
@shared_task
@profile
def bodyTextAnalysis(group_id, body_text):
    task_id = bodyTextAnalysis.request.id

    # try:
    try:
        pages = pd.DataFrame({"body_text": body_text})
        # print(pages)
        logger.info("Entered Body text analysis portion")
        # print(task_id)

        # fill na with string
        pages["body_text"].fillna(" ",inplace=True)

        ### Word Count and text readability of the body text found in html generated content
        pages["word_count"] = pages["body_text"].apply(get_word_count)
        pages["readability"] = pages["body_text"].apply(text_readability)

        ### Create a seperate column with list of keywords and list of stopwords
        pages["keywords"] = pages["body_text"].apply(extract_keywords)

        keywords = pages["keywords"].sum()
        keywords = dict(Counter(keywords).most_common())

    except Exception as e:
        print(e)

        async_to_sync(channel_layer.group_send)(
            "group_" + group_id,
            {
                "type": "analysisFailed",
                "task_id": task_id,
                "task_name": "bodyTextAnalysis",
                "result": str(e)
            }
        )
        return {
            "status": "error",
            "result": "Analysis failed"
        }

    # time.sleep(1.2)
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
        "result": {
            "body": {
                "wordCount": pages["word_count"].to_list(),
                "readability": pages["readability"].to_list(),
                "keywords": keywords,
                # "commonWords": common_words,
            }
        },
    }
    
    # except MemoryError as e:
    #     raise Retry(exc=e)
"""


@shared_task
def bodyTextAnalysis(group_id, body_text):
    task_id = bodyTextAnalysis.request.id
    print(type(body_text))
    try:
        chunk_size = 100  # Adjust the chunk size based on your needs
        num_chunks = len(body_text) // chunk_size + 1
        chunks = [
            body_text[i * chunk_size : (i + 1) * chunk_size]
            for i in range(num_chunks)
        ]

        all_keywords = []
        all_word_count = []
        all_readability = []

        for chunk in chunks:
            chunk_pages = pd.DataFrame({"body_text": chunk})
            chunk_pages["body_text"].fillna(" ",inplace=True)

            chunk_pages["word_count"] = chunk_pages["body_text"].apply(get_word_count)
            chunk_pages["readability"] = chunk_pages["body_text"].apply(text_readability)
            chunk_pages["keywords"] = chunk_pages["body_text"].apply(extract_keywords)

            # chunk_pages.to_json("name" + str(index) + ".json")
            chunk_keywords = chunk_pages["keywords"].sum()
            
            all_keywords.extend(chunk_keywords)
            all_word_count.extend(chunk_pages["word_count"])
            all_readability.extend(chunk_pages["readability"])

        keywords = dict(Counter(all_keywords).most_common())
        # print(keywords)
        # print(all_readability)
        # print(all_word_count)

    except Exception as e:
        print(e)

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
        "result": {
            "body": {
                "wordCount": all_word_count,
                "readability": all_readability,
                "keywords": keywords,
            },
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
    ]
    pages = pd.read_json(
        "output/seo_crawler.jl",
        dtype={
            "status":"int32",
            # "url": pd.SparseDtype("string", fill_value=""),
            # "body_text": pd.SparseDtype("string", fill_value=""),
            # "title": pd.SparseDtype("string", fill_value=""),
            # "meta_desc": pd.SparseDtype("string", fill_value=""),
            # "canonical": pd.SparseDtype("string", fill_value="")
        },
        lines=True,
    )[columns_to_select]

    url_list = pages["url"]

    url_df = url_to_df(url_list)
    # print(url_df)

    robots_url = url_df["scheme"][0] + "://" + url_df["netloc"][0] + "/robots.txt"

    url_dict = url_list.to_dict()
    # url_dict = {"url": url_dict}
    robotsAnalysis.delay(group_id, robots_url, url_dict)

    # sitemapAna.delay(group_id,sitemap_url,url_dict)
    sitemapAnalysis.delay(group_id, robots_url, url_dict)

    ## Creation of Columns based based on functionalities

    # if len(url_list) > 900:

    #  async_to_sync(channel_layer.group_send)(
    #     "group_" + group_id,
    #     {"type": "analysisFailed", "task_id": task_id, "task_name": "audit","result":"Too many urls to process fo body"},
    # )

    # else:

    body_text = pages["body_text"]
    # body_text = body_text.to_dict()
    body_text = body_text.to_list()
    
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

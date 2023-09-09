from celery import shared_task
import logging
import os

# import time

from collections import Counter


import pandas as pd
import re
import tracemalloc
from advertools import (
    crawl,
    robotstxt_test,
    sitemap_to_df,
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
    validate_links,
    syllable_count,
    internal_links,
    flatten
)

channel_layer = get_channel_layer()

logger = logging.getLogger(__name__)




@shared_task
def keyword_analysis(group_id, keywords):
    task_id = keyword_analysis.request.id




@shared_task
def industry_research(group_id, url:list):
    task_id = industry_research.request.id

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
        "title",
        "body_text",
        "status",
        "title",
    ]

    pages = pd.read_json(
        "output/seo_crawler.jl",
        dtype={
            "status":"int32",
        },
        lines=True,
    )[columns_to_select]

    # url_list = pages["url"]

    pages["body_text"] = pages["body_text"].fillna(" ",inplace=True)

    pages["keywords"] = pages["keywords"].apply(extract_keywords)

    











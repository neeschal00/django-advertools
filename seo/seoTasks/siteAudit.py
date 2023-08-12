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
    url_to_df
)
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from seo.utils import (
    extract_stopwords,
    extract_words,
    extract_keywords,
    text_readability,
    get_word_count,
    syllable_count
)

channel_layer = get_channel_layer()

logger = logging.getLogger(__name__)



def bodyAnalysis(group_id,url):
    task_id = bodyAnalysis.request.id

@shared_task
def siteAud(group_id,url):

    task_id = siteAud.request.id

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "LOG_FILE": "logs/crawlLogs/output_file.log",
        "CLOSESPIDER_PAGECOUNT": 1000
    }
    try:
        if os.path.exists("logs/crawlLogs/output_file.log"):
            os.remove("logs/crawlLogs/output_file.log")
        if os.path.exists("output/seo_crawler.jl"):
            os.remove("output/seo_crawler.jl")
    except PermissionError:
        return False
    crawlDf = crawl(
            url,
            output_file="output/seo_crawler.jl",
            follow_links=True,
            custom_settings=custom_settings,
        )
    
    async_to_sync(channel_layer.group_send)(
        "group_" + group_id, {"type": "task_completed", "result": "Crawling Completed"}
    )
    logger.info("Socket Id"+group_id+" SEO crawl one complete")
    pages = pd.read_json("output/seo_crawler.jl",lines=True)


    url_list = crawlDf["url"]
    # print(url_list)
    # print(url_list.to_list())

    url_df = url_to_df(urls=url_list)
    # print(url_df)

    robots_url = url_df["scheme"][0]+"://"+url_df["netloc"][0]+"/robots.txt"
    print(robots_url)
    # robotsTxtAn.delay(group_id,robots_url,url_list)


    # Review sitemap
    sitemap_url = url_df["scheme"][0]+"://"+url_df["netloc"][0]+"/sitemap.xml"
    print(sitemap_url)
    # sitemapAna.delay(group_id,sitemap_url,url_list)
    
    ## Creation of Columns based based on functionalities

    ### Word Count and text readability of the body text found in html generated content
    pages['word_count'] = pages['body_text'].apply(get_word_count)
    pages['readability'] = pages['body_text'].apply(text_readability)

    ### Create a seperate column with list of keywords and list of stopwords 
    pages['keywords'] = pages['body_text'].apply(extract_keywords)
    keywords = pages['keywords'].sum()
    keywords = dict(Counter(keywords))
    
    pages['common_words'] = pages["body_text"].apply(extract_stopwords)
    common_words = pages['common_words'].sum()
    common_words = dict(Counter(common_words))


    # Get character counts of SEO desc , title
    pages["title"] = pages["title"].fillna(" ")
    pages['title_length'] = pages['title'].apply(len)

    missing_title = pages[(pages["title"].isna())]["url"].to_list()
    title_length = pages["title_length"].describe().to_dict()

    latency = pages["download_latency"].describe().to_dict()
    content_size = pages["size"].describe().to_dict()

    pages["meta_desc"] = pages["meta_desc"].fillna(" ")
    pages['desc_length'] = pages['meta_desc'].apply(len)
    
    missing_meta_desc = pages[(pages["meta_desc"].isna())]["url"].to_list()
    desc_length = pages["desc_length"].describe().to_dict()

    #check if canonical is equal to canonical link
    pages['canonical'] = pages['canonical'].fillna(" ")
    missing_canonical = pages[(pages["canonical"].isna())]["url"].to_list()
    pages['canonical_link'] = pages['url'] == pages['canonical']
    condition1 = pages['canonical_link'] == False
    condition2 = pages['canonical'] != " "

    filtered_canonical = pages[condition1 & condition2]
    filtered_canonical = filtered_canonical[["url","canonical"]]

    filtered_canonical_sim = pages[pages["canonical_link"] == True]
    filtered_canonical_sim = filtered_canonical_sim[["url","canonical"]]

    broken_links = pages[~(pages["status"] >= 400)]["url"].to_list()

    async_to_sync(channel_layer.group_send)(
        "group_" + group_id, {"type": "crawlRead", "task_id": task_id,"task_name":"seoCrawler"}
    )

    return {
        "status":"success",
        "result":{
            
            "audit": {
                "body": {
                    "wordCount": pages["word_count"],
                    "readability": pages["readability"],
                    "keywords": keywords,
                    "commonWords": common_words,
                },
                "head":{
                    "meta_desc": {
                        "length_overview": desc_length,
                        "missing":{
                            "urls": missing_meta_desc,
                            "count": len(missing_meta_desc)
                        }
                    },
                    "title": {
                        "length_overview": title_length,
                        "missing":{
                            "urls": missing_title,
                            "count": len(missing_title)
                        }
                    },
                    "canonical":{
                        "missing":{
                            "urls": missing_canonical,
                            "count":len(missing_canonical)
                        },
                        "similar": {
                            "values": filtered_canonical_sim.reset_index(drop=True).to_dict(),
                            "count": len(filtered_canonical_sim)
                        },
                        "different": {
                            "values": filtered_canonical.reset_index(drop=True).to_dict(),
                            "count": len(filtered_canonical)
                        }
                    }
                },
                "links":{
                    "broken_links": broken_links,
                },
                "overview":{
                    "latency": latency,
                    "content_size": content_size,

                }

            }
        }
    }




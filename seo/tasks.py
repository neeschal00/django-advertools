from celery import shared_task
import os
from ydata_profiling import ProfileReport
from django.core.cache import cache

import pandas as pd
from advertools import crawl_headers, crawl
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json

channel_layer = get_channel_layer()
@shared_task
def generateReport(group_id,df,minimal=False,title="Profile Report"):
   
    load_df = pd.read_json(df)
    
    try:
        if minimal:
            profile = ProfileReport(load_df,minimal=True,title=title)
        else:
            profile = ProfileReport(load_df,minimal=False,title=title)
        profile.to_file(os.path.join('templates',"report.html"))
        # messages.success("Report Has been generated sucessfully")
        
        async_to_sync(channel_layer.group_send)(
            "group_"+group_id,
            {
                'type': 'task_completed',
                'result': 'Report generated successfully. for Id '+ group_id
            }
        )
        return "Report Has been generated successfully"
    except Exception as e:
        # print(e)
        async_to_sync(channel_layer.group_send)(
            "group_"+group_id,
            {
                'type': 'conversion_failed',
            }
        )
        return "Report Has been generated successfully"
        return "Report was not generated"




@shared_task
def add(a,b):
    return a+b


@shared_task
def serpCrawlHeaders(group_id,links:list):
    # print(links)
    links = list(links)
    # print(links)
    try:
        if os.path.exists('serp_crawl_headers_output.jl'):
            os.remove('serp_crawl_headers_output.jl')
    except PermissionError:
        return False
    
    crawl_headers(url_list=links,output_file="serp_crawl_headers_output.jl",custom_settings={'LOG_FILE': 'headerCrawl.log'})
    async_to_sync(channel_layer.group_send)(
            "group_"+group_id,
            {
                'type': 'task_completed',
                'result': 'headers crawled'
            }
        )
    serpReadDf.delay(group_id,"headers")
    # df = pd.read_json('serp_crawl_headers_output.jl', lines=True)
    # async_to_sync(channel_layer.group_send)(
    #         "group_"+group_id,
    #         {
    #             'type': 'task_completed',
    #             'result': df.to_json(orient="records")
    #         }
    #     )
    return True
    
@shared_task
def serpCrawlFull(group_id,links:list):
    try:
        if os.path.exists('serp_crawl_output.jl'):
            os.remove('serp_crawl_output.jl')
    except PermissionError:
        return False
    
    crawl(url_list=links,output_file="serp_crawl_output.jl",custom_settings={'LOG_FILE': 'fullCrawl.log'})
    async_to_sync(channel_layer.group_send)(
            "group_"+group_id,
            {
                'type': 'task_completed',
                'result': 'full crawled'
            }
        )
    return True

@shared_task
def serpReadDf(group_id,type:str):
    if type == "headers":
        df = pd.read_json('serp_crawl_headers_output.jl', lines=True)
    else:
        df = pd.read_json('serp_crawl_output.jl', lines=True)

    data = df.to_json(orient="records")
    # print(type(data))
    async_to_sync(channel_layer.group_send)(
            "group_"+group_id,
            {
                'type': 'data_converted',
                'result': data
            }
        )

    return True
    




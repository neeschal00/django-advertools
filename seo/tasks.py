from celery import shared_task
import os
from ydata_profiling import ProfileReport
from django.contrib import messages
import pandas as pd
from advertools import crawl_headers, crawl
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()
@shared_task
def generateReport(task_id,df,minimal=False,title="Profile Report"):
   
    load_df = pd.read_json(df)
    try:
        if minimal:
            profile = ProfileReport(load_df,minimal=True,title=title)
        else:
            profile = ProfileReport(load_df,minimal=False,title=title)
        profile.to_file(os.path.join('templates',"report.html"))
        # messages.success("Report Has been generated sucessfully")
        
        async_to_sync(channel_layer.group_send)(
            f'task_{task_id}',
            {
                'type': 'task_completed',
                'result': 'Report generated successfully. for Id '+ task_id
            }
        )
        return "Report Has been generated successfully"
    except Exception as e:
        print(e)
        return "Report was not generated"




@shared_task
def add(a,b):
    return a+b


@shared_task
def serpCrawlHeaders(links:list):
    # print(links)
    links = list(links)
    # print(links)
    try:
        if os.path.exists('serp_crawl_headers_output.jl'):
            os.remove('serp_crawl_headers_output.jl')
    except PermissionError:
        return False
    
    crawl_headers(url_list=links,output_file="serp_crawl_headers_output.jl",custom_settings={'LOG_FILE': 'headerCrawl.log'})
    return True
    
@shared_task
def serpCrawlFull(links:list):
    try:
        if os.path.exists('serp_crawl_output.jl'):
            os.remove('serp_crawl_output.jl')
    except PermissionError:
        return False
    
    crawl(url_list=links,output_file="serp_crawl_output.jl",custom_settings={'LOG_FILE': 'fullCrawl.log'})
    return True

@shared_task
def serpReadDf(type:str):
    pass

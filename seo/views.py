from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from advertools import robotstxt_to_df, sitemap_to_df, serp_goog, knowledge_graph, crawl, crawl_headers, crawllogs_to_df
from .forms import RobotsTxt, Sitemap, SerpGoogle, KnowledgeG, Crawl, SERPCrawl

from decouple import config
# from advertools import SERP_GOOG_VALID_VALS
# from ydata_profiling import ProfileReport
from django.contrib import messages
# from celery.result import AsyncResult
from seo.tasks import generateReport, serpCrawlFull, serpCrawlHeaders
import os,json
import logging
import validators

logger = logging.getLogger(__name__)

import pandas as pd
pd.set_option('display.max_colwidth', 30)
# from parallel_pandas import ParallelPandas

#initialize parallel-pandas
# ParallelPandas.initialize(disable_pr_bar=True)


# def generateReport(df,minimal=False,title="Profile Report"):

#     # try:
#     profile = ProfileReport(df,minimal=minimal,title=title)
#     profile.to_file(os.path.join('templates',"report.html"))
#     return True
#     #     return True
#     # except Exception as e:
#     #     print(e)
        # return False

def isValidUrl(url):
    return validators.url(url)



def configRobots(url:str) -> str:

    if not url.endswith(("/robots.txt","/robots.txt/")):
        if url.endswith("/"):
            url = url + "robots.txt"
        else:
            url = url + "/robots.txt"
    
    return url

def robotsToDf(request,filters=None):

    if request.method == 'POST':
        form = RobotsTxt(request.POST)
        if form.is_valid():
            
            urls = form.cleaned_data['urls']

            urls = urls.split("\n")

            valid_urls = []
            invalid_urls = []

            for url in map(str.strip,urls):
                if isValidUrl(url):
                    valid_urls.append(url)
                else:
                    invalid_urls.append(url)

            urls = list(map(configRobots,valid_urls))
            df = robotstxt_to_df(urls)
            task_id = "test"
            dynamic_title = "Robots.txt Data profile"
            generateReport.delay(task_id,df.to_json(),False,dynamic_title)
            unique = None
            if "directive" in df:
                unique_counts = df["directive"].value_counts()
                
                new_Df = pd.DataFrame({'frequency': unique_counts,'percentage':unique_counts/len(df)*100})
                new_Df.reset_index(inplace=True)
                new_Df.columns = ['directive','frequency','percentage'] 

                
                unique = new_Df.to_json()
            
                messages.success(request,f'Robots txt dataset viewed successfully')
            
            if df.empty:
                messages.warning(request, "No columns in the dataframe")
           
            
            
            return render(request,'seo/robots.html',{'form': form,
                                                     'json': unique,
                                                     "invalid_urls": invalid_urls,
                                                    #  'unique': unique_counts.to_html(classes='table table-striped text-center', justify='center'),
                                                     'roboDf': df.to_html(classes='table table-striped text-center', justify='center')})

    else:
        form = RobotsTxt()
        return render(request,'seo/robots.html',{'form': form})

def sitemapToDf(request):
    if request.method == 'POST':
        form = Sitemap(request.POST)
        if form.is_valid():
            
            urls = form.cleaned_data['urls']
            try:
                # urls = list(map(str.strip,urls.split("\n")))
                df = sitemap_to_df(urls)
            except Exception as e:
                # print(e)
                messages.warning(request,"The url was not able to convert to a dataframe")
                return render(request,'seo/sitemap.html',{'form': form})

            # generateReport.delay(df.to_json(),title="Sitemap Data profile")

            jsonD = df.to_json(orient="records")

            overview = df["loc"].describe()
            # print(overview)

            check_http = df[["loc"]].copy()
            # print(check_http)
            check_http["https"] = list(
                map(lambda x: x.startswith('https'), check_http['loc']))
            
            # print(check_http)
            unique_counts = check_http["https"].value_counts()

            new_Df = pd.DataFrame({'frequency': unique_counts,'percentage':unique_counts/len(check_http)*100})
            new_Df.reset_index(inplace=True)
            new_Df.columns = ['https','frequency','percentage'] 

            # unique_counts['percentage'] = df["directive"].value_counts() / len(unique_counts) * 100
            unique = new_Df.to_json()
            messages.success(request,f'Sitemap dataset viewed successfully')
            logger.info("Successfully create neccessary dataframe visuals")

           
            return render(request,'seo/sitemap.html',{'form': form,
                                                      'json': jsonD,
                                                      'unique': unique,
                                                      'overview': overview.to_dict(),
                                                      'siteDf': df.to_html(col_space='75px',classes='table table-striped text-center', justify='center')})
        else:
            messages.error(request,f'Invalid form values')
    else:
        # logger.info("data helled")
        form = Sitemap()
        return render(request,'seo/sitemap.html',{'form': form})



def searchEngineResults(request):
    if request.method == 'POST':
        form = SerpGoogle(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            query = list(map(str.strip,query.split(",")))
            gl = form.cleaned_data['geolocation']
            # print(gl)
            # gl = list(map(str.strip,gl.split(",")))
            country = form.cleaned_data['country']
            language = form.cleaned_data['language']
            rights = form.cleaned_data['rights']

            # country = list(map(str.strip,country.split(","))) if country else None
            try:
                if gl or country or language or rights:
                    params = {
                        'q': query,
                        'cx': config('CX'),
                        'key': config('KEY'),
                    }
                    if gl:
                        params['gl'] = gl
                    if country:
                        params['cr'] = country
                    if language:
                        params['lr'] = language
                    if rights:
                        params['rights'] = rights
                    
                    serpDf = serp_goog(**params)
                else:
                    serpDf = serp_goog(q=query,cx=config('CX'),key=config('KEY'))
            
            except Exception as e:
                print(e)
                messages.warning(request,"Unable to make a query for invalid data")
                return render(request, 'seo/serpGoog.html',{'form': form})
            
            # generateReport.delay(serpDf.to_json(),title="SERP Data profile")

            
            domains_df = serpDf['displayLink'].value_counts()
            domains_df = pd.DataFrame({'frequency': domains_df,'percentage':domains_df/len(serpDf)*100})
            domains_df.reset_index(inplace=True)
            domains_df.columns = ['displayLink','frequency','percentage']

            rank_df = serpDf[["searchTerms","displayLink","rank","link"]].head(10)
            
            rank_df.rename(columns={"displayLink":"domain"},inplace=True)
            rank_df = rank_df.reset_index(drop=True).to_html(classes='table', justify='center')
        
            rank_df = rank_df.replace('class="dataframe table"','class="table table-primary table-striped text-center"')
            
            return render(request,'seo/serpGoog.html',{'form': form,
                                                       'serpDf':serpDf.to_html(
                classes='table table-striped text-center', justify='center'),
                'domains_df': domains_df.to_json(orient="records"),
                'rankDf':rank_df
            })

    else:
        # print(SERP_GOOG_VALID_VALS)
        form = SerpGoogle()
        return render(request, 'seo/serpGoog.html',{'form': form})
    


def knowledgeGraph(request):
    if request.method == 'POST':
        form = KnowledgeG(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            query = list(map(str.strip,query.split(",")))
            languages = form.cleaned_data['languages']
            
            languages = list(map(str.strip,languages.split(",")))if languages else None

            limit = form.cleaned_data['limit']
            if limit:
                knowDf = knowledge_graph(query=query,key=config('KEY'),languages=languages,limit=limit)
            else:
                knowDf = knowledge_graph(query=query,key=config('KEY'),languages=languages)

            # generateReport.delay(knowDf.to_json(),title="Knowledge Graph Data profile")

            jsonD = knowDf.to_json(orient="records")
            
            return render(request,'seo/knowledgeG.html',{'form': form,'knowDf':knowDf.to_html(classes='table table-striped text-center', justify='center'),'json':jsonD})

    else:
        form = KnowledgeG()
        return render(request, 'seo/knowledgeG.html',{'form': form})



def analyzeCrawlLogs(logsDf):
    
    logsDescribe = logsDf.message.value_counts()



from .utils import validate_links, delete_existing_files

def carwlLinks(request):
    overview = False
    if request.method == 'POST':
        form = Crawl(request.POST)
        if form.is_valid():
            links = form.cleaned_data['links']
            if not links.startswith("http"):
                messages.warning(request,"The url is invalid")
                logger.warning("Improper links")
                return render(request, 'seo/crawl.html',{'form': form,'overview':overview})
            else:
                links = list(map(str.strip,links.split("\n")))
                follow_links = form.cleaned_data['follow_links']
                headers_only = form.cleaned_data['headers_only']
            
            try:
                delete_existing_files()
            except PermissionError:
                messages.warning(request,"Somebody Else is using this service")
                return HttpResponseRedirect("home")

            if headers_only:
                
                crawlDf = crawl_headers(url_list=links,output_file="crawl_output.jl",
                                        custom_settings={
                        # 'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
                        'CLOSESPIDER_PAGECOUNT': int(form.cleaned_data['pg_count']) if form.cleaned_data['pg_count'] else 100 ,
                        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
                        'LOG_FILE': 'output_file.log',
                    })

                crawlDf = pd.read_json('crawl_output.jl', lines=True)

            else:
                if os.path.exists('crawl_output.jl'):
                    os.remove('crawl_output.jl')
                
                if os.path.exists('output_file.log'):
                    os.remove('output_file.log')
                crawlDf = crawl(
                    url_list=links,output_file="crawl_output.jl",follow_links=follow_links,

                    custom_settings={
                        # 'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
                        'CLOSESPIDER_PAGECOUNT': int(form.cleaned_data['pg_count']) if form.cleaned_data['pg_count'] else 100 ,
                        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
                        'LOG_FILE': 'output_file.log',
                    }
                    )
                
                crawlDf = pd.read_json('crawl_output.jl', lines=True)

            logsDf = crawllogs_to_df(logs_file_path="output_file.log")


            logsDf = logsDf.reset_index(drop=True).to_html(classes='table', justify='center')
        
            logsDf = logsDf.replace('class="dataframe table"','class="table table-primary table-striped text-center"')
            # print(logsDescribe)
            if crawlDf.empty:
                messages.warning(request,"Empty columns observed this url may not be crawlable")
                return render(request, 'seo/crawl.html',{'form': form,'overview':overview})
            else:
                jsonD = crawlDf.to_json()

                task_id = "test"
                dynamic_title = "Crawl Data profile"
                generateReport.delay(task_id,jsonD,True,dynamic_title)

                try:
                    describe = crawlDf[["size","download_latency","status"]].describe().loc[['mean','max','min']]
                except KeyError:
            
                    return render(request,'seo/crawl.html',{'form': form,'crawlDf':crawlDf.to_html(classes='table table-striped', justify='center'),'json': jsonD})
                status = crawlDf["status"].value_counts()
                status = pd.DataFrame({'frequency': status,'percentage':status/len(crawlDf)*100})
                status.reset_index(inplace=True)
                status.columns = ['status','frequency','percentage']
            
                
                overview = True
                return render(request,'seo/crawl.html',{'form': form,
                                                        'describe': describe.to_dict(),
                                                        'statusJ': status.to_json(),
                                                        'logsDf': logsDf,
                                                        
                                                        'crawlDf':crawlDf.to_html(classes='table table-striped', justify='center'),
                                                        'json': jsonD,
                                                        'overview':overview})

    else:
        if os.path.exists('crawl_output.jl'):
            os.remove('crawl_output.jl')
        form = Crawl()
        return render(request, 'seo/crawl.html',{'form': form,'overview':overview})



def serpCrawl(request):
    if request.method == 'POST':
        form = SERPCrawl(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            query = list(map(str.strip,query.split(",")))
            gl = form.cleaned_data['geolocation']
            # print(gl)
            # gl = list(map(str.strip,gl.split(",")))
            country = form.cleaned_data['country']
            language = form.cleaned_data['language']
            rights = form.cleaned_data['rights']
            limit = form.cleaned_data['limit']
            headers_only = form.cleaned_data['headers_only']

            # country = list(map(str.strip,country.split(","))) if country else None
            # try:
            if gl or country or language or rights:
                params = {
                    'q': query,
                    'cx': config('CX'),
                    'key': config('KEY'),
                }
                if gl:
                    params['gl'] = gl
                if country:
                    params['cr'] = country
                if language:
                    params['lr'] = language
                if rights:
                    params['rights'] = rights
                
                serpDf = serp_goog(**params)
            else:
                serpDf = serp_goog(q=query,cx=config('CX'),key=config('KEY'))
        

            links = serpDf["link"].to_list()
            
            
            if headers_only:
                serpCrawlHeaders.delay('test',links)
            else:
                serpCrawlFull.delay('test',links)
            
            return render(request,'seo/serpCrawl.html',{'form': form,
                                                       'serpDf':serpDf.to_html(
                classes='table table-striped text-center', justify='center'),
            })

    else:
        # print(SERP_GOOG_VALID_VALS)
        form = SERPCrawl()
        return render(request, 'seo/serpCrawl.html',{'form': form})



from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from advertools import robotstxt_to_df, sitemap_to_df, serp_goog, knowledge_graph, crawl, crawl_headers
from .forms import RobotsTxt, Sitemap, SerpGoogle, KnowledgeG, Crawl

from decouple import config
from advertools import SERP_GOOG_VALID_VALS
# from ydata_profiling import ProfileReport
from celery.result import AsyncResult
from seo.tasks import generateReport, add
import os,json
import logging
logger = logging.getLogger(__name__)


import pandas as pd
pd.set_option('display.max_colwidth', 30)


# def generateReport(df,minimal=False,title="Profile Report"):

#     # try:
#     profile = ProfileReport(df,minimal=minimal,title=title)
#     profile.to_file(os.path.join('templates',"report.html"))
#     return True
#     #     return True
#     # except Exception as e:
#     #     print(e)
        # return False



def robotsToDf(request,filters=None):

    if request.method == 'POST':
        form = RobotsTxt(request.POST)
        if form.is_valid():
            
            urls = form.cleaned_data['urls']

            urls = list(map(str.strip,urls.split("\n")))
            df = robotstxt_to_df(urls)
            task = add.delay(1,2)
            
            # task.ready()
            report_gen = AsyncResult(task.id)
            print(report_gen.status)
            print(report_gen.result)
            

            unique_counts = df["directive"].value_counts()
            
            new_Df = pd.DataFrame({'frequency': unique_counts,'percentage':unique_counts/len(df)*100})
            new_Df.reset_index(inplace=True)
            new_Df.columns = ['directive','frequency','percentage'] 

            # unique_counts['percentage'] = df["directive"].value_counts() / len(unique_counts) * 100
            unique = new_Df.to_json()

            # jsonD = df.to_json(orient="records")
            return render(request,'seo/robots.html',{'form': form,
                                                     'json': unique,
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

            # urls = list(map(str.strip,urls.split("\n")))
            df = sitemap_to_df(urls)

            generateReport(df,title="Sitemap Data profile")


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
            logger.info("Successfully create neccessary dataframe visuals")

           
            return render(request,'seo/sitemap.html',{'form': form,
                                                      'json': jsonD,
                                                      'unique': unique,
                                                      'overview': overview.to_dict(),
                                                      'siteDf': df.to_html(col_space='75px',classes='table table-striped text-center', justify='center')})

    else:
        logger.info("data helled")
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
            
            generateReport(serpDf,title="SERP Data profile")

            
            domains_df = serpDf['displayLink'].value_counts()
            domains_df = pd.DataFrame({'frequency': domains_df,'percentage':domains_df/len(serpDf)*100})
            domains_df.reset_index(inplace=True)
            domains_df.columns = ['displayLink','frequency','percentage']

            rank_df = serpDf[["searchTerms","displayLink","rank","link"]].head(10)
            # print(rank_df)
            ## convert to html
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

            generateReport(knowDf,title="Knowledge Graph Data profile")

            jsonD = knowDf.to_json(orient="records")
            
            return render(request,'seo/knowledgeG.html',{'form': form,'knowDf':knowDf.to_html(classes='table table-striped text-center', justify='center'),'json':jsonD})

    else:
        form = KnowledgeG()
        return render(request, 'seo/knowledgeG.html',{'form': form})


def carwlLinks(request):
    overview = False
    if request.method == 'POST':
        form = Crawl(request.POST)
        if form.is_valid():
            links = form.cleaned_data['links']
            if not links.startswith("http"):
                logger.warning("Improper links")
                return render(request, 'seo/crawl.html',{'form': form,'overview':overview})
            else:
                links = list(map(str.strip,links.split("\n")))
                follow_links = form.cleaned_data['follow_links']
                headers_only = form.cleaned_data['headers_only']

            if headers_only:
                if os.path.exists('crawl_output.jl'):
                    os.remove('crawl_output.jl')
                crawlDf = crawl_headers(url_list=links,output_file="crawl_output.jl")

                crawlDf = pd.read_json('crawl_output.jl', lines=True)

            else:
                if os.path.exists('crawl_output.jl'):
                    os.remove('crawl_output.jl')
                crawlDf = crawl(url_list=links,output_file="crawl_output.jl",follow_links=follow_links)
                crawlDf = pd.read_json('crawl_output.jl', lines=True)

            generateReport(crawlDf,title="Crawling Data Set profile")


            describe = crawlDf[["size","download_latency","status"]].describe().loc[['mean','max','min']]
            
            status = crawlDf["status"].value_counts()
            status = pd.DataFrame({'frequency': status,'percentage':status/len(crawlDf)*100})
            status.reset_index(inplace=True)
            status.columns = ['status','frequency','percentage']
           

            jsonD = crawlDf.to_json(orient="records")
            overview = True
            return render(request,'seo/crawl.html',{'form': form,
                                                    'describe': describe.to_dict(),
                                                    'statusJ': status.to_json(),
                                                    'crawlDf':crawlDf.to_html(classes='table table-striped', justify='center'),
                                                    'json': jsonD,
                                                    'overview':overview})

    else:
        if os.path.exists('crawl_output.jl'):
            os.remove('crawl_output.jl')
        form = Crawl()
        return render(request, 'seo/crawl.html',{'form': form,'overview':overview})


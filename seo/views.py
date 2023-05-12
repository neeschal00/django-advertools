from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from advertools import robotstxt_to_df, sitemap_to_df, serp_goog, knowledge_graph, crawl, crawl_headers
from .forms import RobotsTxt, Sitemap, SerpGoogle, KnowledgeG, Crawl
from decouple import config
from advertools import SERP_GOOG_VALID_VALS
import os

import pandas as pd
pd.set_option('display.max_colwidth', 30)

def robotsToDf(request):
    if request.method == 'POST':
        form = RobotsTxt(request.POST)
        if form.is_valid():
            
            urls = form.cleaned_data['urls']

            urls = list(map(str.strip,urls.split("\n")))
            df = robotstxt_to_df(urls)
           
            return render(request,'seo/robots.html',{'form': form,'roboDf': df.to_html(classes='table table-striped text-center', justify='center')})

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
           
            return render(request,'seo/sitemap.html',{'form': form,'siteDf': df.to_html(col_space='75px',classes='table table-striped text-center', justify='center')})

    else:
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
            return render(request,'seo/serpGoog.html',{'form': form,'serpDf':serpDf.to_html(classes='table table-striped text-center', justify='center')})

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

            
            return render(request,'seo/knowledgeG.html',{'form': form,'knowDf':knowDf.to_html(classes='table table-striped text-center', justify='center')})

    else:
        form = KnowledgeG()
        return render(request, 'seo/knowledgeG.html',{'form': form})


def carwlLinks(request):
    if request.method == 'POST':
        form = Crawl(request.POST)
        if form.is_valid():
            links = form.cleaned_data['links']
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

            return render(request,'seo/crawl.html',{'form': form,'crawlDf':crawlDf.to_html(classes='table table-striped text-center', justify='center')})

    else:
        if os.path.exists('crawl_output.jl'):
            os.remove('crawl_output.jl')
        form = Crawl()
        return render(request, 'seo/crawl.html',{'form': form})


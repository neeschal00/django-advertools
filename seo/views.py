from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from advertools import robotstxt_to_df, sitemap_to_df
from .forms import RobotsTxt,Sitemap

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




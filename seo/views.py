from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from advertools import (
    robotstxt_to_df,
    sitemap_to_df,
    serp_goog,
    knowledge_graph,
    crawl,
    crawl_headers,
    crawllogs_to_df,
    url_to_df,
    stopwords,
)
from .forms import (
    RobotsTxt,
    Sitemap,
    SerpGoogle,
    KnowledgeG,
    Crawl,
    SERPCrawl,
    SeoAnalyzeForm,
    IndustrySEO,
)
import os
import validators

# from decouple import config
from collections import Counter
from .utils import *
from .seoTasks.audit import audit
from .seoTasks.industry import industry_research
# from advertools import SERP_GOOG_VALID_VALS
# from ydata_profiling import ProfileReport
from django.contrib import messages

# from celery.result import AsyncResult
from seo.tasks import (
    generateReport,
    serpCrawlFull,
    serpCrawlHeaders,
    analyzeContent,
    runCrawler,
    siteAud,
)
import os, json
import logging
import validators

logger = logging.getLogger(__name__)

import pandas as pd

pd.set_option("display.max_colwidth", 30)
# from parallel_pandas import ParallelPandas

# initialize parallel-pandas
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


def configRobots(url: str) -> str:
    if not url.endswith(("/robots.txt", "/robots.txt/")):
        if url.endswith("/"):
            url = url + "robots.txt"
        else:
            url = url + "/robots.txt"

    return url


def robotsToDf(request, filters=None):
    if request.method == "POST":
        form = RobotsTxt(request.POST)
        if form.is_valid():
            urls = form.cleaned_data["urls"]

            urls = urls.split("\n")

            valid_urls = []
            invalid_urls = []

            for url in map(str.strip, urls):
                if isValidUrl(url):
                    valid_urls.append(url)
                else:
                    invalid_urls.append(url)

            urls = list(map(configRobots, valid_urls))
            df = robotstxt_to_df(urls)
            group_id = request.COOKIES.get("socket_id", None)
            logger.info("Socket Is is " + group_id)
            dynamic_title = "Robots.txt Data profile"
            task_id = generateReport.delay(group_id, df.to_json(), False, dynamic_title)
            # print("Task id in robots.txt "+ task_id.id)
            unique = None
            if "directive" in df:
                unique_counts = df["directive"].value_counts()

                new_Df = pd.DataFrame(
                    {
                        "frequency": unique_counts,
                        "percentage": unique_counts / len(df) * 100,
                    }
                )
                new_Df.reset_index(inplace=True)
                new_Df.columns = ["directive", "frequency", "percentage"]

                unique = new_Df.to_json()

                messages.success(request, f"Robots txt dataset viewed successfully")

            if df.empty:
                messages.warning(request, "No columns in the dataframe")

            return render(
                request,
                "seo/robots.html",
                {
                    "form": form,
                    "json": unique,
                    "invalid_urls": invalid_urls,
                    "task_id": task_id.id,
                    #  'unique': unique_counts.to_html(classes='table table-striped text-center', justify='center'),
                    "roboDf": df.to_html(
                        classes="table table-striped text-center", justify="center"
                    ),
                },
            )

    else:
        form = RobotsTxt()
        return render(request, "seo/robots.html", {"form": form})


def sitemapToDf(request):
    if request.method == "POST":
        form = Sitemap(request.POST)
        if form.is_valid():
            urls = form.cleaned_data["urls"]
            try:
                df = sitemap_to_df(urls)
            except Exception as e:
                messages.warning(
                    request, "The url was not able to convert to a dataframe"
                )
                return render(request, "seo/sitemap.html", {"form": form})
            group_id = request.COOKIES.get("socket_id", None)
            logger.info("Socket Is is " + group_id)
            generateReport.delay(group_id, df.to_json(), False, "Sitemap Data profile")

            jsonD = df.to_json(orient="records")

            overview = df["loc"].describe()

            check_http = df[["loc"]].copy()

            check_http["https"] = list(
                map(lambda x: x.startswith("https"), check_http["loc"])
            )

            unique_counts = check_http["https"].value_counts()

            new_Df = pd.DataFrame(
                {
                    "frequency": unique_counts,
                    "percentage": unique_counts / len(check_http) * 100,
                }
            )
            new_Df.reset_index(inplace=True)
            new_Df.columns = ["https", "frequency", "percentage"]

            unique = new_Df.to_json()
            messages.success(request, f"Sitemap dataset viewed successfully")
            logger.info("Successfully create neccessary dataframe visuals")

            return render(
                request,
                "seo/sitemap.html",
                {
                    "form": form,
                    "json": jsonD,
                    "unique": unique,
                    "overview": overview.to_dict(),
                    "siteDf": df.to_html(
                        col_space="75px",
                        classes="table table-striped text-center",
                        justify="center",
                    ),
                },
            )
        else:
            messages.error(request, f"Invalid form values")
    else:
        form = Sitemap()
        return render(request, "seo/sitemap.html", {"form": form})


def searchEngineResults(request):
    if request.method == "POST":
        form = SerpGoogle(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            query = list(map(str.strip, query.split(",")))
            gl = form.cleaned_data["geolocation"]
            country = form.cleaned_data["country"]
            language = form.cleaned_data["language"]
            rights = form.cleaned_data["rights"]

            try:
                if gl or country or language or rights:
                    params = {
                        "q": query,
                        "cx": os.environ.get("CX"),
                        "key": os.environ.get("KEY"),
                    }
                    if gl:
                        params["gl"] = gl
                    if country:
                        params["cr"] = country
                    if language:
                        params["lr"] = language
                    if rights:
                        params["rights"] = rights

                    serpDf = serp_goog(**params)
                else:
                    serpDf = serp_goog(
                        q=query, cx=os.environ.get("CX"), key=os.environ.get("KEY")
                    )

            except Exception as e:
                print(e)
                messages.warning(request, "Unable to make a query for invalid data")
                return render(request, "seo/serpGoog.html", {"form": form})

            serpDf = serpDf.sort_values(by="rank")

            group_id = request.COOKIES.get("socket_id", None)
            logger.info("Socket Is is " + group_id)
            generateReport.delay(group_id, serpDf.to_json(), False, "SERP Data profile")

            domains_df = serpDf["displayLink"].value_counts()
            domains_df = pd.DataFrame(
                {"frequency": domains_df, "percentage": domains_df / len(serpDf) * 100}
            )
            domains_df.reset_index(inplace=True)
            domains_df.columns = ["displayLink", "frequency", "percentage"]

            rank_df = serpDf[["searchTerms", "displayLink", "rank", "link"]].head(10)

            rank_df.rename(columns={"displayLink": "domain"}, inplace=True)
            rank_df = rank_df.reset_index(drop=True).to_html(
                classes="table table-primary table-striped text-center",
                justify="center",
            )

            # rank_df = rank_df.replace(
            #     'class="dataframe table"',
            #     'class="table table-primary table-striped text-center"',
            # )

            return render(
                request,
                "seo/serpGoog.html",
                {
                    "form": form,
                    "serpDf": serpDf.to_html(
                        classes="table table-striped text-center", justify="center"
                    ),
                    "domains_df": domains_df.to_json(orient="records"),
                    "rankDf": rank_df,
                },
            )

    else:
        form = SerpGoogle()
        return render(request, "seo/serpGoog.html", {"form": form})


def knowledgeGraph(request):
    if request.method == "POST":
        form = KnowledgeG(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            query = list(map(str.strip, query.split(",")))
            query = list(filter(None, query))
            languages = form.cleaned_data["languages"]

            languages = (
                list(map(str.strip, languages.split(","))) if languages else None
            )
            languages = list(filter(None, languages))

            limit = form.cleaned_data["limit"]
            if limit:
                knowDf = knowledge_graph(
                    query=query,
                    key=os.environ.get("KEY"),
                    languages=languages,
                    limit=limit,
                )
            else:
                knowDf = knowledge_graph(
                    query=query, key=os.environ.get("KEY"), languages=languages
                )
            analysis = False
            try:
                knowDf = knowDf.sort_values(by="resultScore", ascending=False)
                listCol = knowDf[
                    knowDf["result.detailedDescription.articleBody"].notna()
                ]
                listCol = listCol["result.detailedDescription.articleBody"].to_list()

                submission = True
                group_id = request.COOKIES.get("socket_id", None)
                generateReport.delay(
                    group_id, knowDf.to_json(), False, "Knowledge Graph Data profile"
                )

                jsonD = knowDf.to_json(orient="records")
                analysis = True
                analyzeContent.delay(group_id, listCol, "KG article body Analysis")
                return render(
                    request,
                    "seo/knowledgeG.html",
                    {
                        "form": form,
                        "knowDf": knowDf.to_html(
                            classes="table table-striped text-center", justify="center"
                        ),
                        "json": jsonD,
                        "analysis": analysis,
                        "submission": submission,
                    },
                )

            except Exception as e:
                print(e)
                messages.warning(
                    request, "Unable to analyze the particular column articleBody"
                )
                submission = True
                group_id = request.COOKIES.get("socket_id", None)
                generateReport.delay(
                    group_id, knowDf.to_json(), False, "Knowledge Graph Data profile"
                )

                jsonD = knowDf.to_json(orient="records")

                return render(
                    request,
                    "seo/knowledgeG.html",
                    {
                        "form": form,
                        "knowDf": knowDf.to_html(
                            classes="table table-striped text-center", justify="center"
                        ),
                        "json": jsonD,
                        "analysis": analysis,
                    },
                )

    else:
        form = KnowledgeG()
        return render(request, "seo/knowledgeG.html", {"form": form})


from .utils import delete_existing_files


def analyzeCrawlLogs():
    logsDf = crawllogs_to_df(logs_file_path="logs/crawlLogs/output_file.log")

    logs_m = logsDf["message"].value_counts().to_json()
    logs_s = logsDf["status"].value_counts().to_json()
    logs_mi = logsDf["middleware"].value_counts().to_json()

    logsDf = logsDf.reset_index(drop=True).to_html(classes="table", justify="center")

    logsDf = logsDf.replace(
        'class="dataframe table"',
        'class="table table-primary table-striped text-center"',
    )

    return {
        "logs_message": logs_m,
        "logs_status": logs_s,
        "logs_mi": logs_mi,
        "logsDf": logsDf,
    }


def carwlLinks(request):
    overview = False
    analysis = False
    if request.method == "POST":
        form = Crawl(request.POST)
        if form.is_valid():
            links = form.cleaned_data["links"]
            if not links.startswith("http"):
                messages.warning(request, "The url is invalid")
                logger.warning("Improper links")
                return render(
                    request, "seo/crawl.html", {"form": form, "overview": overview}
                )
            else:
                links = list(map(str.strip, links.split("\n")))
                follow_links = form.cleaned_data["follow_links"]
                headers_only = form.cleaned_data["headers_only"]

            try:
                delete_existing_files()
            except PermissionError:
                messages.warning(request, "Somebody Else is using this service")
                return HttpResponseRedirect("home")

            custom_settings = {
                "CLOSESPIDER_PAGECOUNT": int(form.cleaned_data["pg_count"])
                if form.cleaned_data["pg_count"]
                else 100,
                "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
                "LOG_FILE": "logs/crawlLogs/output_file.log",
            }

            if headers_only:
                crawlDf = crawl_headers(
                    url_list=links,
                    output_file="output/crawl_output.jl",
                    custom_settings=custom_settings,
                )

                crawlDf = pd.read_json("output/crawl_output.jl", lines=True)

            else:
                delete_existing_files()
                crawlDf = crawl(
                    url_list=links,
                    output_file="output/crawl_output.jl",
                    follow_links=follow_links,
                    custom_settings=custom_settings,
                )

                crawlDf = pd.read_json("output/crawl_output.jl", lines=True)

            logsAnalysis = analyzeCrawlLogs()

            if crawlDf.empty:
                messages.warning(
                    request, "Empty columns observed this url may not be crawlable"
                )
                return render(
                    request, "seo/crawl.html", {"form": form, "overview": overview}
                )
            else:
                jsonD = crawlDf.to_json(orient="records")

                group_id = request.COOKIES.get("socket_id", None)
                dynamic_title = "Crawl Data profile"
                generateReport.delay(group_id, jsonD, True, dynamic_title)

                try:
                    describe = (
                        crawlDf[["size", "download_latency", "status"]]
                        .describe()
                        .loc[["mean", "max", "min"]]
                    )
                    # print(describe)
                    # describe = describe.to_dict()

                except KeyError:
                    analysis = True
                    return render(
                        request,
                        "seo/crawl.html",
                        {
                            **logsAnalysis,
                            "analysis": analysis,
                            "form": form,
                            "crawlDf": crawlDf.to_html(
                                classes="table table-striped", justify="center"
                            ),
                            "json": jsonD,
                        },
                    )

                overview = True

                listCol = crawlDf[crawlDf["body_text"].notna()]

                listCol = listCol["body_text"].to_list()

                analyzeContent.delay(group_id, listCol, "Crawl Body Response Analysis")

                analysis = True

                return render(
                    request,
                    "seo/crawl.html",
                    {
                        **logsAnalysis,
                        "form": form,
                        "describe": describe.to_dict(),
                        "crawlDf": crawlDf.to_html(
                            classes="table table-striped", justify="center"
                        ),
                        "analysis": analysis,
                        "json": jsonD,
                        "overview": overview,
                    },
                )

    else:
        if os.path.exists("output/crawl_output.jl"):
            os.remove("output/crawl_output.jl")
        form = Crawl()
        return render(request, "seo/crawl.html", {"form": form, "overview": overview})


def serpCrawl(request):
    if request.method == "POST":
        form = SERPCrawl(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            query = list(map(str.strip, query.split(",")))
            gl = form.cleaned_data["geolocation"]

            country = form.cleaned_data["country"]
            language = form.cleaned_data["language"]
            rights = form.cleaned_data["rights"]
            limit = form.cleaned_data["limit"]
            headers_only = form.cleaned_data["headers_only"]

            if gl or country or language or rights:
                params = {
                    "q": query,
                    "cx": os.environ.get("CX"),
                    "key": os.environ.get("KEY"),
                }
                if gl:
                    params["gl"] = gl
                if country:
                    params["cr"] = country
                if language:
                    params["lr"] = language
                if rights:
                    params["rights"] = rights

                serpDf = serp_goog(**params)
            else:
                serpDf = serp_goog(
                    q=query, cx=os.environ.get("CX"), key=os.environ.get("KEY")
                )

            links = serpDf["link"].to_list()

            serpDf = serpDf.sort_values(by="rank")
            group_id = request.COOKIES.get("socket_id", None)

            if headers_only:
                task_id = serpCrawlHeaders.delay(group_id, links)
            else:
                task_id = serpCrawlFull.delay(group_id, links)

            domains_df = serpDf["displayLink"].value_counts()
            domains_df = pd.DataFrame(
                {"frequency": domains_df, "percentage": domains_df / len(serpDf) * 100}
            )
            domains_df.reset_index(inplace=True)
            domains_df.columns = ["displayLink", "frequency", "percentage"]

            rank_df = serpDf[["searchTerms", "displayLink", "rank", "link"]].head(10)

            rank_df.rename(columns={"displayLink": "domain"}, inplace=True)
            rank_df = rank_df.reset_index(drop=True).to_html(
                classes="table table-primary table-striped text-center",
                justify="center",
            )

            return render(
                request,
                "seo/serpCrawl.html",
                {
                    "form": form,
                    "serpDf": serpDf.to_html(
                        classes="table table-striped text-center", justify="center"
                    ),
                    "task_id": task_id.id,
                    "processing": True,
                    "domains_df": domains_df.to_json(orient="records"),
                    "rankDf": rank_df,
                },
            )

    else:
        # print(SERP_GOOG_VALID_VALS)
        form = SERPCrawl()
        return render(request, "seo/serpCrawl.html", {"form": form})


def seoAnalysis(request):
    form = SeoAnalyzeForm()
    hTitles = ["h1", "h2", "h3", "h4", "h6"]
    if request.method == "POST":
        form = SeoAnalyzeForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            group_id = request.COOKIES.get("socket_id", None)
            runCrawler.delay(group_id, url)
            return render(
                request, "seo/seoAnalysis.html", {"form": form, "processing": True}
            )
    else:
        return render(request, "seo/seoAnalysis.html", {"form": form})


def siteAudit(request):
    form = SeoAnalyzeForm()

    if request.method == "POST":
        form = SeoAnalyzeForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            group_id = request.COOKIES.get("socket_id", None)
            custom_settings = {
                "USER_AGENT": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
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
            crawlDf = crawl(
                url,
                output_file="output/seo_crawler.jl",
                follow_links=True,
                custom_settings=custom_settings,
            )

            logger.info("Socket Id" + group_id + " SEO crawl one complete")
            pages = pd.read_json("output/seo_crawler.jl", lines=True)

            url_list = pages["url"]
            # print(url_list)
            # print(url_list.to_list())

            url_df = url_to_df(urls=url_list)
            # print(url_df)

            robots_url = (
                url_df["scheme"][0] + "://" + url_df["netloc"][0] + "/robots.txt"
            )
            print(robots_url)
            # robotsTxtAn.delay(group_id,robots_url,url_list)

            # Review sitemap
            sitemap_url = (
                url_df["scheme"][0] + "://" + url_df["netloc"][0] + "/sitemap.xml"
            )
            print(sitemap_url)
            # sitemapAna.delay(group_id,sitemap_url,url_list)

            ## Creation of Columns based based on functionalities

            ### Word Count and text readability of the body text found in html generated content
            pages["word_count"] = pages["body_text"].apply(get_word_count)
            pages["readability"] = pages["body_text"].apply(text_readability)

            ### Create a seperate column with list of keywords and list of stopwords
            pages["keywords"] = pages["body_text"].apply(extract_keywords)
            keywords = pages["keywords"].sum()
            keywords = dict(Counter(keywords))

            pages["common_words"] = pages["body_text"].apply(extract_stopwords)
            common_words = pages["common_words"].sum()
            common_words = dict(Counter(common_words))

            # Get character counts of SEO desc , title
            pages["title"] = pages["title"].fillna(" ")
            pages["title_length"] = pages["title"].apply(len)

            missing_title = pages[(pages["title"].isna())]["url"].to_list()
            title_length = pages["title_length"].describe().to_dict()

            latency = pages["download_latency"].describe().to_dict()
            content_size = pages["size"].describe().to_dict()

            pages["meta_desc"] = pages["meta_desc"].fillna(" ")
            pages["desc_length"] = pages["meta_desc"].apply(len)

            missing_meta_desc = pages[(pages["meta_desc"].isna())]["url"].to_list()
            desc_length = pages["desc_length"].describe().to_dict()

            # check if canonical is equal to canonical link
            pages["canonical"] = pages["canonical"].fillna(" ")
            missing_canonical = pages[(pages["canonical"].isna())]["url"].to_list()
            pages["canonical_link"] = pages["url"] == pages["canonical"]
            condition1 = pages["canonical_link"] == False
            condition2 = pages["canonical"] != " "

            filtered_canonical = pages[condition1 & condition2]
            filtered_canonical = filtered_canonical[["url", "canonical"]]

            filtered_canonical_sim = pages[pages["canonical_link"] == True]
            filtered_canonical_sim = filtered_canonical_sim[["url", "canonical"]]

            broken_links = pages[(pages["status"] >= 400)]["url"].to_list()

            context = {
                "status": "success",
                "result": {
                    "audit": {
                        "body": {
                            "wordCount": pages["word_count"],
                            "readability": pages["readability"],
                            "keywords": keywords,
                            "commonWords": common_words,
                        },
                        "head": {
                            "meta_desc": {
                                "length_overview": desc_length,
                                "missing": {
                                    "urls": missing_meta_desc,
                                    "count": len(missing_meta_desc),
                                },
                            },
                            "title": {
                                "length_overview": title_length,
                                "missing": {
                                    "urls": missing_title,
                                    "count": len(missing_title),
                                },
                            },
                            "canonical": {
                                "missing": {
                                    "urls": missing_canonical,
                                    "count": len(missing_canonical),
                                },
                                "similar": {
                                    "values": filtered_canonical_sim.reset_index(
                                        drop=True
                                    ).to_dict(),
                                    "count": len(filtered_canonical_sim),
                                },
                                "different": {
                                    "values": filtered_canonical.reset_index(
                                        drop=True
                                    ).to_dict(),
                                    "count": len(filtered_canonical),
                                },
                            },
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
            return render(
                request,
                "seo/siteAudit.html",
                {"form": form, "processing": True, "context": context},
            )
    else:
        return render(request, "seo/siteAudit.html", {"form": form})


def siteAuditv2(request):
    form = SeoAnalyzeForm()
    hTitles = ["h1", "h2", "h3", "h4", "h6"]
    if request.method == "POST":
        form = SeoAnalyzeForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            group_id = request.COOKIES.get("socket_id", None)

            audit.delay(group_id, url)
            return render(
                request, "seo/siteAudit2.html", {"form": form, "processing": True}
            )
    else:
        return render(request, "seo/siteAudit2.html", {"form": form})


def industrySEO(request):
    form = IndustrySEO()
    if request.method == "POST":
        form = IndustrySEO(request.POST)
        if form.is_valid():
            url_list = form.cleaned_data["urls"].split("\n")
            group_id = request.COOKIES.get("socket_id", None)
            url_list = [url for url in url_list if validators.url(url)]
            # print(url_list)
            industry_research.delay(group_id, url_list)
            return render(
                request, "seo/industrySeoresearch.html", {"form": form, "processing": True}
            )
    else:
        return render(request, "seo/industrySeoresearch.html", {"form": form})

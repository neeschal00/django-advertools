from django.urls import path, include
from . import views

urlpatterns = [
    path("robots/", views.robotsToDf, name="robotsdf"),
    path("sitemap/", views.sitemapToDf, name="sitemapdf"),
    path("serp/", views.searchEngineResults, name="serp"),
    path("knowledge/", views.knowledgeGraph, name="know"),
    path("crawl/", views.carwlLinks, name="crawl"),
    path("serpCrawl/", views.serpCrawl, name="serp-crawl"),
    path("Analyze/", views.seoAnalysis, name="seo-analyze"),
    path("site-audit/", views.siteAudit, name="site-audit"),
    path("site-audit2/", views.siteAuditv2, name="site-audit2"),
    path("industry/research", views.industrySEO, name="industry-seo"),
]

from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from advertools import (
    url_to_df,
    emoji_search,
    extract_emoji,
    stopwords,
    word_frequency,
    extract_intense_words,
    extract_hashtags,
    extract_mentions,
    extract_numbers,
    extract_questions,
    extract_urls,
)
from .forms import (
    AnalyseUrls,
    EmojiSearch,
    EmojiExtract,
    TextAnalysis,
    DatasetExtract,
    DatasetSelect,
)
from .utils import url_structure
from .models import DatasetFile
import pandas as pd
from seo.tasks import generateReport, add


def analyseUrl(request):
    if request.method == "POST":
        form = AnalyseUrls(request.POST)
        if form.is_valid():
            urls = form.cleaned_data["urls"]
            urls = list(map(str.strip, urls.split("\n")))
            # urls = [url for url in urls if url.startswith("http","www")]

            decode = form.cleaned_data["decode"]

            df = url_to_df(urls=urls, decode=decode)

            figure = url_structure(df).to_html()

            return render(
                request,
                "analyse/anUrl.html",
                {
                    "form": form,
                    "figure": figure,
                    "urlsDf": df.to_html(
                        classes="table table-striped text-center", justify="center"
                    ),
                },
            )

    else:
        form = AnalyseUrls()
        return render(request, "analyse/anUrl.html", {"form": form})


def searchEmoji(request):
    if request.method == "POST":
        form = EmojiSearch(request.POST)
        if form.is_valid():
            emoji_text = form.cleaned_data["emoji_text"]

            df = emoji_search(emoji_text)

            return render(
                request,
                "analyse/emoji.html",
                {
                    "form": form,
                    "emojiDf": df.to_html(
                        classes="table table-striped text-center", justify="center"
                    ),
                },
            )

    else:
        form = EmojiSearch()
        return render(request, "analyse/emoji.html", {"form": form})


def extractEmoji(request):
    if request.method == "POST":
        form = EmojiExtract(request.POST)
        if form.is_valid():
            emoji_text = form.cleaned_data["emoji_text"]
            emoji_text = list(map(str.strip, emoji_text.split("\n")))
            df = extract_emoji(emoji_text)
            # print(df)
            df = pd.DataFrame.from_dict(df, orient="index")
            df = df.transpose()
            return render(
                request,
                "analyse/emojiExtract.html",
                {
                    "form": form,
                    "emojiDf": df.to_html(
                        classes="table table-striped text-center", justify="center"
                    ),
                },
            )

    else:
        form = EmojiExtract()
        return render(request, "analyse/emojiExtract.html", {"form": form})


def getStopWords(request):
    if request.method == "GET":
        stopwords_list = stopwords
        df = pd.DataFrame.from_dict(stopwords_list, orient="index")
        df = df.transpose()
        return render(
            request,
            "analyse/stopwords.html",
            {
                "df": df.to_html(
                    classes="table table-striped text-center", justify="center"
                )
            },
        )
    else:
        return HttpResponse("Ínvalid request Type")


def overviewText(request):
    if request.method == "POST":
        form = TextAnalysis(request.POST)
        if form.is_valid():
            valid_text = form.cleaned_data["valid_text"]
            valid_text = list(map(str.strip, valid_text.split("\n")))
            phrase_len = form.cleaned_data["phrase_len"]

            df = pd.DataFrame()
            if phrase_len:
                df = word_frequency(valid_text, phrase_len=phrase_len, extra_info=True)
            else:
                df = word_frequency(valid_text, extra_info=True)
            if not df.empty:
                generateReport.delay(df.to_json(), title="KText Overview profile")
            messages.success(request, "text Overview generated")

            # df = pd.DataFrame.from_dict(df,orient='index')
            # df = df.transpose()
            # jsonD = df.to_json
            return render(
                request,
                "analyse/textan.html",
                {
                    "form": form,
                    #  'json': jsonD,
                    "textDf": df.to_html(
                        classes="table table-striped text-center", justify="center"
                    ),
                },
            )

    else:
        form = TextAnalysis()
        return render(request, "analyse/textan.html", {"form": form})


def getDataset(request):
    if request.method == "POST":
        form = DatasetExtract(request.POST, request.FILES)
        # print(form)
        if form.is_valid():
            # print(form.cleaned_data)
            # form.save()
            data, created = DatasetFile.objects.get_or_create(**form.cleaned_data)
            # print(data)
            if created:
                messages.success(request, f"The dataset has been successfully added")
            else:
                messages.warning(
                    request,
                    f"The dataset {data.file_title}:{data.file_field} already exits.",
                )
            # print(df)
            # df = pd.DataFrame.from_dict(df,orient='index')
            # df = df.transpose()
            return redirect("datasetT")
        else:
            print(form.cleaned_data)
            return HttpResponse("form invalid")
    else:
        form = DatasetExtract()
        return render(request, "analyse/extraction.html", {"form": form})


def dataSetAnalysis(request):
    submission = False

    if request.method == "POST":
        form = DatasetSelect(request.POST)
        # print(form)
        if form.is_valid():
            form_data = form.cleaned_data

            dataset_val = form_data["file_title"]

            column_name = form_data["column_name"]
            try:
                df = pd.read_csv(dataset_val.file_field)
                listCol = df[column_name.strip()].to_list()

                urls = extract_urls(listCol)

                mentions = extract_mentions(listCol)

                questions = extract_questions(listCol)

                numbers = extract_numbers(listCol)

                hashtags = extract_hashtags(listCol)

                intense_words = extract_intense_words(
                    listCol, min_reps=3
                )  # minimum repertition of words 3

                submission = True

                return render(
                    request,
                    "analyse/analyzeText.html",
                    {
                        "form": form,
                        "textDf": df.to_html(
                            classes="table table-striped text-center", justify="center"
                        ),
                        "submission": submission,
                        "urls": urls,
                        "mentions": mentions,
                        "questions": questions,
                        "numbers": numbers,
                        "hashtags": hashtags,
                        "intense_words": intense_words,
                    },
                )
            except Exception as e:
                messages.warning(request, "Unable to analyze the particular column")
                return render(
                    request,
                    "analyse/analyzeText.html",
                    {
                        "form": form,
                    },
                )
        else:
            # print(form.cleaned_data)
            return HttpResponse("form invalid")
    else:
        form = DatasetSelect()
        return render(
            request,
            "analyse/analyzeText.html",
            {"form": form, "submission": submission},
        )

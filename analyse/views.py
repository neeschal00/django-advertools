from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect, JsonResponse
from advertools import url_to_df, emoji_search, extract_emoji, stopwords,word_frequency
from ydata_profiling import ProfileReport
from .forms import AnalyseUrls, EmojiSearch, EmojiExtract, TextAnalysis
from .utils import url_structure
import pandas as pd




def analyseUrl(request):
    if request.method == 'POST':
        form = AnalyseUrls(request.POST)
        if form.is_valid():
            
            urls = form.cleaned_data['urls']
            urls = list(map(str.strip,urls.split("\n")))

            decode = form.cleaned_data['decode']
            
            df = url_to_df(urls=urls,decode=decode)

            figure = url_structure(df).to_html()

            return render(request,'analyse/anUrl.html',{'form': form,'figure': figure,'urlsDf': df.to_html(classes='table table-striped text-center', justify='center')})

    else:
        form = AnalyseUrls()
        return render(request,'analyse/anUrl.html',{'form': form})



def searchEmoji(request):
    if request.method == 'POST':
        form = EmojiSearch(request.POST)
        if form.is_valid():
            
            emoji_text = form.cleaned_data['emoji_text']
           
            df = emoji_search(emoji_text)

            return render(request,'analyse/emoji.html',{'form': form,'emojiDf': df.to_html(classes='table table-striped text-center', justify='center')})

    else:
        form = EmojiSearch()
        return render(request,'analyse/emoji.html',{'form': form})


def extractEmoji(request):
    if request.method == 'POST':
        form = EmojiExtract(request.POST)
        if form.is_valid():
            
            emoji_text = form.cleaned_data['emoji_text']
            emoji_text = list(map(str.strip,emoji_text.split("\n")))
            df = extract_emoji(emoji_text)
            # print(df)
            df = pd.DataFrame.from_dict(df,orient='index')
            df = df.transpose()
            return render(request,'analyse/emojiExtract.html',{'form': form,'emojiDf': df.to_html(classes='table table-striped text-center', justify='center')})

    else:
        form = EmojiExtract()
        return render(request,'analyse/emojiExtract.html',{'form': form})


def getStopWords(request):
    if request.method == 'GET':
        stopwords_list = stopwords
        df = pd.DataFrame.from_dict(stopwords_list,orient='index')
        df = df.transpose()
        return render(request,'analyse/stopwords.html',{'df':df.to_html(classes='table table-striped text-center', justify='center')})
    else:
        return HttpResponse('Ínvalid request Type')


def analyzeText(request):
    if request.method == 'POST':
        form = TextAnalysis(request.POST)
        if form.is_valid():
            
            valid_text = form.cleaned_data['valid_text']
            valid_text = list(map(str.strip,valid_text.split("\n")))
            phrase_len = form.cleaned_data['phrase_len']
            if phrase_len:
                df = word_frequency(valid_text,phrase_len=phrase_len,extra_info=True)
            else:
                df = word_frequency(valid_text,extra_info=True)
            # print(df)
            # df = pd.DataFrame.from_dict(df,orient='index')
            # df = df.transpose()
            return render(request,'analyse/textan.html',{'form': form,'textDf': df.to_html(classes='table table-striped text-center', justify='center')})

    else:
        form = TextAnalysis()
        return render(request,'analyse/textan.html',{'form': form})





from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from advertools import ad_create, kw_generate, ad_from_string
from .forms import GenerateKeywords, DescriptionAds, LargeScaleAds

import pandas as pd


def generateDescription(request):
    if request.method == 'POST':
        form = DescriptionAds(request.POST)
        if form.is_valid():
            
            description_text = form.cleaned_data['description_text']
            slots = form.cleaned_data['slots']
            # print(slots)
            if slots:
                slots = list(map(str.strip,slots.split(",")))
                slots = list(map(float,slots))
                generateLargeAds = ad_from_string(description_text, slots=slots)
            else:
                slots = None
                generateLargeAds = generateLargeAds = ad_from_string(description_text)

            df = pd.DataFrame({
                'large_ads': generateLargeAds
            })

            return render(request,'generateAds/advertisement.html',{'form': form,'adsDf': df.to_html(classes='table table-striped text-center', justify='center')})

    else:
        form = DescriptionAds()
        return render(request,'generateAds/advertisement.html',{'form': form})


def generateAds(request):
    if request.method == 'POST':
        descriptive_form = DescriptionAds(request.POST or None)
        large_form =  LargeScaleAds(request.POST or None)

        if 'descriptive_form_submit' in request.POST:
            form = descriptive_form
            if form.is_valid():
            
                description_text = form.cleaned_data['description_text']
                slots = form.cleaned_data['slots']
                if slots:
                    slots = list(map(str.strip,slots.split(",")))
                    slots = list(map(float,slots))
                    generateLargeAds = ad_from_string(description_text, slots=slots)
                else:
                    slots = None
                    generateLargeAds = generateLargeAds = ad_from_string(description_text)

                df = pd.DataFrame({
                    'large_ads': generateLargeAds
                })

                return render(request,'generateAds/advertisement.html',{'descriptive_form': descriptive_form,'large_form':large_form,'adsDf': df.to_html(classes='table table-striped text-center', justify='center')})

        elif 'large_form_submit' in request.POST:
            form = large_form
            if form.is_valid():
                
                template = form.cleaned_data['template']
                capitalize = form.cleaned_data['capitalize']
                replacements = form.cleaned_data['replacements']
                replacements = list(map(str.strip,replacements.split(",")))
                max_len = form.cleaned_data['max_len']
                # print(max_len)
                # print(type(max_len))
                fallback = form.cleaned_data['fallback']

                if max_len:
                    try:
                        generateLargeAds = ad_create(template=template,
                                                    replacements=replacements,
                                                    capitalize=capitalize,
                                                    fallback=fallback, max_len=max_len)
                    except ValueError:
                        messages.error(request,'The template + fallback should be <= '+str(max_len)+' if available')
                        return redirect('advertisement')
                else:
                    generateLargeAds = ad_create(template=template,
                                                replacements=replacements,
                                                capitalize=capitalize,
                                                fallback=fallback,max_len= len(template)+5)
                
                df = pd.DataFrame({
                    'large_ads': generateLargeAds
                })

                return render(request,'generateAds/advertisement.html',{'descriptive_form': descriptive_form,'large_form':large_form,'adsDf': df.to_html(classes='table table-striped text-center', justify='center')})
        

    else:
        descriptive_form = DescriptionAds()
        large_form =  LargeScaleAds()
        return render(request,'generateAds/advertisement.html',{'descriptive_form': descriptive_form,'large_form':large_form})


def generate(request, products=['jack'],max_length=100,fallback='Great Cities'):
    if request.is_ajax() and request.method == "POST":
        template = json.loads(request.POST.get('template'))
        products = json.loads(request.POST.get('products'))
        ads_gen = ad_create(template=template,
                replacements=products,
                max_len=30,
                fallback='Great Cities')
        return JsonResponse(
            {
                "success":True,
                "result": ads_gen 
            }
        )
    else:
        return JsonResponse(
            {
                "sucess":False,
                "result": "Invalid request" 
            }
        )


def generateKeywords(request):
    if request.method == 'POST':
        form = GenerateKeywords(request.POST)
        if form.is_valid():
            
            product = form.cleaned_data['product']
            word = form.cleaned_data['word']
            products = list(map(str.strip,product.split(",")))
            words = list(map(str.strip,word.split(",")))
            
            keywordDf = kw_generate(products,words)

            return render(request,'generateAds/keywords.html',{'form': form,'keywordDf': keywordDf.to_html(classes='table table-striped text-center', justify='center')})

    else:
        form = GenerateKeywords()
        return render(request,'generateAds/keywords.html',{'form': form})



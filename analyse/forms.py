from django import forms

class AnalyseUrls(forms.Form):
    urls = forms.CharField(widget=forms.Textarea(attrs={"rows": 10, 
    "cols": 40,
    "placeholder": "Enter urls in new lines like  \nhttp://localhost:8000/generate/advertisement/large/\nhttps://importsem.com/create-a-custom-twitter-tweet-alert-system-with-python/"
    }
    ))

    decode = forms.BooleanField(required=False)


class EmojiSearch(forms.Form):
    emoji_text = forms.CharField(widget=forms.TextInput(attrs={
    "placeholder":'Enter Emoji you want to view like "vegetable" '
    }
    ))

class EmojiExtract(forms.Form):
    emoji_text = forms.CharField(widget=forms.Textarea(attrs={"rows": 10, 
    "cols": 40,
    "placeholder":'Enter text you want to extract emoji from in new lines like\nI am grinning 😀\nA grinning cat 😺\nhello! 😀😀😀 💛💛\nJust text'
    }
    ))


class TextAnalysis(forms.Form):
    valid_text = forms.CharField(widget=forms.Textarea(attrs={"rows": 7, 
    "cols": 40,
    "placeholder":'Enter text you want to analyze if seperately seperate it in new lines like\nI am grinning 😀\nA grinning cat 😺\nhello! 😀😀😀 💛💛\nJust text'
    }
    ))

    phrase_len = forms.IntegerField(max_value=10,required=False)




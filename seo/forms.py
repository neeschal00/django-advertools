from django import forms

class RobotsTxt(forms.Form):
    urls = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, 
    "cols": 40,
    "placeholder": "Enter robots.txt urls in new lines like  \nhttps://www.amazon.com/robots.txt\nhttps://twitter.com/robots.txt"
    }
    ))


class Sitemap(forms.Form):
    urls = forms.CharField(widget=forms.TextInput(attrs={
    "placeholder": "Enter sitemap .xml urls in new lines like https://www.bbc.com/sitemaps/https-sitemap-com-archive-1.xml"
    }
    ))

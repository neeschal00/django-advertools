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


class MultiSelectFormField(forms.MultipleChoiceField):
    widget = forms.SelectMultiple

    def clean(self, value):
        if not value and self.required:
            raise forms.ValidationError("This field is required.")
        return value







class SerpGoogle(forms.Form):

    GL_Choices = (
        ('np', "NP"),
        ("us", "US"),
        ("in", "IN"),
    )

    query = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, 
    "cols": 40,
    "placeholder": "Enter the search query(seperate with ',' if multiple)"
    }
    ))

    geolocation = forms.MultipleChoiceField(choices=GL_Choices, widget=forms.CheckboxSelectMultiple())

    country = forms.CharField(widget=forms.Textarea(attrs={"rows": 2, 
    "cols": 40,
    "placeholder": "Enter the geolocation for end user like\nnp,in,us"
    }
    ),required=False)


class KnowledgeG(forms.Form):

    query = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, 
    "cols": 40,
    "placeholder": "Enter the search query(seperate with ',' if multiple)"
    }
    ))

    languages = forms.CharField(widget=forms.Textarea(attrs={"rows": 2, 
    "cols": 40,
    "placeholder": "Enter the languages for end user like\nen,es,de"
    }
    ),required=False)


class Crawl(forms.Form):
    links = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, 
    "cols": 40,
    "placeholder": "Enter the urls you want to crawl in new line"
    }
    ))

    follow_links = forms.BooleanField(required=False)

    headers_only = forms.BooleanField(required=False)



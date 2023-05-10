from django import forms
from advertools import SERP_GOOG_VALID_VALS
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div



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

    GL_Choices = ((gl,gl) for gl in SERP_GOOG_VALID_VALS['gl'])
    CR_Choices = ((cr,cr) for cr in SERP_GOOG_VALID_VALS['cr'])

    query = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, 
    "cols": 40,
    "placeholder": "Enter the search query(seperate with ',' if multiple)"
    }
    ))

    geolocation = forms.MultipleChoiceField(required=False,choices=GL_Choices, widget=forms.CheckboxSelectMultiple(attrs={'class':'gl-checkbox'}))

    country = forms.MultipleChoiceField(required=False,choices=GL_Choices, widget=forms.CheckboxSelectMultiple(attrs={'class':'cr-checkbox'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Div('geolocation', css_class='form-group'),
            Div('country', css_class='form-group'),
            Submit('submit', 'Submit', css_class='btn btn-primary')
        )
    
    

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



from django import forms
from advertools import SERP_GOOG_VALID_VALS
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django_select2.forms import Select2MultipleWidget





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








class SerpGoogle(forms.Form):

    GL_Choices = ((gl,gl) for gl in SERP_GOOG_VALID_VALS['gl'])
    CR_Choices = ((cr,cr) for cr in SERP_GOOG_VALID_VALS['cr'])

    query = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, 
    "cols": 40,
    "placeholder": "Enter the search query(seperate with ',' if multiple)"
    }
    ))

    geolocation = forms.MultipleChoiceField(required=False,choices=GL_Choices, widget=Select2MultipleWidget)

    country = forms.MultipleChoiceField(required=False,choices=CR_Choices, widget=Select2MultipleWidget)

    # def __init__(self, *args, **kwargs):
    #     super(SerpGoogle, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_id = 'serp-google'
    #     self.helper.form_method = 'post'
    #     self.helper.form_class = 'form-horizontal'
    #     self.helper.label_class = 'col-sm-3'
    #     self.helper.field_class = 'col-sm-9'
    #     self.helper.layout = Layout(
    #         Fieldset(
    #             'query'
    #             'Select options',
    #             'geolocation',
    #         ),
    #         Submit('submit', 'Submit', css_class='btn-primary')
        # )
    
    

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



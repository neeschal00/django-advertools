from django import forms
from advertools import SERP_GOOG_VALID_VALS
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Div
from django_select2.forms import Select2MultipleWidget


class RobotsTxt(forms.Form):
    urls = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "cols": 40,
                "placeholder": "Enter robots.txt urls in new lines like  \nhttps://www.amazon.com/robots.txt\nhttps://twitter.com/robots.txt",
            }
        )
    )


class Sitemap(forms.Form):
    urls = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 2,
                "cols": 40,
                "placeholder": "Enter sitemap .xml url like https://www.bbc.com/sitemaps/https-sitemap-com-archive-1.xml",
            }
        )
    )


class SerpGoogle(forms.Form):
    GL_Choices = ((gl, gl) for gl in SERP_GOOG_VALID_VALS["gl"])
    CR_Choices = ((cr, cr) for cr in SERP_GOOG_VALID_VALS["cr"])
    LR_Choices = ((lr, lr) for lr in SERP_GOOG_VALID_VALS["lr"])
    Rights_Choices = ((rights, rights) for rights in SERP_GOOG_VALID_VALS["rights"])

    query = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "cols": 40,
                "placeholder": "Enter the search query(seperate with ',' if multiple)",
                "help_text": "Query you want to get results for",
            }
        )
    )

    geolocation = forms.MultipleChoiceField(
        required=False,
        choices=GL_Choices,
        widget=Select2MultipleWidget(attrs={"class": "select2 col-md-4"}),
    )

    country = forms.MultipleChoiceField(
        required=False,
        choices=CR_Choices,
        widget=Select2MultipleWidget(attrs={"class": "select2 col-md-4"}),
    )

    language = forms.MultipleChoiceField(
        required=False,
        choices=LR_Choices,
        widget=Select2MultipleWidget(attrs={"class": "select2 col-md-4"}),
    )

    rights = forms.MultipleChoiceField(
        required=False,
        choices=Rights_Choices,
        widget=Select2MultipleWidget(attrs={"class": "select2 col-md-4"}),
    )

    def __init__(self, *args, **kwargs):
        super(SerpGoogle, self).__init__(*args, **kwargs)
        self.fields[
            "geolocation"
        ].help_text = '<span class="text-sm">geolocation of end user</span>'
        self.fields[
            "country"
        ].help_text = '<span class="text-sm">restrict result originating in a particular country</span>'
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div("query"),
            Div(
                Div("geolocation", css_class="col-md-6 mr-2"),
                Div("country", css_class="col-md-6 mr-2"),
                Div("language", css_class="col-md-6 mr-2"),
                Div("rights", css_class="col-md-6 mr-2"),
                css_class="row",
            ),
            Submit("submit", "Submit", css_class="mt-2 btn"),
        )


class KnowledgeG(forms.Form):
    # LR_Choices = ((lr.split("_")[1],lr.split("_")[1]) for lr in SERP_GOOG_VALID_VALS['lr'])

    query = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "cols": 40,
                "placeholder": "Enter the search query(seperate with ',' if multiple) like flights,tickets,barley",
            }
        )
    )

    languages = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 2,
                "cols": 40,
                "placeholder": "Enter the languages for end user like\nen,es,de",
            }
        ),
        required=False,
    )

    limit = forms.IntegerField(required=False, min_value=1)


class Crawl(forms.Form):
    links = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "cols": 40,
                "placeholder": "Enter the urls you want to crawl in new line",
            }
        )
    )

    follow_links = forms.BooleanField(
        required=False, help_text="Crawl all reachable links from page"
    )

    headers_only = forms.BooleanField(required=False)

    pg_count = forms.IntegerField(
        required=False, min_value=1, max_value=10000, help_text="max crawlable pages"
    )


class SERPCrawl(SerpGoogle):
    limit = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Enter the limit"}
        ),
        help_text="Limit the number of urls you want to crawl",
    )

    headers_only = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout[1].append("limit")
        self.helper.layout[1].append("headers_only")


class SeoAnalyzeForm(forms.Form):
    url = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter the URL to analyze"}))

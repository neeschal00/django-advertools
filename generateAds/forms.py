from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class DescriptionAds(forms.Form):
    description_text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "cols": 30,
                "placeholder": "Add the descriptive text to generate Ads from",
            }
        )
    )

    slots = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Add slots like 46,78,98"})
    )

    def __init__(self, *args, **kwargs):
        super(DescriptionAds, self).__init__(*args, **kwargs)
        self.fields["slots"].required = False


class LargeScaleAds(forms.Form):
    template = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "cols": 30,
                "placeholder": "Add the templates to generate adds for like \n 5-star Hotels in {}",
            }
        )
    )

    replacements = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "cols": 30,
                "placeholder": "Add replacements values such as Kathmandu,New-York,New-Delhi",
            }
        )
    )

    fallback = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Add fallback value 'great cities'"}
        )
    )

    capitalize = forms.BooleanField(required=False)
    max_len = forms.IntegerField(required=False)


class GenerateKeywords(forms.Form):
    product = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "cols": 30,
                "placeholder": 'Enter the products you want to generate keywords for seperated by "," like\nshoes,shirt,scarf',
            }
        )
    )
    word = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "cols": 30,
                "placeholder": 'Enter the words you want to generate keywords for seperated by "," like\nbuy,cheap,quality,premium',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(GenerateKeywords, self).__init__(*args, **kwargs)
        self.fields["product"].help_text = 'Please add the Input seperated by "," '
        self.fields["word"].help_text = 'Please add the Input seperated by "," '
        # self.fields['products'].widget.attrs['placeholder'] = 'Enter the products you want to generate keywords for seperated by "," like\nshoes,shirt,scarf'
        # self.fields['word'].widget.attrs['placeholder'] = 'Enter the words you want to generate keywords for seperated by "," like\nbuy,cheap,quality,premium'
        self.helper = FormHelper()
        self.helper.add_input(
            Submit("Generate KeyWords", "Generate Keywords", css_class="btn-secondary")
        )
        self.helper.form_method = "POST"

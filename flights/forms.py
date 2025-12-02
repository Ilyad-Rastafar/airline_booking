from django import forms

class SearchForm(forms.Form):
    origin = forms.CharField(required=False)
    destination = forms.CharField(required=False)
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
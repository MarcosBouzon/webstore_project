from django import forms
from django.forms.fields import CharField

class SearchForm(forms.Form):
    search = forms.CharField(max_length=20)
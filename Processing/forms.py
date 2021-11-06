from django import forms

class ConvertForm(forms.Form):
    file = forms.FileField()
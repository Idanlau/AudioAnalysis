from django import forms

class ConvertForm(forms.Form):
    file = forms.FileField()
    file.widget.attrs.update({'class': 'form-control'})
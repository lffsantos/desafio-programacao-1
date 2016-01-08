from django import forms
__author__ = 'lucas'


class UploadForm(forms.Form):
    file = forms.FileField(label='Selecione um Arquivo', widget=forms.FileInput(attrs={'style' : 'float:left;', 'class': 'form-control'}))



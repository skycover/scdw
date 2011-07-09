from django import forms

class SelectPathForm(forms.Form):
    source = forms.CharField(max_length=250, label='Source path')

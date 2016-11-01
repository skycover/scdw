# -*- coding: utf-8 -*-

from django import forms

class SelectPathForm(forms.Form):
    source = forms.CharField(max_length=500, label='Source path', widget=forms.TextInput(attrs={'size': '60'}))

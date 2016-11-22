from django import forms
from django.utils.translation import ugettext as _


from bprofile.bprofile import list_keys


class NewBackupForm(forms.Form):
    name = forms.CharField(max_length=30, label=_('Short name'))
    source = forms.CharField(
        max_length=250, label=_('Source path'), widget=forms.HiddenInput
    )

    def clean_name(self):
        import re
        name = self.cleaned_data.get('name', '')
        # check for alnum
        if not re.search(r'^[a-zA-Z--_]+$', name):
            raise forms.ValidationError("Invalid characters in name")

        return name

    def clean_source(self):
        import os
        source = self.cleaned_data.get('source', '')
        # cheeck for real path
        if os.path.exists(source):
            return source
        else:
            raise forms.ValidationError(
                "File or directory not found: '%s'" % source)


class ConfigureBackupForm(forms.Form):
    name = forms.CharField(
        max_length=30, label=_('Short name'), widget=forms.HiddenInput
    )
    source = forms.CharField(
        max_length=250, label=_('Source path'), widget=forms.HiddenInput
    )
    descr = forms.CharField(
        required=False, label=_('Description')
    )
    notes = forms.CharField(
        required=False, label=_('Notes'), widget=forms.Textarea
    )
    conf = forms.CharField(
        required=False, label=_('Config'),
        widget=forms.Textarea(attrs={'rows': 20, 'cols': 100})
    )

    def clean_name(self):
        import re
        name = self.cleaned_data.get('name', '')
        # check for alnum
        if not re.search(r'^[a-zA-Z--_]+$', name):
            raise forms.ValidationError("Invalid characters in name")

        return name

    def clean_source(self):
        import os
        source = self.cleaned_data.get('source', '')
        # cheeck for real path
        if os.path.exists(source):
            return source
        else:
            raise forms.ValidationError(
                "File or directory not found: '%s'" % source)


class AddExceptionForm(forms.Form):
    source = forms.CharField(
        max_length=500, widget=forms.TextInput(attrs={'size': '60'})
    )


class GlobalConfigForm(forms.Form):
    conf = forms.CharField(
        label=_('Global config'),
        widget=forms.Textarea(attrs={'rows': 30, 'cols': 120})
    )


class QuickSettingsForm(forms.Form):
    password = forms.CharField(
        required=False, max_length=250, label='GPG_PW',
        widget=forms.TextInput(attrs={'size': '60'})
    )
    key = forms.ChoiceField(
        required=False, label='GPG_KEY',
        choices=[('', "<don't use key>")] + list_keys()
    )
    target = forms.CharField(
        required=False, max_length=500, label='TARGET',
        widget=forms.TextInput(attrs={'size': '60'})
    )


class PrePostForm(forms.Form):
    """ pre/post form """
    pre = forms.CharField(
        required=False, label='PRE',
        widget=forms.Textarea()
    )
    post = forms.CharField(
        required=False, label='POST',
        widget=forms.Textarea()
    )

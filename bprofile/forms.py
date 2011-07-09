from django import forms

class NewBackupForm(forms.Form):
    name = forms.CharField(max_length=30, label='Short name')
    source = forms.CharField(max_length=250, label='Source path', widget=forms.HiddenInput)
    
    def clean_name(self):
        import os, re
        from views import find_confhome
        name = self.cleaned_data.get('name','')
        # check for alnum
        if not re.search(r'^[a-zA-Z--_]+$', name):
            raise forms.ValidationError("Invalid characters in name")

        return name

    def clean_source(self):
        import os
        source = self.cleaned_data.get('source','')
        # cheeck for real path
        if os.path.exists(source):
            return source
        else:
            raise forms.ValidationError("File or directory not found: '%s'" % source)

class ConfigureBackupForm(forms.Form):
    name = forms.CharField(max_length=30, label='Short name', widget=forms.HiddenInput)
    source = forms.CharField(max_length=250, label='Source path', widget=forms.HiddenInput)
    descr = forms.CharField(required=False, label='Description')
    notes = forms.CharField(required=False, label='Notes', widget=forms.Textarea)
    conf = forms.CharField(required=False, label='Config', widget=forms.Textarea(attrs={'rows': 20, 'cols': 100}))
    
    def clean_name(self):
        import os, re
        from views import find_confhome
        name = self.cleaned_data.get('name','')
        # check for alnum
        if not re.search(r'^[a-zA-Z--_]+$', name):
            raise forms.ValidationError("Invalid characters in name")

        return name

    def clean_source(self):
        import os
        source = self.cleaned_data.get('source','')
        # cheeck for real path
        if os.path.exists(source):
            return source
        else:
            raise forms.ValidationError("File or directory not found: '%s'" % source)

class AddExceptionForm(forms.Form):
    source = forms.CharField(max_length=250)

class GlobalConfigForm(forms.Form):
    conf = forms.CharField(label='Global config', widget=forms.Textarea(attrs={'rows': 30, 'cols': 120}))

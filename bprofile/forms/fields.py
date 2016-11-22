from django import forms
from django.utils.translation import ugettext as _


class FolderField(forms.CharField):
    def __init__(self, dontCheck=True, *args, **kwargs):
        self.dc = dontCheck
        super(FolderField, self).__init__(*args, **kwargs)

    @staticmethod
    def checkDestination(value='/'):
        import os
        return os.path.exists(os.path.join('/', *value.split('/')))

    def clean(self, value):
        pass


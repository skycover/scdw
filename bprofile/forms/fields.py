from django import forms
from bprofile.bprofile import list_keys
from django.utils.translation import ugettext as _
from django.core.validators import RegexValidator
from widgets import MaxAgeWidget


class MaxAgeField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (
            forms.IntegerField(required=False),
            forms.CharField(required=False, max_length=1),
        )
        widget = MaxAgeWidget
        super(MaxAgeField, self).__init__(
            fields=fields, require_all_fields=False, widget=widget,
            *args, **kwargs
        )

    def compress(self, data_list):
        return None if data_list[0] is None else \
            ''.join([unicode(v) for v in data_list])

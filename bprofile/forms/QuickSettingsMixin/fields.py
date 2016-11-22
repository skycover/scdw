from django import forms
from django.utils.translation import ugettext as _
from widgets import MaxAgeWidget, SFTPTargetWidget


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


class SFTPTargetField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (
            forms.CharField(label=_('host')),
            forms.IntegerField(required=False, label=_('port')),
            forms.CharField(label=_('path'))
        )
        widget = SFTPTargetWidget()
        super(SFTPTargetField, self).__init__(
            fields=fields, require_all_fields=False, widget=widget,
            *args, **kwargs
        )

    def compress(self, data_list):
        ret = 'sftp://' + unicode(data_list[0])
        if data_list[1]:
            ret += ':' + unicode(data_list[1])
        ret += '//' + unicode(data_list[2])
        return ret


class FileTargetField(forms.CharField):

    def to_python(self, value):
        return value.replace('file://', '')


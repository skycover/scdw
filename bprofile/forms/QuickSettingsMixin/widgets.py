from django import forms
from django.utils.translation import ugettext as _


TIMECHOISE = [
    ('s', _('seconds')),
    ('m', _('minutes')),
    ('h', _('hours')),
    ('D', _('days')),
    ('W', _('weeks')),
    ('M', _('months')),
    ('Y', _('years'))
]


class MaxAgeWidget(forms.MultiWidget):
    def __init__(self, *args, **kwargs):

        _widgets = (
            forms.NumberInput(attrs={'size': '4'}),
            forms.Select(choices=TIMECHOISE)
        )
        super(MaxAgeWidget, self).__init__(_widgets, *args, **kwargs)

    def decompress(self, value):
        import re
        if value:
            try:
                return [
                    re.search('^[0-9]+', value).group(),
                    re.search('[smhDWMY]$', value).group(),
                ]
            except AttributeError:
                return ['', '']
        else:
            return ['', '']


class SFTPTargetWidget(forms.MultiWidget):
    STR_STARTS = ['sftp', 'scp', 'ssh']

    def __init__(self, *args, **kwargs):
        _widgets = (
            forms.TextInput(),
            forms.NumberInput(),
            forms.TextInput(),
        )
        _widgets[1].attrs['required'] = False
        print _widgets[1].attrs
        super(SFTPTargetWidget, self).__init__(_widgets, *args, **kwargs)

    def decompress(self, value):
        try:
            t, url = value.split('://', 1)
            full_host, path = url.split('//', 1)
            temp = full_host.split('@')
            if len(temp) == 2:
                host_port = temp[1]
            else:
                host_port = temp[0]
            temp = host_port.split(':')
            host = temp[0]
            if len(temp) == 2:
                port = temp[1]
            else:
                port = None
            return [
                host, port, path
            ]
        except:
            return [None, None, None]



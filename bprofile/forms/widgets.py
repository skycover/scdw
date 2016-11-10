from django import forms
from bprofile.bprofile import list_keys
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
    def __init__(self, attrs=None, val=''):

        _widgets = (
            forms.NumberInput(attrs={'size': '4'}),
            forms.Select(choices=TIMECHOISE)
        )
        super(MaxAgeWidget, self).__init__(_widgets, attrs)

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

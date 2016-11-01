# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms


class DateWidget(forms.TextInput):

    class Media:
        js = ('/static/js/jquery-3.1.1.min.js',
              '/static/js/jquery.datetimepicker.full.min.js',
              '/static/js/datetimewidget.js',)
        css = {
            'all': ('/static/css/jquery.datetimepicker.css',)
        }

    def __init__(self, attrs={}, *args, **kwargs):
        attrs = attrs.copy()
        attrs['class'] = 'DateWidget'
        attrs['size'] = attrs.get('size', '10')
        super(DateWidget, self).__init__(attrs=attrs, *args, **kwargs)


class DateTimeWidget(forms.TextInput):

    class Media:
        js = ('/static/js/jquery-3.1.1.min.js',
              '/static/js/jquery.datetimepicker.full.min.js',
              '/static/js/datetimewidget.js')
        css = {
            'all': ('/static/css/jquery.datetimepicker.css',)
        }

    def __init__(self, attrs={}, *args, **kwargs):
        attrs = attrs.copy()
        attrs['class'] = 'DateTimeWidget'
        attrs['size'] = attrs.get('size', '20')
        super(DateTimeWidget, self).__init__(attrs=attrs, *args, **kwargs)


class TimeWidget(forms.TextInput):

    class Media:
        js = ('/static/js/jquery-3.1.1.min.js',
              '/static/js/jquery.datetimepicker.full.min.js',
              '/static/js/datetimewidget.js')
        css = {
            'all': ('/static/css/jquery.datetimepicker.css',)
        }

    def __init__(self, attrs={}, *args, **kwargs):
        attrs = attrs.copy()
        attrs['class'] = 'TimeWidget'
        attrs['size'] = attrs.get('size', '10')
        super(TimeWidget, self).__init__(attrs=attrs, *args, **kwargs)


class DateForm(forms.Form):
    date = forms.DateTimeField(
        widget=DateTimeWidget, label='Date'
    )

    def clean(self):
        from time import mktime
        data = super(DateForm, self).clean()
        return int(mktime(data['date'].timetuple()))


class PathForm(forms.Form):
    path = forms.CharField(
        label='Restore path', max_length=500,
        widget=forms.TextInput(attrs={'size': '60'})
    )

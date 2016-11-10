from django import forms
from django.utils.translation import ugettext as _
from bprofile.forms.QuickSettingsFormNew import FORM_LIST


class MailForm(forms.Form):
    MAIL_FROM = forms.CharField(
        label=_('MAIL_FROM'),
    )
    MAIL_TO = forms.CharField()
    MAIL_SUBJ = forms.CharField()
    MAIL_CMD = forms.CharField()
    MAIL_VERBOSE = forms.ChoiceField(
        choices=(
            (0, _('only errors')),
            (1, _('warnings and errors')),
            (2, _('everything'))
        )
    )


class TargetSFTP(forms.Form):
    host = forms.CharField()
    username = forms.CharField()
    port = forms.IntegerField()
    path = forms.CharField()


FORM_LIST['mail'] = MailForm
FORM_LIST['target_sftp'] = TargetSFTP
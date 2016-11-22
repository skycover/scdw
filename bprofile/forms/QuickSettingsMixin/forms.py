from django import forms
from django.utils.translation import ugettext as _
from bprofile.forms.QuickSettingsFormNew import FORM_LIST
from bprofile.bprofile import list_keys
from fields import SFTPTargetField, FileTargetField


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
    TARGET = SFTPTargetField()
    TARGET_USER = forms.CharField()
    TARGET_PASS = forms.CharField()


class TargetFile(forms.Form):
    TARGET = FileTargetField()


class GPG_key(forms.Form):
    GPG_KEY = forms.ChoiceField(
        choices=list_keys() + [('disable', 'message'), ],
    )
    GPG_PW = forms.CharField(
        required=False
    )


class GPG_pw(forms.Form):
    GPG_PW = forms.CharField()


FORM_LIST['mail'] = MailForm
FORM_LIST['target_sftp'] = TargetSFTP
FORM_LIST['target_scp'] = TargetSFTP
FORM_LIST['target_file'] = TargetFile
FORM_LIST['gpg_key'] = GPG_key
FORM_LIST['gpg_pw'] = GPG_pw

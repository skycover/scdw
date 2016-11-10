from django import forms
from django.utils.translation import ugettext as _
from bprofile.forms.fields import MaxAgeField

TARGET_TYPES = [
    ('file', _('Local storage')),
    ('ftp', _('FTP')),
    ('hsi', _('HSI')),
    ('cf+http', _('Cloud Files')),
    # ('imap', _('')),
    # ('imaps', _('')),
    # ('rsync', _('')),
    # ('s3', _('')),
    # ('s3+http', _('')),
    # ('scp', _('')),
    # ('sftp', _('')),
]

FORM_LIST = dict()


class QuickSettingsFormBase(forms.Form):
    """ New QuickSettings"""
    """ gpg settings """
    use_gpg = forms.ChoiceField(
        label=_('Use GPG?'), choices=[
            ('no', _('No')),
            ('key', _('Use key')),
            ('password', _('Use passphrase'))
        ]
    )
    """ mail section """
    use_mail = forms.ChoiceField(
        label=_('Use Mail?'), choices=[
            ('no', _('No')),
            ('yes', _('Yes')),
        ]
    )
    """ target section """
    TARGET = forms.ChoiceField(
        label=_('Target'), help_text=_('Choose target type'),
        choices=TARGET_TYPES,
    )

    """ bkpsection """
    MAX_AGE = MaxAgeField(
        label=_('MAX_AGE'), required=False
    )
    MAX_FULL_BACKUPS = forms.IntegerField(
        label=_('MAX_FULL_BACKUPS'), required=False,
    )
    MAX_FULLBKP_AGE = MaxAgeField(
        label=_('MAX_FULLBKP_AGE'), required=False,
    )
    VOLSIZE = forms.IntegerField(
        label=_('VOLSIZE'), help_text=_('in MB'),
        required=False
    )
    AUTOPURGE = forms.ChoiceField(
        choices=(
            ('', _('Don\'t Use')),
            ('FULL', _('Use purge by FULL')),
            ('AGE', _('Use purge by AGE')),
        )
    )

    def clean(self):
        val = super(QuickSettingsFormBase, self).clean()
        ret = {
            k: v for k, v in val.items()
            if not (v is None or k in ('use_gpg', 'use_mail'))
        }
        if val.get('use_gpg') == 'no':
            ret['GPW_KEY'] = 'disabled'
        return ret


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
    ('sftp', _('sftp')),
]

FORM_LIST = dict()


def intersect(a, b):
    """
    Finds the intersection of two dictionaries.

    A key and value pair is included in the result only if the key exists in
    both given dictionaries. Value is taken from
    the second dictionary.
    """

    return dict(filter(lambda (x, y): x in a, b.items()))


class MixinForm(object):

    def _iterate_over_instances(self, method_name, *args, **kwargs):
        all_classes = type(self).__mro__
        results = []

        for cls in all_classes[1:2] + all_classes[3:-3]:
            # Temporary set values
            # self.instance = instance
            # self._meta = meta
            ret = getattr(super(MixinForm, cls), method_name)(*args, **kwargs)
            # print cls, ret
            results.append(ret)

        # Restore original values
        # self.instance = original_instance
        # self._meta = original_meta

        return results

    def clean(self):
        # We traverse in reverse order to keep in sync with get_declared_fields
        ret = reversed(self._iterate_over_instances('clean'))
        return reduce(
            intersect, ret
        )

    def _post_clean(self):
        self._iterate_over_instances('_post_clean')


class QuickSettingsFormBase(MixinForm, forms.Form):
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
    use_type = forms.ChoiceField(
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
            (None, _('Don\'t Use')),
            ('FULL', _('Use purge by FULL')),
            ('AGE', _('Use purge by AGE')),
        ), required=False
    )

    def clean(self):
        val = forms.Form.clean(self)
        ret = {
            k: v for k, v in val.items()
            if not k.startswith('use_')
        }
        if val.get('use_gpg') == 'no':
            ret['GPW_KEY'] = 'disabled'
        return ret

    def _post_clean(self):
        return forms.Form._post_clean(self)



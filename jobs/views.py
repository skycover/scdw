# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required()
def ListFiles(request, profile, restore=False, to=False):
    from bprofile.bprofile import list_conf, read_bprofile, find_confhome
    from forms import DateForm, PathForm
    if profile not in list_conf():
        return HttpResponseRedirect('/')
    context = {
        'profile': read_bprofile(find_confhome(), profile),
        'dateform': DateForm(),
        'restore': restore,
    }
    if restore:
        from bprofile.bprofile import encode, decode
        from django.core.urlresolvers import reverse
        from forms import PathForm
        context['pathform'] = PathForm(
            {'path': decode(to) if to else '/'}
        )
        context['action_url'] = encode(
            reverse('RestoreFiles', args=(profile,))
            if to else reverse('RestoreFiles', args=(profile, ))[:-1]
        )
        context['to'] = {
            'decoded': decode(to) if to else '/',
            'encoded': to if to else encode('/'),
        }
    return render(request, 'jobs/file_list.html', context)

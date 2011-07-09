# Create your views here.
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from forms import *
import base64

def encode(s):
    return base64.b64encode(s)

def decode(s):
    return base64.b64decode(s)

def list_files(path):
    import os

    flist = []
    for f in os.listdir(path):
        ffull = os.path.join(path, f)
        ff = {'type': '', 'encoded': encode(ffull), 'decoded': f }
        if os.path.isdir(ffull):
              ff['type'] = '+'
        flist.append(ff)
    return flist

def split_path(pth, pl = []):
    import os
    (fp, fn) = os.path.split(pth)
    if fn:
        return split_path(fp, pl + [{'encoded': encode(pth), 'decoded': fn,}])
    else:
        pl.reverse()
        return pl
    
def filelist(request, **kwargs):
    import logging
    import re, os
    from django.conf import settings

    ae = kwargs['action']
    pe = kwargs['path']
    pd = decode(pe)

    targs = {
        'action': {'encoded': ae, 'decoded': decode(ae)},
        'path': {'encoded': pe, 'decoded': pd},
        'path_list': split_path(pd),
        'root': {'encoded': encode('/'), 'decoded': '/'},
        'file_list': list_files(decode(pe)),
    }

    if (request.method == 'POST') and ('submit' in request.POST):
        select_path_form = SelectPathForm(request.POST)
        if select_path_form.is_valid():
            cd = select_path_form.cleaned_data
            if os.path.isdir(cd['source']):
                return HttpResponseRedirect('/filelist/%s/%s/' % (ae, encode(cd['source'])))
    else:
        select_path_form = SelectPathForm(initial={'source': pd})

    targs['select_path_form'] = select_path_form
    return direct_to_template(request, 'filelist/filelist.html', targs)

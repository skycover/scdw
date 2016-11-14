# -*- coding: utf-8 -*-

# The SkyCover Duply Web - the web interface for scduply/duplicity.
# Copyright (C) 2011 Dmitry Chernyak
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Create your views here.
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from forms import *

from bprofile.bprofile import encode, decode


def list_files(path, dirsOnly=False):
    import os

    flist = []
    dirlist = [
        d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))
    ] if dirsOnly else os.listdir(path)
    for f in dirlist:
        ffull = os.path.join(path, f)
        ff = {'type': '', 'encoded': encode(ffull), 'decoded': f}
        if os.path.isdir(ffull):
              ff['type'] = '+'
        flist.append(ff)
    flist.sort()
    return flist


def split_path(pth, pl=[]):
    import os
    (fp, fn) = os.path.split(pth)
    if fn:
        return split_path(fp, pl + [{'encoded': encode(pth), 'decoded': fn,}])
    else:
        pl.reverse()
        return pl


def filelist(request, **kwargs):
    import os

    ae = kwargs['action']
    pe = kwargs['path']
    dirsOnly = kwargs.get('dirsOnly', False)
    pd = decode(pe)
    home = os.path.expanduser('~')

    targs = {
        'action': {'encoded': ae, 'decoded': decode(ae)},
        'path': {'encoded': pe, 'decoded': pd},
        'path_list': split_path(pd),
        'root': {'encoded': encode('/'), 'decoded': '/'},
        'home': {'encoded': encode(home)},
        'documents': {'encoded': encode(home)},
        'file_list': list_files(decode(pe), dirsOnly),
        'dirsOnly': dirsOnly,
        'p_url': 'ListDirs' if dirsOnly else 'ListFiles'
    }

    if request.method == 'POST' and 'submit' in request.POST:
        select_path_form = SelectPathForm(request.POST)
        if select_path_form.is_valid():
            cd = select_path_form.cleaned_data
            if os.path.isdir(cd['source']):
                return HttpResponseRedirect(
                    reverse(
                        'ListDirs' if dirsOnly else 'ListFiles',
                        args=(ae, encode(cd['source'].encode('utf8')))
                    )
                )
    else:
        select_path_form = SelectPathForm(initial={'source': pd})

    targs['select_path_form'] = select_path_form
    return render(request, 'filelist/filelist.html', targs)

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
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import (
    NewBackupForm, ConfigureBackupForm, AddExceptionForm, GlobalConfigForm,
    QuickSettingsForm
)
from .bprofile import (
    encode, scduply_init, find_confhome, enum_profiles,
    read_bprofile, add_exclude, decode, write_exclude,
    write_bprofile, create_bprofile, read_gconf,
    write_gconf, list_keys, write_qconf, read_qconf,
)


@login_required()
def init_backend(request, **kwargs):
    targs = {}
    if (request.method == 'POST') and ('submit' in request.POST):
        ret = scduply_init()
        if ret:
            targs['init_error'] = ret
        else:
            return HttpResponseRedirect('/')

    return render(request, 'bprofile/init.html', targs)


@login_required()
def list_bprofiles(request, **kwargs):
    confhome = find_confhome()
    if confhome:
        targs = {
            'confhome': confhome,
            'bprofiles': enum_profiles(confhome),
            'path_new': encode('select folder or file'),
        }

        return render(request, 'bprofile/list.html', targs)
    else:
        return HttpResponseRedirect('/init/')


@login_required()
def delete_bprofile(request, **kwargs):
    name = kwargs['name']
    return render(request, 'bprofile/delete.html', {'name': name})


@login_required()
def show_bprofile(request, **kwargs):
    from bprofile import list_conf
    from django.http import HttpResponseNotFound
    confhome = find_confhome()
    name = kwargs['name']
    if name not in list_conf():
        return HttpResponseRedirect('/')
    pr = read_bprofile(confhome, name)
    targs = {
        'confhome': confhome,
        'profile': pr,
        'action_show': encode('/show/%s' % name),
        'source_enc': encode(pr['source']),
        'exclude_enc': [
            {'plain': e, 'encoded': encode(e)} for e in pr['exclude']
        ]
    }
    
    if request.method == 'POST':
        add_exception_form = AddExceptionForm(request.POST)
        if add_exception_form.is_valid():
            cd = add_exception_form.cleaned_data
            if 'submit_add_plus' in request.POST:
                ret = add_exclude(
                    confhome, pr, cd['source'].encode('utf8'), '+'
                )
            elif 'submit_add_minus' in request.POST:
                ret = add_exclude(
                    confhome, pr, cd['source'].encode('utf8'), '-'
                )
            if ret:
                targs['exception_error'] = ret
            else:
                return HttpResponseRedirect('/show/%s/' % name)
    else:
        excpt_enc = kwargs.get('excpt_enc')
        if excpt_enc:
            excpt = decode(excpt_enc)
            if excpt.startswith(pr['source']):
                excpt = excpt[len(pr['source'])+1:]
            else:
                excpt = ""
                targs['exception_error'] = \
                    'Selected path is not under the backup path'
        else:
            excpt = ""
        add_exception_form = AddExceptionForm(
            initial={'source': excpt}
        )

    targs['add_exception_form'] = add_exception_form
    return render(request, 'bprofile/show.html', targs)


@login_required()
def excl_action(request, **kwargs):
    name = kwargs['name']
    action = kwargs['action']
    excl = decode(kwargs['excpt_enc'])
    confhome = find_confhome()
    pr = read_bprofile(confhome, name)
    if action == 'rem':
        pr['exclude'].remove(excl)
        write_exclude(confhome, pr)
    if action == 'up':
        i = pr['exclude'].index(excl)
        if i > 0:
            pr['exclude'].remove(excl)
            pr['exclude'].insert(i-1, excl)
        write_exclude(confhome, pr)
    if action == 'down':
        i = pr['exclude'].index(excl)
        l = len(pr['exclude'])
        if (l > 1) and (i < l-1):
            pr['exclude'].remove(excl)
            pr['exclude'].insert(i+1, excl)
        write_exclude(confhome, pr)

    return HttpResponseRedirect('/show/%s/' % name)


@login_required()
def edit_bprofile(request, **kwargs):
    confhome = find_confhome()
    name = kwargs['name']
    pr = read_bprofile(confhome, name)
    targs = {
        'confhome': confhome,
        'action_new': encode('/edit/'+name),
        'profile': pr,
        'source_enc': encode(pr['source']),
    }

    if (request.method == 'POST') and ('submit' in request.POST):
        conf_backup_form = ConfigureBackupForm(request.POST)
        if conf_backup_form.is_valid():
            cd = conf_backup_form.cleaned_data
            write_bprofile(confhome, cd)
            return HttpResponseRedirect('/show/%s/' % name)
        else:
            targs['conf_backup_error'] = "Saving failed"
    else:
        conf_backup_form = ConfigureBackupForm(
            initial={'source': pr['source'],
                     'name': name,
                     'descr': pr['descr'],
                     'notes': pr['notes'],
                     'conf': pr['conf'],
            })

    targs['conf_backup_form'] = conf_backup_form
    return render(request, 'bprofile/edit.html', targs)


@login_required()
def new_bprofile(request, **kwargs):
    import os
    from django.conf import settings

    confhome = find_confhome()
    source = decode(kwargs['source_enc'])
    if os.path.exists(source):
        source_enc = kwargs['source_enc']
    else:
        source_enc = encode('/')
    targs = {
        'confhome': confhome,
        'action_new': encode('/new'),
        'source': source,
        'source_enc': source_enc,
    }

    if (request.method == 'POST') and ('submit' in request.POST):
        new_backup_form = NewBackupForm(request.POST)
        if new_backup_form.is_valid():
            cd = new_backup_form.cleaned_data
            # check for the already configured profile
            if os.path.isfile(
                    os.path.join(confhome, cd['name'], 'source')):
                targs['new_backup_error'] = \
                    "Profile '%s' already exists" % cd['name']
            else:
                ret = create_bprofile(confhome, cd['name'], cd['source'])
                if ret:
                    targs['create_backup_error'] = ret
                else:
                    return HttpResponseRedirect('/show/%s/' % cd['name'])
    else:
        new_backup_form = NewBackupForm(initial={'source': source})

    targs['new_backup_form'] = new_backup_form
    return render(request, 'bprofile/new.html', targs)


@login_required()
def edit_conf(request, **kwargs):
    confhome = find_confhome()
    pr = read_gconf(confhome)
    targs = {
        'confhome': confhome,
    }

    if (request.method == 'POST') and ('submit' in request.POST):
        global_conf_form = GlobalConfigForm(request.POST)
        if global_conf_form.is_valid():
            cd = global_conf_form.cleaned_data
            write_gconf(confhome, cd['conf'])
            return HttpResponseRedirect('/')
        else:
            targs['global_conf_error'] = "Saving failed"
    else:
        global_conf_form = GlobalConfigForm(
            initial={'conf': read_gconf(confhome),
        })

    targs['global_conf_form'] = global_conf_form
    return render(request, 'bprofile/edit_conf.html', targs)


@login_required()
def edit_quick(request, **kwargs):
    confhome = find_confhome()
    pr = read_gconf(confhome)
    keys = list_keys()
    targs = {
        'confhome': confhome,
    }

    if (request.method == 'POST') and ('submit' in request.POST):
        quick_settings_form = QuickSettingsForm(request.POST)
        if quick_settings_form.is_valid():
            cd = quick_settings_form.cleaned_data
            write_qconf(confhome, cd)
            return HttpResponseRedirect('/')
        else:
            targs['quick_settings_error'] = "Saving failed"
    else:
        quick_settings_form = QuickSettingsForm(initial=read_qconf(confhome),)

    targs['quick_settings_form'] = quick_settings_form
    return render(request, 'bprofile/gqconf.html', targs)


@login_required()
def show_log(request, **kwargs):
    from subprocess import check_output
    targs = {
        'logstuff': unicode(check_output(
            ("zcat", decode(kwargs['log_enc']))
        ), encoding='utf-8', errors='replace'),
        'name': kwargs['name'],
        'type': kwargs['type'],
        'date': kwargs['date'],
    }

    return render(request, 'bprofile/log.html', targs)


def pre_post(request, profile):
    from forms import PrePostForm
    from bprofile import (
        read_bprofile, find_confhome, getPrePostForProfile, setPrePostForProfile
    )
    targs = {
        'profile': read_bprofile(find_confhome(), profile),
    }
    if request.method == 'GET':
        form = PrePostForm(getPrePostForProfile(profile))
        targs['form'] = form
    if request.method == 'POST':
        form = PrePostForm(request.POST)
        if form.is_valid():
            setPrePostForProfile(profile, form.cleaned_data)
        targs['form'] = form

    return render(request, 'bprofile/pre_post.html', targs)

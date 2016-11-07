# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import (
    JsonResponse, HttpResponseNotFound, HttpResponseRedirect,
    HttpResponse, HttpResponseServerError
)
from django.contrib.auth.decorators import login_required


@login_required()
def AllJobsStatusAjax(request):
    from bprofile.bprofile import list_conf, read_bprofile, find_confhome
    return JsonResponse({
        job: {
            name: value
            for name, value in read_bprofile(find_confhome(), job).items()
        } for job in list_conf()
    })


@login_required()
def JobStatusAjax(request, job):
    from bprofile.bprofile import list_conf, read_bprofile, find_confhome
    return JsonResponse({
            name: value
            for name, value in read_bprofile(find_confhome(), job).items()
        }) \
        if job in list_conf() else HttpResponseNotFound('There is such profile')


@login_required()
def StartBKPALLAjax(request):
    from scduply import scduply_command
    if request.method == 'POST':
        scduply_command('bkpall')
        return HttpResponse()
    else:
        return HttpResponseRedirect('/')


@login_required()
def StartBackupAjax(request, profile, full=None):
    from scduply import scduply_command
    from bprofile.bprofile import list_conf
    if profile not in list_conf():
        return HttpResponseNotFound('there is no such profile')
    if request.method == 'POST':
        scduply_command(profile, 'backup' if not full else 'pre_full_post')
        return HttpResponse()
    else:
        return HttpResponseRedirect('/show/%s/' % profile)


@login_required()
def ListFilesAjax(request, profile):
    from scduply import file_tree, scduply_files
    from bprofile.bprofile import list_conf
    from forms import DateForm
    if profile not in list_conf():
        HttpResponseNotFound('there is no such profile')
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            return JsonResponse(
                file_tree(scduply_files(profile, form.cleaned_data)),
                safe=False
            )
    return JsonResponse(file_tree(scduply_files(profile)), safe=False)


@login_required()
def StartRestoreAjax(request, profile):
    from bprofile.bprofile import list_conf
    from json import loads
    from scduply import scduply_command
    from forms import DateForm
    if profile not in list_conf():
        HttpResponseNotFound('there is no such profile')
    if request.method == 'POST':
        job = loads(request.body)
        try:
            form = DateForm({'date': job['date']})
            if form.is_valid():
                try:
                    date = form.cleaned_data
                except:
                    date = 'now'
                params = ['fetch', job['file'], job['restore_path'], date] \
                    if job['file'] else [
                    'restore', '"%s"' % job['restore_path'], date
                ]
            else:
                HttpResponseServerError('some error')
        except:
            params = ['fetch', job['file'], job['restore_path']] \
                if job['file'] else ['restore', job['restore_path']]
        scduply_command(profile, *params)
    return JsonResponse({'status': 'OK'})
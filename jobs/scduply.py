# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone


def is_running(profile):
    """check task for running"""
    import os
    import sys
    hostname = os.uname()[1]
    path = os.path.join(
        os.getenv('HOME'), '.cache', 'duplicity', profile
    )
    try:
        pids_list = [
            int(f.split('.')[1]) for f in os.listdir(path) if f.startswith(hostname)
        ]
    except OSError:
        pids_list = []
    if not sys.platform == 'cygwin':
        for pid in pids_list:
            try:
                os.kill(pid, 0)
                return True
            except OSError:
                try:
                    os.remove(
                        os.path.join(path, "%s.%s" % (hostname, pid))
                    )
                except: pass

        else:
            return False
    else:
        from commands import getoutput
        output = getoutput(
            'ps aux|awk \'/python/ {print $1}\''
        ).split('\n')
        if not output[1] == '':
            for opid in output:
                for pid in pids_list:
                    if str(pid).startswith(opid):
                        return True
            else: return False
    return pids_list


def scduply_command(*args):
    import subprocess
    import os
    with open(os.devnull, 'r+b', 0) as DEVNULL:
        p = subprocess.Popen(
            ['scduply'] + [a for a in args],
            stdin=DEVNULL, stdout=DEVNULL,
            stderr=DEVNULL,
        )
        return p


def scduply_files(profile, date='now'):
    from commands import getoutput
    from bprofile.bprofile import list_conf
    from datetime import datetime as dt
    if profile not in list_conf():
        return []
    output = unicode(getoutput(
        'scduply %s list %s|egrep ":[0-6][0-9] [0-9]{4} .*"' % (
            profile, date
        )
    ), encoding='utf8')
    return [
        (dt.strptime(s[:24], '%c'), s[25:])
        for s in output.split('\n') if not s[25:] == '.'
    ]


def file_tree(file_list):
    import os
    ret = []
    counter = 0
    id_dict = dict()
    for date, path in file_list:
        counter += 1
        p = path.split('/')
        id_dict[path] = 'ajson%s' % counter
        ret.append({
            'id': 'ajson%s' % counter,
            'text': p[-1],
            'parent': '#' if len(p) == 1 else id_dict[os.path.join(*p[:-1])]
        })
    return ret


def folder_tree(*args):
    import os
    ret = [
        {
            'text': f, 'child': True
        } for f in os.listdir(os.path.join('/', *args))
        if os.path.isdir(os.path.join('/', *args) + '/' + f)
    ]
    return ret
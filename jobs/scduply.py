# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def __escape_from_virtualenv():
    import os
    env = os.environ.copy()
    if env.get('VIRTUAL_ENV'):
        env['PATH'] = ':'.join(
            f for f in env['PATH'].split(':')
            if not f.startswith(env['VIRTUAL_ENV'])
        )
        del env['VIRTUAL_ENV']
    return env


def is_running(profile):
    """ check task for running """
    import os
    platform, hostname = os.uname()[:2]
    path = os.path.join(
        os.getenv('HOME'), '.cache', 'duplicity', profile
    )
    try:
        pids_list = [
            f.split('.')[1]
            for f in os.listdir(path) if f.startswith(hostname)
        ] if not platform.lower().startswith('cygwin') else [
            f.split('.')[1].split('-')[0]
            for f in os.listdir(path) if f.startswith(hostname)
        ]
    except OSError:
        pids_list = []
    for pid in pids_list:
        try:
            os.kill(int(pid), 0)
            return True
        except OSError:
            pass

    else:
        return False


def scduply_command(*args):
    import os
    import subprocess
    # double fork magic
    try:
        pid = os.fork()
    except OSError, e:
        raise Exception, "%s [%d]" % (e.strerror, e.errno)
    if pid == 0:
        os.setsid()
        try:
            newpid = os.fork()
            if newpid == 0:
                subprocess.Popen(
                    ('scduply',) + args,
                    env=__escape_from_virtualenv(),
                    preexec_fn=os.setpgrp, close_fds=True
                )
        except OSError, e:
            raise Exception, "%s [%d]" % (e.strerror, e.errno)


def scduply_output(*args):
    import subprocess
    output = subprocess.check_output(
        ('scduply', ) + args,
        env=__escape_from_virtualenv()
    )
    return unicode(output, encoding='utf-8')


def scduply_files(profile, date='now'):
    from bprofile.bprofile import list_conf
    from datetime import datetime as dt
    from re import search
    try:
        return [
            (dt.strptime(l[:24], '%c'), l[25:])
            for l in scduply_output(profile, 'list', date).split('\n')
            if search(
                r'^[A-Z][a-z]{2} [A-Z][a-z]{2}[ ]{1,2}[0-9]{1,2} [0-9:]{8}',
                l
            ) and not l[25:] == '.'
        ] if profile in list_conf() else []
    except ValueError:
        return []


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
    return [
        {
            'text': f, 'child': True
        } for f in os.listdir(os.path.join('/', *args))
        if os.path.isdir(os.path.join('/', *args) + '/' + f)
    ]


def scduply_backupdates(profile):
    from re import search, split
    from datetime import datetime as dt
    from bprofile.bprofile import list_conf
    return [
        (lambda x, y: (x, dt.strptime(y, '%c')))(*split('[ ]{3,}', f)[1:-1])
        for f in scduply_output(profile, 'status').split('\n')
        if search(r'[0-9]{4}[ \t]+[0-9]+$', f) and len(split('[ ]+', f)) == 8
    ] if profile in list_conf() else []

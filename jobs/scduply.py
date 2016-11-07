# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def is_running(profile):
    """check task for running"""
    import os
    platform, hostname = os.uname()[:2]
    path = os.path.join(
        os.getenv('HOME'), '.cache', 'duplicity', profile
    )
    try:
        pids_list = [
            f.split('.')[1]
            for f in os.listdir(path) if f.startswith(hostname)
        ]
    except OSError:
        pids_list = []
    if not platform == 'cygwin':
        for pid in pids_list:
            try:
                os.kill(int(pid), 0)
                return True
            except OSError:
                try:
                    os.remove(
                        os.path.join(path, "%s.%s" % (hostname, pid))
                    )
                except IOError:
                    pass

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
            else:
                return False
    return pids_list


def scduply_command(*args):
    import os
    import subprocess
    env = os.environ.copy()
    env['PATH'] = '/usr/local/bin:/usr/bin:/bin'
    try:
        pid = os.fork()
    except OSError, e:
        raise Exception, "%s [%d]" % (e.strerror, e.errno)

    if pid == 0:
        os.setsid()
        try:
            pid == os.fork()
        except OSError, e:
            raise Exception, "%s [%d]" % (e.strerror, e.errno)
    subprocess.Popen(
        ('scduply',) + args,
        env=env, preexec_fn=os.setpgrp, close_fds=True
    )


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
    try:
        return [
            (dt.strptime(s[:24], '%c'), s[25:])
            for s in output.split('\n') if not s[25:] == '.'
        ]
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
    ret = [
        {
            'text': f, 'child': True
        } for f in os.listdir(os.path.join('/', *args))
        if os.path.isdir(os.path.join('/', *args) + '/' + f)
    ]
    return ret

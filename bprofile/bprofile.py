# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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


def encode(s):
    import base64
    try:
        return base64.b64encode(
            s.encode('utf-8')
        ).replace('+', '-').replace('/', '_')
    except:
        return base64.b64encode(s).replace('+', '-').replace('/', '_')


def decode(s):
    import base64
    m = s.replace('-', '+').replace('_', '/')
    try:
        return unicode(base64.b64decode(m), encoding='utf-8')
    except:
        return base64.b64decode(m)


def find_confhome():
    import os
    home = os.path.expanduser('~')
    if os.getuid() == 0 and os.path.isfile('/etc/scduply/conf'):
        return '/etc/scduply'
    elif os.path.isfile(os.path.join(home, '.scduply', 'conf')):
        return os.path.join(home, '.scduply')
    else:
        return None


def scduply_init():
    import commands
    (status, output) = commands.getstatusoutput("scduply init")
    if status > 0:
        return output
    else:
        return None


def scduply_create(name):
    import commands
    (status, output) = commands.getstatusoutput("scduply %s create" % name)
    if status > 0:
        return output
    else:
        return None


def nicedate(d):
    from datetime import datetime
    import pytz
    from jobs.const import TIMEZONE
    uu = datetime.strptime(d, '%Y%m%dT%H%M%SZ').replace(tzinfo=pytz.UTC)
    dd = uu.astimezone(TIMEZONE)
    return dd.strftime('%Y-%m-%d %H:%M:%S')


def read_logs(confhome, name):
    import os

    # XXX some ugly euristics
    if confhome == '/etc/scduply':
        logdir = os.path.join('/var/log/scduply', name)
    else:
        logdir = os.path.join(confhome, 'log', name)

    full = ''
    fullf = ''
    inc = ''
    incf = ''
    err = ''
    errf = ''
    if os.path.exists(logdir):
        for f in [l for l in os.listdir(logdir)
                  if l.startswith('duplicity-log.')
                  or l.startswith('duplicity-cmdlog-pre_full_post.')]:
            m = f.split('.')
            d = m[-2]
            if m[1] == 'err':
                if err < d:
                    err = d
                    errf = f
            elif m[-3] == 'to':
                if inc < d:
                    inc = d
                    incf = f
            else:
                if full < d:
                    full = d
                    fullf = f
        
        if inc < full:
            inc = ''
            incf = ''
        if full:
            full = nicedate(full)
            fullf = encode(os.path.join(logdir, fullf))
        if inc:
            inc = nicedate(inc)
            incf = encode(os.path.join(logdir, incf))
        if err:
            err = nicedate(err)
            errf = encode(os.path.join(logdir, errf))

    return {'full': (full, fullf), 'inc': (inc, incf), 'err': (err, errf)}

        
def read_bprofile(confhome, name):
    import os
    from codecs import open
    from jobs.scduply import is_running
    confdir = os.path.join(confhome, name)
    srcfile = os.path.join(confdir, 'source')
    dscfile = os.path.join(confdir, 'descr')
    cnffile = os.path.join(confdir, 'conf')
    excfile = os.path.join(confdir, 'exclude')
    lockfile = os.path.join(
        os.getenv('HOME'), '.cache', 'duplicity', name, 'lockfile.lock'
    )
    if os.path.isdir(confdir) and os.path.isfile(srcfile):
        f = open(srcfile, 'r')
        try:
            ff = {
                'name': name,
                'source': unicode(f.readline().strip(), encoding='utf-8')
            }
        except:
            ff = {'name': name, 'source': f.readline().strip(), }

        ff['source']
        f.close()
        f = open(cnffile, 'r', encoding='utf-8')
        ff['conf'] = f.read()
        f.close()
        try:
            f = open(excfile, 'r', encoding='utf-8')
            ff['exclude'] = [
                s.strip() for s in f.readlines()
                if s.strip() != ''
            ]
            f.close()
        except:
            ff['exclude'] = []
        try:
            f = open(dscfile, 'r', encoding='utf-8')
            ff['descr'] = f.readline().strip()
            ff['notes'] = f.read()
            f.close()
        except:
            ff['descr'] = ''
            ff['notes'] = ''

        ff['logs'] = read_logs(confhome, name)
        ff['locking'] = os.path.exists(
            lockfile
        )
        ff['running'] = is_running(name)
        return ff
    else:
        return None


def create_bprofile(confhome, name, source):
    import os
    from codecs import open
    confdir = os.path.join(confhome, name)
    if not os.path.isdir(confdir):
        ret = scduply_create(name)
        if ret:
            return ret
        if not os.path.isdir(confdir):
            return "scduply hasn't created profile in %s' % confdir"
    f = open(os.path.join(confdir, "source"), 'w', encoding='utf-8')
    f.write(source+'\n')
    f.close()
    return None


def write_bprofile(confhome, cd):
    import os
    confdir = os.path.join(confhome, cd['name'])
    if not os.path.isdir(confdir):
        return "Profile not found in %s'" % confdir
    write_safe(os.path.join(confdir, "conf"),
        cd.get(
            'conf',
            "# Empty config file. Use global settings.\n"
        ).replace('\r', ''))
    write_safe(os.path.join(confdir, "source"),
        cd['source']+'\n')
    if cd.get('exclude'):
        write_exclude(confhome, cd)
    write_safe(os.path.join(confdir, "descr"),
        cd.get('descr', '')+'\n'+cd.get('notes', '').replace('\r', ''))


def write_safe(fname, data):
    import os
    from codecs import open
    ftemp = fname + '.tmp'
    f = open(ftemp, 'w', encoding='utf-8')
    f.write(data)
    f.close()
    os.rename(ftemp, fname)


def write_exclude(confhome, profile):
    import os
    # XXX possibly race when the user is mad ;)
    write_safe(
        os.path.join(confhome, profile['name'], 'exclude'),
        '\n'.join(profile['exclude'])+'\n'
    )


def add_exclude(confhome, profile, source, sign):
    if source == '**':
        src = '**'
    else:
        src = "%s/%s" % (profile['source'], unicode(source, encoding='utf-8'))
    if sign:
        s = "%s %s" % (sign, src)
    else:
        s = src
    profile['exclude'].append(s)
    return write_exclude(confhome, profile)


def enum_profiles(confhome):
    import os

    blist = []
    for f in os.listdir(confhome):
        ff = read_bprofile(confhome, f)
        if ff:
            blist.append(ff)
    return blist


def read_gconf(confhome):
    import os

    cnffile = os.path.join(confhome, 'conf')
    if os.path.isfile(cnffile):
        f = open(cnffile, 'r')
        ff = f.read()
        f.close()
        return ff
    else:
        return ''


def write_gconf(confhome, conf):
    import os
    write_safe(os.path.join(confhome, 'conf'), conf.replace('\r', ''))


def list_keys():
    from subprocess import check_output
    res = []
    for l in check_output(("gpg", "--list-secret-keys")).split('\n'):
        m = l.split()
        # XXX here is some strange bug under CygWin:
        # If I use "m" instead of "len(m)>0" then "m" evaluates to False
        # But if I write "print m", or simple "pass" before the "if" statement
        # Then "m" becames True and all goes fine
        if len(m) > 0:
            if m[0] == 'sec':
                key = m[1].split('/')[1]
                date = m[2]
            elif m[0] == 'uid':
                uid = ' '.join(m[1:])
                res.append([key, "%s (%s, %s)" % (key, date, uid)])
    return res


def read_qconf(confdir):
    import os
    res = {}
    qcnffile = os.path.join(confdir, 'conf.scdw')
    if os.path.isdir(confdir) and os.path.isfile(qcnffile):
        f = open(qcnffile, 'r')
        for l in [s.strip() for s in f.readlines()]:
            m = l.split("='")
            if m:
                if m[0] == 'TARGET':
                    res['target'] = m[1].strip("'")
                elif m[0] == 'GPG_KEY':
                    res['key'] = m[1].strip("'")
                elif m[0] == 'GPG_PW':
                    res['password'] = m[1].strip("'")
        f.close()
    return res


def read_qconf_new(confdir):
    import os
    res = {}
    qcnffile = os.path.join(confdir, 'conf.scdw')
    if os.path.isdir(confdir) and os.path.isfile(qcnffile):
        f = open(qcnffile, 'r')
        for l in [s.strip() for s in f.readlines()]:
            m = l.split("=")
            res[m[0]] = m[1].replace('\'', '').replace('\"', '')
        f.close()
    return res


def write_qconf(confdir, qconf):
    import os
    qcnffile = os.path.join(confdir, 'conf.scdw')
    s=''
    if qconf.get('target'):
        s += "%s='%s'\n" % ('TARGET', qconf.get('target'))
    if qconf.get('key'):
        s += "%s='%s'\n" % ('GPG_KEY', qconf.get('key'))
    if qconf.get('password'):
        s += "%s='%s'\n" % ('GPG_PW', qconf.get('password'))
    write_safe(qcnffile, s)


def get_consolecodepage():
    from commands import getoutput
    from sys import platform
    codepage = 'utf-8'
    exclude_list = {
        '65001': 'utf-8'
    }
    if platform == 'cygwin':
        output = getoutput('cmd /c chcp')
        console_codepage = output[:-1].split(' ')[-1]
        codepage = exclude_list.get(console_codepage, 'cp%s' % console_codepage)
    return codepage


def list_conf():
    import os
    home = find_confhome()
    ret = [
        d for d in os.listdir(home)
        if os.path.isdir(os.path.join(home, d)) and not d == 'log' and
        os.path.exists(os.path.join(home, d, 'conf'))
    ]
    return ret


def write_qconf_new(confdir, qconf={}):
    import os
    qcnffile = os.path.join(confdir, 'conf.scdw')
    s = ''
    for key, val in qconf.items():
        s += u"%s=%s\n" % (key, val)
    write_safe(qcnffile, s)

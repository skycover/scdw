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

from urlenc import encode, decode

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

def read_bprofile(confhome, name, full = True):
    import os

    confdir = os.path.join(confhome, name)
    srcfile = os.path.join(confdir, 'source')
    dscfile = os.path.join(confdir, 'descr')
    cnffile = os.path.join(confdir, 'conf')
    excfile = os.path.join(confdir, 'exclude')
    if os.path.isdir(confdir) and os.path.isfile(srcfile):
        f = open(srcfile, 'r')
        ff = {'name': name, 'source': f.readline().strip(), }
        f.close()
        f = open(cnffile, 'r')
        ff['conf'] = f.read()
        f.close()
        try:
            f = open(excfile, 'r')
            ff['exclude'] = [s.strip() for s in f.readlines() if s.strip() != '']
            f.close()
        except:
            ff['exclude']=[]
        try:
            f = open(dscfile, 'r')
            ff['descr'] = f.readline().strip()
            ff['notes']=f.read()
            f.close()
        except:
            ff['descr'] = ''
            ff['notes']=''
        return ff
    else:
        return None

def create_bprofile(confhome, name, source):
    import os
    confdir = os.path.join(confhome, name)
    if not os.path.isdir(confdir):
        ret = scduply_create(name)
        if ret:
            return ret
        if not os.path.isdir(confdir):
            return "scduply hasn't created profile in %s' % confdir"
    f = open(os.path.join(confdir, "source"),'w')
    f.write(source+'\n')
    f.close()
    return None

def write_bprofile(confhome, cd):
    import os
    confdir = os.path.join(confhome, cd['name'])
    if not os.path.isdir(confdir):
        return "Profile not found in %s'" % confdir
    write_safe(os.path.join(confdir, "conf"),
        cd.get('conf',"# Empty config file. Use global settings.\n").replace('\r',''))
    write_safe(os.path.join(confdir, "source"),
        cd['source']+'\n')
    if cd.get('exclude'):
        write_exclude(confhome, cd)
    write_safe(os.path.join(confdir, "descr"),
        cd.get('descr','')+'\n'+cd.get('notes','').replace('\r',''))

def write_safe(fname, data):
    import os
    ftemp = fname+'.tmp'
    f = open(ftemp, 'w')
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
        src = "%s/%s" % (profile['source'], source)
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
        ff = read_bprofile(confhome, f, False)
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
    write_safe(os.path.join(confhome, 'conf'), conf.replace('\r',''))

def list_keys():
    from commands import getoutput
    res = []
    for l in getoutput("gpg --list-secret-keys").split('\n'):
        m = l.split()
        if m:
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
        for l in [ s.strip() for s in f.readlines() ]:
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

def write_qconf(confdir,qconf):
    import os
    from bprofile import write_safe
    qcnffile = os.path.join(confdir, 'conf.scdw')
    s=''
    if qconf.get('target'):
        s+="%s='%s'\n" % ('TARGET', qconf.get('target'))
    if qconf.get('key'):
        s+="%s='%s'\n" % ('GPG_KEY', qconf.get('key'))
    if qconf.get('password'):
        s+="%s='%s'\n" % ('GPG_PW', qconf.get('password'))
    write_safe(qcnffile, s)

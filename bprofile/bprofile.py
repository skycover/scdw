# -*- coding: utf-8 -*-

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

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
            ff['exclude'] = [s.strip() for s in f.readlines() ]
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
    f = open(os.path.join(confdir, "conf"),'w')
    f.write(cd.get('conf',"# Empty config file. Use global settings.\n"))
    f.close()
    f = open(os.path.join(confdir, "source"),'w')
    f.write(cd['source']+'\n')
    f.close()
    f = open(os.path.join(confdir, "exclude"),'w')
    f.write('\n'.join(cd.get('exclude',[])))
    f.close()
    f = open(os.path.join(confdir, "descr"),'w')
    f.write(cd.get('descr','')+'\n')
    f.write(cd.get('notes',''))
    f.close()

def write_exclude(confhome, profile):
    import os
    # XXX possibly race when the user is mad ;)
    ef = os.path.join(confhome, profile['name'], 'exclude')
    eftemp = ef+'.tmp'
    f = open(eftemp, 'w')
    f.write('\n'.join(profile['exclude']))
    f.close()
    os.rename(eftemp, ef)
    return None

def add_exclude(confhome, profile, source, sign):
    profile['exclude'].append("%s%s/%s" % (sign, profile['source'], source))
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
    cnffile = os.path.join(confhome, 'conf')
    f = open(cnffile,'w')
    f.write(conf)
    f.close()

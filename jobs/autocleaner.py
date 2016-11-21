# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from threading import Thread
from time import sleep


def cleanProfile(profile):
    from bprofile.bprofile import find_confhome
    import os
    import re
    path = os.path.join(find_confhome(), 'log', profile)
    files = [
        f for f in os.listdir(path)
        if not re.search(
            r"duplicity-(cmdlog-(fetch|restore)|log.(ok|err)|report|status)",
            f
        )
    ]
    for f in files:
        try:
            os.remove(os.path.join(path, f))
        except:
            pass


class ProfileCleaner(Thread):

    def __init__(self):
        super(ProfileCleaner, self).__init__()
        self.setDaemon(True)
        self.start()

    def run(self):
        from bprofile.bprofile import list_conf
        while True:
            for profile in list_conf():
                cleanProfile(profile)
            sleep(120)

cleaner = ProfileCleaner()

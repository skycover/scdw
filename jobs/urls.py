from django.conf.urls import url, include
from views import (
    JobStatusAjax, AllJobsStatusAjax, StartBKPALLAjax, StartBackupAjax,
    ListFiles, ListFilesAjax, FolderListAjax, StartRestoreAjax
)

urlpatterns = [
    url(r'^ajax/status/$', AllJobsStatusAjax, name='AllJobsStatusAjax'),
    url(r'^ajax/status/(?P<job>.*)/$', JobStatusAjax, name='JobStatusAjax'),
    url(r'^ajax/run/bkpall/$', StartBKPALLAjax, name='StartBKPALLAjax'),
    url(r'^ajax/run/bkp/(?P<profile>.*)/full/$', StartBackupAjax,
        name='StartFullBackupAjax', kwargs={'full': True}),
    url(r'^ajax/run/bkp/(?P<profile>.*)/$', StartBackupAjax,
        name='StartBackupAjax'),
    url(r'^ajax/list/(?P<profile>.*)/$', ListFilesAjax,
        name='ListFilesAjax'),
    url(r'^list/(?P<profile>.*)/$', ListFiles, name='ListProfileFiles'),
    url(r'^restore/(?P<profile>.*)/(?P<to>.*)/$', ListFiles,
        name='RestoreFilesTo', kwargs={'restore': True}),
    url(r'^restore/(?P<profile>.*)/$', ListFiles, name='RestoreFiles',
        kwargs={'restore': True}),
    url(r'^ajax/restore/(?P<profile>.*)/$', StartRestoreAjax,
        name='StartRestoreAjax'),
    url(r'^ajax/folder_list/$', FolderListAjax, name="FolderListAjax"),
]

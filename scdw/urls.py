"""scdw URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from filelist.views import filelist
from bprofile.views import (
    init_backend, list_bprofiles, delete_bprofile, show_bprofile,
    excl_action, edit_bprofile, new_bprofile, edit_conf, edit_quick,
    show_log
)
from django.contrib.auth.views import login, logout
from django.conf.urls.static import static
import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', list_bprofiles, name='Default'),
    url(r'^list/$', list_bprofiles, name='ListProfiles'),
    url(r'^show/(?P<name>.*)/(?P<excpt_enc>.*)/$', show_bprofile,
        name='ShowProfileWith'),
    url(r'^show/(?P<name>.*)/$', show_bprofile, name='ShowProfile'),
    url(r'^new/(?P<source_enc>.*)/$', new_bprofile, name='CreateProfile'),
    url(r'^edit/(?P<name>.*)/$', edit_bprofile, name='EditProfile'),
    url(r'^delete/(?P<name>.*)/$', delete_bprofile, name='DeleteProfile'),
    url(r'^log/(?P<name>.*)/(?P<type>.*)/(?P<date>.*)/(?P<log_enc>.*)/$',
        show_log, name='ShowLog'),
    url(r'^edit_config/$', edit_conf, name='EditGlobalConfig'),
    url(r'^edit_quick/$', edit_quick, name='EditSCDWGlobalConfig'),
    url(r'^excl/(?P<action>.*)/(?P<name>.*)/(?P<excpt_enc>.*)/$', excl_action,
        name='MoveExclude'),
    url(r'^init/$', init_backend, name='InitSCDW'),
    url(r'^filelist/(?P<action>.*)/(?P<path>.*)/dirs$', filelist,
        name='ListDirs', kwargs={'dirsOnly': True}),
    url(r'^filelist/(?P<action>.*)/(?P<path>.*)/$', filelist, name='ListFiles'),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout,
        dict(template_name='registration/logout.html',),
        name='logout', ),
    url(r'^job/', include('jobs.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

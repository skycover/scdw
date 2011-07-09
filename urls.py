from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from bprofile.views import *
from filelist.views import *
from django.conf import settings

urlpatterns = patterns('',
    # Example:
    # (r'^scduplyw/', include('scduplyw.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^$', list_bprofiles),
    (r'^list/$', list_bprofiles),
    (r'^show/(?P<name>.*)/(?P<excpt_enc>.*)/$', show_bprofile),
    (r'^show/(?P<name>.*)/$', show_bprofile),
    (r'^new/(?P<source_enc>.*)/$', new_bprofile),
    (r'^edit/(?P<name>.*)/$', edit_bprofile),
    (r'^delete/(?P<name>.*)/$', delete_bprofile),
    (r'^edit_config/$', edit_conf),
    (r'^excl/(?P<action>.*)/(?P<name>.*)/(?P<excpt_enc>.*)/$', excl_action),
    (r'^init/$', init_backend),
    (r'^filelist/(?P<action>.*)/(?P<path>.*)/$', filelist),
)

urlpatterns += patterns('',
    (r'^favicon.ico$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'path': "favicon.ico"}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
)

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^moderate/save/$', 'gatekeeper.views.moderate', name="gatekeeper_moderate"),
    url(r'^moderate/(?P<app_label>\w+)\.(?P<model>\w+)/$', 'gatekeeper.views.moderate_list'),
    url(r'^moderate/$', 'gatekeeper.views.moderate_list', name="gatekeeper_moderate_list"),
)
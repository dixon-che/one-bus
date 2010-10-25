from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings


admin.autodiscover()

urlpatterns = patterns('',
                       (r'^$', "one-bus.views.hello"),
                       (r'^transport_list/$', "one-bus.views.transport_list"),
                       (r'^route/$', "one-bus.views.route"),
                       (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       (r'^admin/', include(admin.site.urls)),
)

if settings.MEDIA_APACHE_DIRECT == False:
    urlpatterns += patterns('',
        (r'^%s(.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

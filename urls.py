from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings


admin.autodiscover()

urlpatterns = patterns('',
                       (r'^$', "one-bus.views.hello"),
                       (r'^transport_list/$', "one-bus.views.transport_list"),
                       (r'^route/$', "one-bus.views.route"),
                       (r'^stations/add/$', "one-bus.views.station_add"),
                       (r'^stations/autocomplete/$', "one-bus.views.station_autocomplete"),
                       (r'^stations/autocomplete2/$', "one-bus.views.station_autocomplete2"),
                       (r'^stations/edit/(?P<route_id>\d+)/$', "one-bus.views.station_edit"),
                       url(r'^stations/save_station/$', "one-bus.views.station_save_in_route", name="ajax-station-save"),
                       url(r'^stations/save_new_station/$', "one-bus.views.new_station_save_in_route", name="ajax-newstation-save"),
                       url(r'^stations/delete_station/$', "one-bus.views.station_delete", name="ajax-station-delete"),
                       (r'^stations/route_save/$', "one-bus.views.station_save"),
                       (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       (r'^admin/', include(admin.site.urls)),
)

if settings.MEDIA_APACHE_DIRECT == False:
    urlpatterns += patterns('',
        (r'^%s(.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

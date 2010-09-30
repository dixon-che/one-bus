from apps.point.models import Transport, Route, Station, Metastation
from django.contrib import admin


class TransportAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'ico', 'price', 'description')

admin.site.register(Transport, TransportAdmin)

class RouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'route', 'interval', 'speed', 'price', 'transport_type', 'one_pay')
    list_filter = ('transport_type', 'price') 

admin.site.register(Route, RouteAdmin)

class StationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'coordinate_x', 'coordinate_y', 'route', 'next_station', 'prev_station', 'meta_station')
    list_filter = ('route', 'meta_station')

admin.site.register(Station, StationAdmin)

class MetastationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address')

admin.site.register(Metastation, MetastationAdmin)

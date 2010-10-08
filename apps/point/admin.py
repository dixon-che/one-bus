from apps.point.models import Transport, Route, Station, Metastation
from django.contrib import admin


class TransportAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'ico', 'price', 'description')
    list_editable = ('price', 'description')

admin.site.register(Transport, TransportAdmin)

class RouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'route', 'interval', 'transport_type', 'speed', 'price', 'one_pay')
    list_filter = ('transport_type', 'price')
    list_editable = ('price', 'speed', 'interval')

admin.site.register(Route, RouteAdmin)

class StationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'coordinate_x', 'coordinate_y', 'route', 'order', 'meta_station')
    list_filter = ('route', 'meta_station', 'name')
    list_editable = ('coordinate_x', 'coordinate_y', 'order')

admin.site.register(Station, StationAdmin)

class MetastationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address')

admin.site.register(Metastation, MetastationAdmin)

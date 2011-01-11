from apps.point.models import Transport, Route, Station, Onestation
from django.contrib import admin


class TransportAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'ico', 'price', 'description')

admin.site.register(Transport, TransportAdmin)

class RouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'route', 'interval', 'transport_type', 'speed', 'price', 'one_pay', 'color')
    list_filter = ('transport_type', 'price')
    list_editable = ('price', 'speed', 'interval')

admin.site.register(Route, RouteAdmin)

class OnestationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'coordinate_x', 'coordinate_y')
    list_editable = ('coordinate_x', 'coordinate_y')

admin.site.register(Onestation, OnestationAdmin)

class StationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'coordinate_x', 'coordinate_y', 'route', 'order', 'matrix_index', 'notstations', 'one_station')
    list_filter = ('route', 'name')
    list_editable = ('coordinate_x', 'coordinate_y', 'order', 'matrix_index', 'notstations')

admin.site.register(Station, StationAdmin)

#class MetastationAdmin(admin.ModelAdmin):
#    list_display = ('id', 'name', 'address')

#admin.site.register(Metastation, MetastationAdmin)

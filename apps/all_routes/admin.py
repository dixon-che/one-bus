from apps.all_routes.models import Routes
from django.contrib import admin


class RouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'finish_point', 'start_point', 'route')

admin.site.register(Routes, RouteAdmin)

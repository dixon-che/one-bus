#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apps.point.models import Route, Station, Metastation, Transport

                                        '''ПРИОБРАЗОВАНИЕ ДАННЫХ ИЗ КВЕРИСЕТ'''

points_list = Station.objects.values_list('coordinate_x', 'coordinate_y').order_by('id')
a = Station.objects.values('id', 'route_id', 'coordinate_x', 'coordinate_y', 'name', 'meta_station_id')
z = Route.objects.values('id', 'route', 'speed', 'interval')
b = Metastation.objects.values('id')
graph_dict = dict()
time_chenge = dict()
all_speed = dict()
points_list_chenge = list()

for q in a:
    name = q['name']
    idk = q['id']
    route_id = q['route_id']
    meta_station_id = q['meta_station_id']

for q in z:
    idk = q['id']
    qwas = Route.objects.get(id=idk).station_set.values_list('id', flat=True)
    graph_dict[idk] = qwas
    route = q['route']
    speed = q['speed']
    interval = q['interval']
    all_speed[route] = speed
    time_chenge[route] = interval

for q in b:
    idk = q['id']
    qwas = Metastation.objects.get(id=idk).station_set.values_list('id', flat=True)
    points_list_chenge += [qwas]











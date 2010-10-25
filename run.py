#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apps.point.models import Route, Station, Metastation, Transport

a = Station.objects.values('id', 'route_id', 'coordinate_x', 'coordinate_y', 'name', 'meta_station_id')
z = Route.objects.values('id', 'route', 'speed', 'interval')
time_chenge = dict()
all_speed = dict()
points_list_chenge = list()
for q in a:
    name = q['name']
    idk = q['id']
    route_id = q['route_id']
    meta_station_id = q['meta_station_id']

for q in z:
    route = q['route']
    speed = q['speed']
    interval = q['interval']
    all_speed[route] = speed
    time_chenge[route] = interval


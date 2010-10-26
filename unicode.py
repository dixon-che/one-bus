#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from apps.point.models import Station, Route

fp = open('example_view', 'r+b')
points_list = json.load(fp)

s = Station.objects.values('route_id', 'coordinate_x', 'coordinate_y', 'name')
for point in s:
    q = point['route_id']
    w = point['coordinate_x']
    z = point['coordinate_y']
    e = point['name']
    print q, w, z, e


    for item in points_list:
        a = item['id']
        x = item['x']
        y = item['y']
        name = item['name']
        pname = item['pname']
        qwaz = Station(route_id=a, coordinate_x=x, coordinate_y=y, name=pname)
        qwaz.save()
        print qwaz   


#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from apps.point.models import Route, Station, Metastation, Transport
from math import *
from utils import len_witput_points, get_speed_matrix, get_border_points, get_lenth_finish, get_lenth_start, get_all_x, get_points_in_radius_start, get_points_in_radius_finish
import json


def station_save(request):
    route0 = request.POST['route']
    routeName = request.POST['routeName']
    transportType = request.POST['routeType']
    route = eval(route0)
    routeName = str(routeName)
    transportType = str(transportType)
    transport = Transport.objects.get(name=transportType)
    new_route = Route(route = routeName, transport_type = transport, interval = 12, speed = 12, color = "FFFFFFFF", price = 1)
    new_route.save()
    for index in range(len(route)):
        station_1 = route[str(index)]
        station_name = station_1[0].decode('utf8')
        station_y = station_1[1]
        station_x = station_1[2]
        matrix_index = list()
        for station_out_bd in Station.objects.all():
            matrix_index += [station_out_bd.matrix_index]
        matrix_index_max = max(matrix_index) + 1
        station_in_bd = Station(route = new_route, name = station_name, coordinate_x = station_x, coordinate_y = station_y, matrix_index = matrix_index_max)
        station_in_bd.save()
    return HttpResponse('ok')

def station_add(request):
    text2 = 'Welcome to "Transplants do not"'
    return render_to_response('add_stations.html', {"text2": text2})

def station_edit(request):
    text3 = 'Welcome to "Transplants do not"'
    return render_to_response('edit_stations.html', {"text3": text3})

def hello(request):
    text = 'Welcome to "Transplants do not"'
    return render_to_response('base.html', {"text": text})

def transport_list(request):
    stations = list(Station.objects.all().values('route__id', 'route__route',
                                                 'route__color', 'route__transport_type', 'name',
                                                 'coordinate_x', 'coordinate_y'))
    return HttpResponse(json.dumps(stations), 'application/javascript')

def route(request):
    closed_points_list = list()
    KoeRad = 0.01
    R = 6376 # радиус земли
    speed_matrix = get_speed_matrix()

    start_x = float(request.GET['x1'])
    start_x_rad = start_x*pi/180 
    sx1 = start_x + KoeRad
    sx2 = start_x - KoeRad
    start_y = float(request.GET['y1'])
    start_y_rad = start_y*pi/180
    sy1 = start_y + KoeRad
    sy2 = start_y - KoeRad
    finish_x = float(request.GET['x2'])
    finish_x_rad = finish_x*pi/180
    fx1 = finish_x + KoeRad
    fx2 = finish_x - KoeRad
    finish_y = float(request.GET['y2'])
    finish_y_rad = finish_y*pi/180
    fy1 = finish_y + KoeRad
    fy2 = finish_y - KoeRad
    s_f = acos(sin(start_y_rad)*sin(finish_y_rad) + cos(start_y_rad)*cos(finish_y_rad)*cos(finish_x_rad-start_x_rad))*R

    # заполняем список точек пересадок metastations_stations_list
    metastations_stations_list = list()
    for metastation_item in Metastation.objects.all():
        metastation_station_set = list(metastation_item.station_set.values_list('matrix_index', flat=True))
        metastations_stations_list += [metastation_station_set]

    all_station_x = get_all_x()
    lenth_start = get_lenth_start(start_y_rad, start_x_rad)
    lenth_finish = get_lenth_finish(finish_y_rad, finish_x_rad)
    lenth_finish_min = min(lenth_finish)
    T_pesh_finish = lenth_finish_min
    lenth_start_min = min(lenth_start)
    tstart_point = lenth_start.index(lenth_start_min)
    tend_point = lenth_finish.index(lenth_finish_min)

    start_point = lenth_start.index(lenth_start_min)
    end_point = lenth_finish.index(lenth_finish_min)

    lenth_start.append(0)
    lenth_start.append(s_f)
    lenth_finish.append(s_f)
    lenth_finish.append(0)

    for Mass in speed_matrix:
        index_Mass = speed_matrix.index(Mass)
        Mass.append(lenth_start[index_Mass])
        Mass.append(lenth_finish[index_Mass])

    speed_matrix.append(lenth_start)
    speed_matrix.append(lenth_finish)

    points_in_radius_start = get_points_in_radius_start(sx2, sx1, sy1, sy2, all_station_x)
    for point_in_radius in points_in_radius_start:
        that = list()
        that += [start_point]
        that += [point_in_radius]
        metastations_stations_list += [that]

    points_in_radius_finish = get_points_in_radius_finish(fx2, fx1, fy1, fy2, all_station_x)
    for point_in_radius in points_in_radius_finish:
        thet = list()
        thet += [end_point]
        thet += [point_in_radius]
        metastations_stations_list += [thet]

    if points_in_radius_finish == []:
        end_point = tend_point
    if points_in_radius_start == []:
        start_point = tstart_point

    points_price = {str(start_point): [0, [start_point], [0]]}
    next_points_list = [start_point]

    while next_points_list:
        p = [[next_key, points_price[str(next_key)][0]] for next_key in next_points_list]
        active_point = min(p, key=lambda x: x[1])[0]
        active_point_price = points_price[str(active_point)][0]
        active_point_P = points_price[str(active_point)][1]
        active_point_Pe = points_price[str(active_point)][2]
        border_points = get_border_points(active_point, closed_points_list)
        for item_point_index in border_points:
            go_price = speed_matrix[active_point][item_point_index]
            if str(item_point_index) not in points_price:
                curent_point_index = [item_point_index]
                go_price_time = active_point_price + go_price
                time = [go_price_time]
                points_price[str(item_point_index)] = [go_price_time, active_point_P + curent_point_index, active_point_Pe + time]
            else:
                item_point_price = points_price[str(active_point)][0] + go_price
                if item_point_price < points_price[str(item_point_index)][0]:
                    points_price[str(item_point_index)][0] = item_point_price

        closed_points_list.append(active_point)
        next_points_list.remove(active_point)
        next_points_list += border_points
        next_points_list = list(set(next_points_list))
        if end_point in closed_points_list:
            break

    if str(end_point) in points_price:
        print "Your way is:", points_price[str(end_point)][1]
        print "Your time is:", points_price[str(end_point)][2]
    final_views = [{'x': start_x, 'y': start_y, 'idRoute':"-1", 'transportName':"", 'stopName':"Start", 't':'0'}]
    i = 0
    for q in points_price[str(end_point)][1]:
        item_dict = {}
        point = Station.objects.get(matrix_index=q)
        item_dict['stopName'] = point.name
        item_dict['idRoute'] = str(point.route_id)
        item_dict['route__transport_type'] = str(point.route.transport_type_id)
        item_dict['transportName'] = item_dict['route__transport_type']
        item_dict['x'] = str(point.coordinate_x)
        item_dict['y'] = str(point.coordinate_y)
        item_dict['t'] = str(points_price[str(end_point)][2][i])
        final_views += [item_dict]
        i += 1
    final_time = points_price[str(end_point)][2][-1] + T_pesh_finish
    final_views.append({'x': finish_x, 'y': finish_y, 'idRoute': "-1", 'transportName': "", 'stopName': "Finish", 't': final_time})
    final_views.reverse()

    return HttpResponse(json.dumps(final_views), 'application/javascript')

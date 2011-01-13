#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db.models import Max
from settings import PROJECT_ROOT
from django.shortcuts import render_to_response
from django.http import HttpResponse
from apps.point.models import Route, Station, Transport, Onestation
from math import *
from utils import len_witput_points, get_speed_matrix, get_border_points, get_lenth_finish, get_lenth_start, get_all_x, get_points_in_radius_start, get_points_in_radius_finish, get_metastations_stations_list, new_Metastation, new_speed_matrix, points_list, transport_types
import json, os, datetime


def new_station_save_in_route(request):
    name = request.POST['name']
    y = request.POST['lat']
    x = request.POST['lon']
    route_id = request.POST['route_id']
    matrix_index = list()
    for station_out_bd in Station.objects.all():
        matrix_index += [station_out_bd.matrix_index]
    matrix_index_max = max(matrix_index) + 1
    new_station = Station(route_id = route_id, name = name, coordinate_x = x, coordinate_y = y, matrix_index = matrix_index_max)
    new_station.save()
    return HttpResponse('OK')


def station_save_in_route(request):
    station_id = request.POST['id']
    name = request.POST['name']
    y = request.POST['lat']
    x = request.POST['lon']
    station = Station.objects.get(id=station_id)
    station.name = name
    station.coordinate_x = x
    station.coordinate_y = y
    station.save()
    return HttpResponse('OK')


def station_delete(request):
    station_id = request.POST['id']
    station = Station.objects.get(id=station_id)
    station.delete()
    return HttpResponse('OK')


def station_save(request):
    route0 = request.POST['route']
    routeName = request.POST['routeName']
    transportType = request.POST['routeType']
    route = eval(route0)
    routeName = str(routeName)
    transportType = str(transportType)
    transport = Transport.objects.get(name=transportType)
    new_route = Route(route = routeName, transport_type = transport, interval = 0.12, speed = 12, color = "FFFFFFFF", price = 1)
    new_route.save()
    for index in range(len(route)):
        station_1 = route[str(index)]
        station_name = station_1[0].decode('utf8')
        station_y = station_1[1]
        station_x = station_1[2]
        station_list = list()
        one_station_list_with_name = Onestation.objects.filter(name=station_name)
        if not one_station_list_with_name:
            one_station = Onestation.objects.create(name=station_name, coordinate_x=station_x, coordinate_y=station_y)
        else:
            one_station = one_station_list_with_name[0]
        matrix_index = list()
        for station_out_bd in Station.objects.all():
            matrix_index += [station_out_bd.matrix_index]
        matrix_index_max = max(matrix_index) + 1
        station_in_bd = Station(route=new_route, name=station_name, coordinate_x=station_x, coordinate_y=station_y, matrix_index=matrix_index_max, notstations=True, order=index, one_station=one_station)
        if station_name == "temporary":
            station_name = "temporary" + str(index)
            station_in_bd = Station(route=new_route, name=station_name, coordinate_x=station_x, coordinate_y=station_y, matrix_index=-1, notstations=False, order=index)

        station_in_bd.save()
    return HttpResponse('ok')


def station_add(request):
    onestation = "onestation"
    return render_to_response('add_stations.html', {"onestation": onestation})


def station_autocomplete(request):
    name = request.GET['term']
    json_list = list()
    for station in Onestation.objects.filter(name__contains=name):
        stat_dict = dict()
        stat_dict['label'] = station.name
        stat_dict['value'] = station.name
        stat_dict['id'] = station.name
        stat_dict['x'] = station.coordinate_x
        stat_dict['y'] = station.coordinate_y
        json_list += [stat_dict]
    return  HttpResponse(json.dumps(json_list), 'application/javascript')


def station_edit(request, route_id):
    stations = Station.objects.filter(route = route_id)
    return render_to_response('edit_stations.html', {"stations": stations,
                                                     "route_id": route_id})


def hello(request):
#    qw = Onestation.objects.all()
#    for q in qw:
#        qa = Station.objects.filter(name=q.name)
#        for a in qa:
#            a.one_station = q
#            a.save()

#    qw =set(Station.objects.all().values_list('name', flat=True))
#    for q in qw:
#        a = Station.objects.filter(name=q).values_list('coordinate_x', flat=True)
#        z = Station.objects.filter(name=q).values_list('coordinate_y', flat=True)
#        Onestation.objects.create(name=q, coordinate_x=a[0], coordinate_y=z[0])
    text = 'Welcome to "Transplants do not"'
    return render_to_response('base.html', {"text": text})


def transport_list(request):
    transport_list_txt = os.path.join(PROJECT_ROOT, 'kesh/transport_list.txt')
    max_station_timestamp = Station.objects.all().aggregate(Max('timestamp'))
    max_route_timestamp = Route.objects.all().aggregate(Max('timestamp'))
    max_transport_timestamp = Transport.objects.all().aggregate(Max('timestamp'))
    max_onestation_timestamp = Onestation.objects.all().aggregate(Max('timestamp'))
    max_timestamp = max(max_onestation_timestamp, max_station_timestamp, max_route_timestamp, max_transport_timestamp)
    max_timestamp = max_timestamp['timestamp__max']
    if os.path.isfile(transport_list_txt) == False:
        open(transport_list_txt, 'w')
    sm_file = os.path.getmtime(transport_list_txt)
    stat = os.stat(transport_list_txt)
    file_size = stat.st_size
    timestamp = datetime.datetime.fromtimestamp(sm_file)

    if timestamp < max_timestamp or file_size == 0:
        stations = list(Station.objects.all().values('route__id', 'route__route',
                                                     'route__color', 'route__transport_type', 'name',
                                                     'coordinate_x', 'coordinate_y').order_by('route__id', 'order'))

        fp = open(transport_list_txt, 'w+')
        fp.write(repr(stations))
        fp.close()
    else:
        fp = open(transport_list_txt, 'r')
        read_file = fp.read()
        stations = eval(read_file)
        fp.close()            

    return HttpResponse(json.dumps(stations), 'application/javascript')


def route(request):
    closed_points_list, border_in_radius = list(), list()
    KoeRad = 0.05
    R = 6376 # радиус земли
    Transport0 = Transport1 = Transport2 = Transport3 = Transport4 = 0
#    Transport1 = 1
#    Transport2 = 1
    speed_matrix = get_speed_matrix(Transport1, Transport2, Transport3, Transport4)
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
    s_f = (acos(sin(start_y_rad)*sin(finish_y_rad) + cos(start_y_rad)*cos(finish_y_rad)*cos(finish_x_rad-start_x_rad))*R)/3
    all_station_x = get_all_x()
    lenth_start = get_lenth_start(start_y_rad, start_x_rad)
    lenth_finish = get_lenth_finish(finish_y_rad, finish_x_rad)
    lenth_finish_min = min(lenth_finish)
    lenth_start_min = min(lenth_start)
    tstart_point = lenth_start.index(lenth_start_min)
    tend_point = lenth_finish.index(lenth_finish_min)
    transports = transport_types()
    start_point = len(all_station_x)
    end_point = start_point + 1

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

    points_in_radius_finish = get_points_in_radius_finish(fx2, fx1, fy1, fy2, all_station_x)    
    points_in_radius_start = get_points_in_radius_start(sx2, sx1, sy1, sy2, all_station_x, Transport1, Transport2, Transport3, Transport4)
    if points_in_radius_finish == []:
        points_in_radius_finish = [tend_point]
    if points_in_radius_start == []:
        points_in_radius_start = [tstart_point]

    points_price = {str(start_point): [0, [start_point], [0]]}
    point_list_item = points_list(points_in_radius_finish, points_in_radius_start, start_point, end_point)
    metastations_stations_list = new_Metastation(Transport1, Transport2, Transport3, Transport4)
    next_points_list = [start_point]
    while next_points_list:
        p = [[next_key, points_price[str(next_key)][0]] for next_key in next_points_list]
        active_point = min(p, key=lambda x: x[1])[0]
        active_point_price = points_price[str(active_point)][0]
        active_point_P = points_price[str(active_point)][1]
        active_point_Pe = points_price[str(active_point)][2]
        border_points = get_border_points(active_point, closed_points_list, point_list_item, metastations_stations_list)
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
                    points_price[str(item_point_index)][1] = points_price[str(active_point)][1] + [item_point_index]
                    points_price[str(item_point_index)][2] = points_price[str(active_point)][2] + [item_point_price]

        closed_points_list.append(active_point)
        next_points_list.remove(active_point)
        next_points_list += border_points
        next_points_list = list(set(next_points_list))
        if end_point in closed_points_list:
            break

    if str(end_point) in points_price:
        print "Your way is:", points_price[str(end_point)][1]
        print "Your time is:", points_price[str(end_point)][2]
        final_time = round((points_price[str(end_point)][2][-1])*60, 2)
        points_price[str(end_point)][1].remove(start_point)
        points_price[str(end_point)][1].remove(end_point)
        points_price[str(end_point)][2] = points_price[str(end_point)][2][1:-1]

    final_views = [{'x': start_x, 'y': start_y, 'idRoute':"-1", 'transportName':"", 'stopName':"Start", 't':'0', 'TransportsType':'', 'routeName':''}]
    i = 0
    q_list = list()
    for q in points_price[str(end_point)][1]:
        q_list += [q]
        item_dict = {}
        point = Station.objects.get(matrix_index=q)
        item_dict['stopName'] = point.name
        item_dict['idRoute'] = point.route_id
        item_dict['routeName'] = Route.objects.get(id=point.route_id).route
        item_dict['route__transport_type'] = point.route.transport_type_id
        transport_id = item_dict['transportName'] = item_dict['route__transport_type']
        item_dict['TransportsType'] = Transport.objects.get(id=transport_id).name
        item_dict['x'] = point.coordinate_x
        item_dict['y'] = point.coordinate_y
        item_dict['t'] = round(points_price[str(end_point)][2][i]*60, 2)
        final_views += [item_dict]            
        orde = point.order
        long_route = len(Station.objects.filter(route=point.route_id).values_list('order', flat=True)) - 1
        next_orde = orde + 1
        prev_orde = orde - 1
        prev_q = q - 1
        next_q = q + 1
        if long_route >= next_orde and Station.objects.get(order=next_orde, route=point.route_id).matrix_index == -1 and next_q not in q_list:
            end_orde = range(Station.objects.get(matrix_index=next_q).order)
            order_list = end_orde[next_orde:]
            for element in order_list:
                item_dict = {}
                point2 = Station.objects.get(order=element, route=point.route_id)
                item_dict['route__transport_type'] = 10
                item_dict['idRoute'] = point.route_id
                item_dict['x'] = point2.coordinate_x
                item_dict['y'] = point2.coordinate_y
                item_dict['stopName'] = element
                item_dict['t'] = round(points_price[str(end_point)][2][i]*60, 2)
                final_views += [item_dict]
        elif prev_orde >= 1 and Station.objects.get(order=prev_orde, route=point.route_id).matrix_index == -1 and prev_q not in q_list:
            end_orde = range(Station.objects.get(matrix_index=q).order)
            end_orde2 = len(range(Station.objects.get(matrix_index=prev_q).order + 1))
            order_list = end_orde[end_orde2:orde] 
            order_list.reverse()
            for element in order_list:
                item_dict = {}
                point2 = Station.objects.get(order=element, route=point.route_id)
                item_dict['route__transport_type'] = 10
                item_dict['idRoute'] = point.route_id
                item_dict['x'] = point2.coordinate_x
                item_dict['y'] = point2.coordinate_y
                item_dict['stopName'] = element
                item_dict['t'] = round(points_price[str(end_point)][2][i]*60, 2)
                final_views += [item_dict]
            print order_list
        i += 1
    final_views.append({'x': finish_x, 'y': finish_y, 'idRoute': "-1", 'transportName': "", 'stopName': "Finish", 't': final_time, 'TransportsType':'', 'routeName':''})
    final_views.reverse()

    return HttpResponse(json.dumps(final_views), 'application/javascript')

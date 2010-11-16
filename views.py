#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from apps.point.models import Route, Station, Metastation, Transport
from math import *
import json


def hello(request):
    text = 'Welcome to "Transplants do not"'
    return render_to_response('base.html', {"text": text})

def transport_list(request):
    stations = list(Station.objects.all().values('route__id', 'route__route',
                                                 'route__color', 'route__transport_type', 'name',
                                                 'coordinate_x', 'coordinate_y'))
    return HttpResponse(json.dumps(stations), 'application/javascript')


def route(request):
    points_list = Station.objects.values_list('coordinate_x', 'coordinate_y').order_by('id')
    len_points = len(points_list)
    speed_matrix = [[0] * len_points  for i in range(len_points)]
    all_station_list = Station.objects.values('id', 'route_id', 'coordinate_x', 'coordinate_y',
                                              'name', 'meta_station_id', 'matrix_index').order_by('matrix_index')

    lenth_start, lenth_finish, lenth_finish_to_z, lenth_start_to_z = list(), list(), list(), list()
    closed_points_list = list()
    points_in_radius_start, points_in_radius_finish = list(), list()
    all_station_x, radius_x_start, radius_x_finish = list(), list(), list()

    coord_v_km, coord_v_km2 = 111.1, 78.56
    speed_Pesh = 3.0
    wating_index = 1/2.0
    KoeRad = 0.001

    def len_witput_points(start_point, end_point):
        lenth = pow((pow(start_point[0] - end_point[0], 2) * coord_v_km2) +
                     (pow(start_point[1] - end_point[1], 2) * coord_v_km), 1/2.0)
        return lenth

    start_x = float(request.GET['x1'])#*pi/180
    sx1 = start_x + KoeRad
    sx2 = start_x - KoeRad
    start_y = float(request.GET['y1'])#*pi/180
    sy1 = start_y + KoeRad
    sy2 = start_y - KoeRad
    finish_x = float(request.GET['x2'])#*pi/180
    fx1 = finish_x + KoeRad
    fx2 = finish_x - KoeRad
    finish_y = float(request.GET['y2'])#*pi/180
    fy1 = finish_y + KoeRad
    fy2 = finish_y - KoeRad
#    R = 6376
#    ddd = acos(sin(start_y)*sin(finish_y) + cos(start_y)*cos(finish_y)*cos(finish_x-start_x))*R

    # заполняем routes_dict, routes_speeds, routes_intevals
    routes_dict, routes_intevals, routes_speeds = dict(), dict(), dict()
    for route_item in Route.objects.all():
        routes_dict[route_item.id] = list(route_item.station_set.values_list('matrix_index', flat=True))
        routes_speeds[route_item.id] = route_item.speed
        routes_intevals[route_item.id] = route_item.interval
#    print ddd, pi

    # заполняем список точек пересадок metastations_stations_list
    metastations_stations_list = list()
    for metastation_item in Metastation.objects.all():
        metastation_station_set = list(metastation_item.station_set.values_list('matrix_index', flat=True))
        metastations_stations_list += [metastation_station_set]

    # формирование матрици времени переходов speed_matrix)
    for route_id in routes_dict:
        route_item_list = routes_dict[route_id]
        route_speed = float(routes_speeds[route_id])

        for item_index in range(len(route_item_list)):
            next_item_index = item_index + 1
            if next_item_index == len(route_item_list):
                break

            from_matrix_index = route_item_list[item_index]
            to_matrix_index = route_item_list[next_item_index]

            speed_matrix[to_matrix_index][from_matrix_index] = \
            speed_matrix[from_matrix_index][to_matrix_index] = len_witput_points(points_list[from_matrix_index],
                                                                                 points_list[to_matrix_index]) / route_speed
    # добавление в speed_matrix переходов по метастанциям
    for item_metastation_stations_list in metastations_stations_list:
        for item_station_from in item_metastation_stations_list:
            for item_station_to in item_metastation_stations_list:
                route_interval_time = routes_intevals[Station.objects.get(matrix_index=item_station_to).route_id]
                speed_matrix[item_station_from][item_station_to] = route_interval_time * wating_index

    # добавляем точки старта-финиша к матрице переходов
    for station_item in all_station_list:
        coordinate_x = float(station_item['coordinate_x'])
        all_station_x += [coordinate_x]
        coordinate_y = float(station_item['coordinate_y'])

        l_s = pow((pow(start_x - coordinate_x, 2) * coord_v_km2) +
                  (pow(start_y - coordinate_y, 2) * coord_v_km),
                  1/2.0) / speed_Pesh
        lenth_start += [l_s]
        lenth_start_to_z += [l_s]

        l_f = pow((pow(finish_x - coordinate_x, 2) * coord_v_km2) +
                  (pow(finish_y - coordinate_y, 2) * coord_v_km),
                  1/2.0) / speed_Pesh
        lenth_finish += [l_f]
        lenth_finish_to_z += [l_f]

    s_f = pow((pow(finish_x - start_x, 2) * coord_v_km2) +
              (pow(finish_y - start_y, 2) * coord_v_km),
              1/2.0) / speed_Pesh

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

#    end_point = index_Mass + 2
#    start_point = index_Mass +1

    for station_x in all_station_x:
        if sx2 < station_x < sx1:
            radius_x_start += [station_x]
    for x_start in radius_x_start:
        station_for_y = Station.objects.filter(coordinate_x=x_start).values_list('coordinate_y', 'matrix_index')
        for station_y in station_for_y:
            if sy2 < station_y[0] < sy1:
                points_in_radius_start += [station_y[1]]

    for point_in_radius in points_in_radius_start:
        that = list()
        that += [start_point]
        that += [point_in_radius]
        metastations_stations_list += [that]

    for station_x in all_station_x:
        if fx2 < station_x < fx1:
            radius_x_finish += [station_x]
    for x_finish in radius_x_finish:
        station_for_y = Station.objects.filter(coordinate_x=x_finish).values_list('coordinate_y', 'matrix_index')
        for station_y in station_for_y:
            if fy2 < station_y[0] < fy1:
                points_in_radius_finish += [station_y[1]]

    for point_in_radius in points_in_radius_finish:
        thet = list()
        thet += [end_point]
        thet += [point_in_radius]
        metastations_stations_list += [thet]

    if points_in_radius_finish == []:
        end_point = tend_point
    if points_in_radius_start == []:
        start_point = tstart_point

    def get_border_points(points_price_min, closed_points_list):
        points_list = []
        for route_id in routes_dict:
            points_list_item = routes_dict[route_id]
            len_points_list_item = len(points_list_item)
            if points_price_min in points_list_item:
                index_in_list = points_list_item.index(points_price_min)
                if index_in_list < len_points_list_item - 1:
                    right_border_index = points_list_item[index_in_list + 1]
                    if right_border_index not in closed_points_list:
                        points_list += [right_border_index]
                if index_in_list > 0:
                    left_border_index = points_list_item[index_in_list - 1]
                    if left_border_index not in closed_points_list:
                        points_list += [left_border_index]

                for metastation in metastations_stations_list:
                    if points_price_min in metastation:
                        for metastation_index in range(len(metastation)):
                            metastation_index_next = metastation_index + 1
                            if metastation_index_next == len(metastation):
                                break
                            next_index = metastation.index(points_price_min) - metastation_index_next
                            next_item = metastation[next_index]
                            if next_item not in closed_points_list:
                                points_list += [next_item]

        for metastation in metastations_stations_list:
            if points_price_min in metastation:
                for metastation_index in range(len(metastation)):
                    metastation_index_next = metastation_index + 1
                    if metastation_index_next == len(metastation):
                        break
                    next_index = metastation.index(points_price_min) - metastation_index_next
                    next_item = metastation[next_index]
                    if next_item not in closed_points_list:
                        points_list += [next_item]
        return list(set(points_list))

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
        point_name = point.name
        item_dict['stopName'] = point_name
        point_route_id = point.route_id
        P_route_id = str(point_route_id)
        item_dict['idRoute'] = str(point.route_id) #P_route_id
        item_dict['route__transport_type'] = str(point.route.transport_type_id)
        item_dict['transportName'] = item_dict['route__transport_type']
        point_coordinate_x = point.coordinate_x
        item_dict['x'] = str(point_coordinate_x)
        point_coordinate_y = point.coordinate_y
        item_dict['y'] = str(point_coordinate_y)
        item_dict['t'] = str(points_price[str(end_point)][2][i])
        final_views += [item_dict]
        i += 1
    final_time = points_price[str(end_point)][2][-1] + T_pesh_finish
    final_views.append({'x': finish_x, 'y': finish_y, 'idRoute': "-1", 'transportName': "", 'stopName': "Finish", 't': final_time})
    final_views.reverse()

    return HttpResponse(json.dumps(final_views), 'application/javascript')

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from settings import PROJECT_ROOT
from math import *
from apps.point.models import Route, Station, Metastation, Transport
from django.db.models import Max
import os
import datetime


# функция нахождения растояния по шаровым координатам
def len_witput_points(start_point, end_point):
    R = 6376 # радиус земли
    sp1 = start_point[1]*pi/180
    ep1 = end_point[1]*pi/180
    sp0 = start_point[0]*pi/180
    ep0 = end_point[0]*pi/180
    lenth = acos(sin(sp1)*sin(ep1) + cos(sp1)*cos(ep1)*cos(ep0-sp0))*R
    return lenth

#функция нахождения соседних точек
def get_border_points2(points_price_min, closed_points_list, metastations_stations_list):

         # заполняем routes_dict, routes_speeds, routes_intevals
    routes_dict = dict()
    for route_item in Route.objects.all():
        routes_dict[route_item.id] = list(route_item.station_set.values_list('matrix_index', flat=True))

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

# функция создания speed_matrix "с кешем"
def get_speed_matrix():
    s_m__txt = os.path.join(PROJECT_ROOT, 'speed_matrix.txt')
    max_station_timestamp = Station.objects.all().aggregate(Max('timestamp'))
    max_route_timestamp = Route.objects.all().aggregate(Max('timestamp'))
    max_transport_timestamp = Transport.objects.all().aggregate(Max('timestamp'))
    max_metastation_timestamp = Metastation.objects.all().aggregate(Max('timestamp'))
    max_timestamp = max(max_metastation_timestamp, max_station_timestamp, max_route_timestamp, max_transport_timestamp)
    max_timestamp = max_timestamp['timestamp__max']
    sm_file = os.path.getmtime(s_m__txt)
    stat = os.stat(s_m__txt)
    file_size = stat.st_size
    timestamp = datetime.datetime.fromtimestamp(sm_file)

    if timestamp < max_timestamp or file_size == 0:
        speed_matrix = new_speed_matrix()

    else:
        fp = open(s_m__txt, 'r')
        read_file = fp.read()
        speed_matrix = eval(read_file)
        fp.close()            

    return speed_matrix

# функция создания списка растояний от start
def get_lenth_start(start_y_rad, start_x_rad):
    speed_Pesh = 3.0
    R = 6376 # радиус земли
    all_station_list = Station.objects.values('coordinate_x', 'coordinate_y').order_by('matrix_index')
    lenth_start = list()
    for station_item in all_station_list:
        coordinate_x = float(station_item['coordinate_x'])*pi/180
        coordinate_y = float(station_item['coordinate_y'])*pi/180
        l_s = acos(sin(start_y_rad)*sin(coordinate_y) + cos(start_y_rad)*cos(coordinate_y)*cos(coordinate_x-start_x_rad))*R / speed_Pesh
        lenth_start += [l_s]
    return lenth_start

# функция создания списка растояний от finish
def get_lenth_finish(finish_y_rad, finish_x_rad):
    speed_Pesh = 3.0
    R = 6376 # радиус земли
    all_station_list = Station.objects.values('coordinate_x', 'coordinate_y').order_by('matrix_index')
    lenth_finish = list()
    for station_item in all_station_list:
        coordinate_x = float(station_item['coordinate_x'])*pi/180
        coordinate_y = float(station_item['coordinate_y'])*pi/180
        l_s = acos(sin(finish_y_rad)*sin(coordinate_y) + cos(finish_y_rad)*cos(coordinate_y)*cos(coordinate_x-finish_x_rad))*R / speed_Pesh
        lenth_finish += [l_s]
    return lenth_finish

#ф-ия нахождения х(иксов) всех станций "с кешем"
def get_all_x():
    x_txt = os.path.join(PROJECT_ROOT, 'all_x.txt')
    max_station_timestamp = Station.objects.all().aggregate(Max('timestamp'))
    max_route_timestamp = Route.objects.all().aggregate(Max('timestamp'))
    max_transport_timestamp = Transport.objects.all().aggregate(Max('timestamp'))
    max_metastation_timestamp = Metastation.objects.all().aggregate(Max('timestamp'))
    max_timestamp = max(max_metastation_timestamp, max_station_timestamp, max_route_timestamp, max_transport_timestamp)
    max_timestamp = max_timestamp['timestamp__max']
    sm_file = os.path.getmtime(x_txt)
    stat = os.stat(x_txt)
    file_size = stat.st_size
    timestamp = datetime.datetime.fromtimestamp(sm_file)

    if timestamp < max_timestamp or file_size == 0:
        all_station_list = Station.objects.values('coordinate_x').order_by('matrix_index')
        all_station_x = list()
        for station_item in all_station_list:
            coordinate_x = float(station_item['coordinate_x'])
            all_station_x += [coordinate_x]

        fp = open(x_txt, 'w')
        fp.write(repr(all_station_x))
        fp.close()
    else:
        fp = open(x_txt, 'r')
        read_file = fp.read()
        all_station_x = eval(read_file)
        fp.close()            

    return all_station_x

# нахождение точек в радиусе старта
def get_points_in_radius_start(sx2, sx1, sy1, sy2, all_station_x):
    radius_x_start, points_in_radius_start = list(), list()
    for station_x in all_station_x:
        if sx2 < station_x < sx1:
            radius_x_start += [station_x]
    for x_start in radius_x_start:
        station_for_y = Station.objects.filter(coordinate_x=x_start).values_list('coordinate_y', 'matrix_index').order_by('matrix_index')
        for station_y in station_for_y:
            if sy2 < station_y[0] < sy1:
                points_in_radius_start += [station_y[1]]
    return list(set(points_in_radius_start))

# нахождение точек в радиусе финиша
def get_points_in_radius_finish(fx2, fx1, fy1, fy2, all_station_x):
    radius_x_finish, points_in_radius_finish = list(), list()
    for station_x in all_station_x:
        if fx2 < station_x < fx1:
            radius_x_finish += [station_x]
    for x_finish in radius_x_finish:
        station_for_y = Station.objects.filter(coordinate_x=x_finish).values_list('coordinate_y', 'matrix_index').order_by('matrix_index')
        for station_y in station_for_y:
            if fy2 < station_y[0] < fy1:
                points_in_radius_finish += [station_y[1]]
    return list(set(points_in_radius_finish))

#ф-ия добавления переходов от точек старта и финиша до точек их радиуса
def get_metastations_stations_list(points_in_radius_finish, points_in_radius_start, start_point, end_point):
    metastations_stations_list = new_Metastation()

    for point_in_radius in points_in_radius_start:
        that = list()
        that += [start_point]
        that += [point_in_radius]
        metastations_stations_list += [that]

    for point_in_radius in points_in_radius_finish:
        thet = list()
        thet += [end_point]
        thet += [point_in_radius]
        metastations_stations_list += [thet]

    return metastations_stations_list

def new_Metastation():
    metastation_txt = os.path.join(PROJECT_ROOT, 'metastation.txt')
    max_station_timestamp = Station.objects.all().aggregate(Max('timestamp'))
    max_route_timestamp = Route.objects.all().aggregate(Max('timestamp'))
    max_transport_timestamp = Transport.objects.all().aggregate(Max('timestamp'))
    max_metastation_timestamp = Metastation.objects.all().aggregate(Max('timestamp'))
    max_timestamp = max(max_metastation_timestamp, max_station_timestamp, max_route_timestamp, max_transport_timestamp)
    max_timestamp = max_timestamp['timestamp__max']
    sm_file = os.path.getmtime(metastation_txt)
    stat = os.stat(metastation_txt)
    file_size = stat.st_size
    timestamp = datetime.datetime.fromtimestamp(sm_file)

    if timestamp < max_timestamp or file_size == 0:
        Metastat = list()
        Radius = 0.004
        for station in Station.objects.values_list('matrix_index', flat=True).order_by('id'):
            station_x = Station.objects.get(matrix_index=station).coordinate_x
            station_y = Station.objects.get(matrix_index=station).coordinate_y
            x1 = station_x - Radius
            x2 = station_x + Radius
            y1 = station_y - Radius
            y2 = station_y + Radius
            all_x = get_all_x()
            radius_x, points_in_radius = list(), list()
            for xs in all_x:
                if x1< xs < x2:
                    radius_x += [xs]
            for x_st in radius_x:
                station_for_y = Station.objects.filter(coordinate_x=x_st).values_list('coordinate_y', 'matrix_index').order_by('matrix_index')
                for sy in station_for_y:
                    if y1 < sy[0] < y2:
                        points_in_radius += [sy[1]]
            points_in_radius = list(set(points_in_radius))
            for point in points_in_radius:
                if point != station:
                    para_point = list()
                    para_point += [station]
                    para_point += [point]
                    if len(para_point) == 2:
                        Metastat += [para_point]
        fp = open(metastation_txt, 'w')
        fp.write(repr(Metastat))
        fp.close()
    else:
        fp = open(metastation_txt, 'r')
        read_file = fp.read()
        Metastat = eval(read_file)
        fp.close()            

    return Metastat

def new_speed_matrix():
    Metastation = new_Metastation()
    wating_index = 1/2.0
    speed_Pesh = 3.0
    points_list = Station.objects.values_list('coordinate_x', 'coordinate_y').order_by('matrix_index')
    len_points = len(points_list)
    speed_matrix = [[0] * len_points  for i in range(len_points)]

    routes_dict, routes_intevals, routes_speeds = dict(), dict(), dict()
    for route_item in Route.objects.all():
        routes_dict[route_item.id] = list(route_item.station_set.values_list('matrix_index', flat=True).order_by('matrix_index'))
        routes_speeds[route_item.id] = route_item.speed
        routes_intevals[route_item.id] = route_item.interval

    for para in Metastation:
        route_interval_time = routes_intevals[Station.objects.get(matrix_index=para[1]).route_id]
        wait_interval = route_interval_time * wating_index
        stationx1 = Station.objects.get(matrix_index=para[0]).coordinate_x
        stationy1 = Station.objects.get(matrix_index=para[0]).coordinate_y
        stationx2 = Station.objects.get(matrix_index=para[1]).coordinate_x
        stationy2 = Station.objects.get(matrix_index=para[1]).coordinate_y
        if stationy1 != stationy2 and stationx1 != stationx2:
            station0 = [stationx1, stationy1]
            station1 = [stationx2, stationy2]
            speed_matrix[para[0]][para[1]] = len_witput_points(station0, station1) / speed_Pesh + wait_interval
        else:
            speed_matrix[para[0]][para[1]] = wait_interval

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
                                                                                     points_list[to_matrix_index]) / route_speed + 0.01

    fp = open(os.path.join(PROJECT_ROOT, 'speed_matrix.txt'), 'w')
    fp.write(repr(speed_matrix))
    fp.close()

    return speed_matrix

                                        #функция нахождения соседних точек

def points_list(points_in_radius_finish, points_in_radius_start, start_point, end_point):
             # заполняем routes_dict, routes_speeds, routes_intevals
    routes_dict = dict()
    points_list_item = list()
    for route_item in Route.objects.all():
        routes_dict[route_item.id] = list(route_item.station_set.values_list('matrix_index', flat=True).order_by('matrix_index'))
        for route_id in routes_dict:
            list2 = routes_dict[route_id]
            points_list_item += [list2]

    for point_in_radius in points_in_radius_start:
        that = list()
        that += [start_point]
        that += [point_in_radius]
        points_list_item += [that]

    for point_in_radius in points_in_radius_finish:
        thet = list()
        thet += [end_point]
        thet += [point_in_radius]
        points_list_item += [thet]

    return points_list_item

#функция нахождения соседних точек
def get_border_points(points_price_min, closed_points_list, points_list_item, metastations_stations_list):
    points_list = list()
    for list_item in points_list_item:
        len_list_item = len(list_item)
        if points_price_min in list_item:
            index_in_list = list_item.index(points_price_min)
            if index_in_list < len_list_item - 1:
                right_border_index = list_item[index_in_list + 1]
                if right_border_index not in closed_points_list:
                    points_list += [right_border_index]

            if index_in_list > 0:
                left_border_index = list_item[index_in_list - 1]
                if left_border_index not in closed_points_list:
                    points_list += [left_border_index]

            for metastation in metastations_stations_list:
                if points_price_min == metastation[0] and metastation[1] not in closed_points_list:
                    points_list += [metastation[1]]
                if points_price_min == metastation[1] and metastation[0] not in closed_points_list:
                    points_list += [metastation[0]]

    return list(set(points_list))

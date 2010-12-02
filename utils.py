#!/usr/bin/env python
# -*- coding: utf-8 -*-


from math import *
from apps.point.models import Route, Station, Metastation, Transport
from django.db.models import Max
import os
import datetime


R = 6376 # радиус земли
speed_Pesh = 3.0

#ф-ия построения нулевой speed_matrix
def S_M():
    points_list = Station.objects.values_list('coordinate_x', 'coordinate_y').order_by('id')
    len_points = len(points_list)
    speed_matrix = [[0] * len_points  for i in range(len_points)]
    return speed_matrix

speed_matrix = S_M

# функция нахождения растояния по шаровым координатам
def len_witput_points(start_point, end_point):
    lenth = acos(sin(start_point[1])*sin(end_point[1]) + cos(start_point[1])*cos(end_point[1])*cos(end_point[0]-start_point[0]))*R
    return lenth

#функция нахождения соседних точек
def get_border_points(points_price_min, closed_points_list, metastations_stations_list):

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

# функция создания speed_matrix
def get_speed_matrix():
    wating_index = 1/2.0
    points_list = Station.objects.values_list('coordinate_x', 'coordinate_y').order_by('id')
    len_points = len(points_list)
    speed_matrix = [[0] * len_points  for i in range(len_points)]
    max_station_timestamp = Station.objects.all().aggregate(Max('timestamp'))
    max_route_timestamp = Route.objects.all().aggregate(Max('timestamp'))
    max_transport_timestamp = Transport.objects.all().aggregate(Max('timestamp'))
    max_metastation_timestamp = Metastation.objects.all().aggregate(Max('timestamp'))
    max_timestamp = max(max_metastation_timestamp, max_station_timestamp, max_route_timestamp, max_transport_timestamp)
    max_timestamp = max_timestamp['timestamp__max']
    sm_file = os.path.getmtime('speed_matrix.txt')
    stat = os.stat('speed_matrix.txt')
    file_size = stat.st_size
    timestamp = datetime.datetime.fromtimestamp(sm_file)
    if timestamp < max_timestamp or file_size == 0:

               # заполняем routes_dict, routes_speeds, routes_intevals
        routes_dict, routes_intevals, routes_speeds = dict(), dict(), dict()
        for route_item in Route.objects.all():
            routes_dict[route_item.id] = list(route_item.station_set.values_list('matrix_index', flat=True))
            routes_speeds[route_item.id] = route_item.speed
            routes_intevals[route_item.id] = route_item.interval

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

                # заполняем список точек пересадок metastations_stations_list
        metastations_stations_list = list()
        for metastation_item in Metastation.objects.all():
            metastation_station_set = list(metastation_item.station_set.values_list('matrix_index', flat=True))
            metastations_stations_list += [metastation_station_set]

                # добавление в speed_matrix переходов по метастанциям
        for item_metastation_stations_list in metastations_stations_list:
            for item_station_from in item_metastation_stations_list:
                for item_station_to in item_metastation_stations_list:
                    route_interval_time = routes_intevals[Station.objects.get(matrix_index=item_station_to).route_id]
                    speed_matrix[item_station_from][item_station_to] = route_interval_time * wating_index
        fp = open('speed_matrix.txt', 'r+')
        fp.write(repr(speed_matrix))
        fp.close()
    else:
        fp = open('speed_matrix.txt', 'r')
        read_file = fp.read()
        speed_matrix = eval(read_file)
        fp.close()            

    return speed_matrix

# функция создания списка растояний от start
def get_lenth_start(start_y_rad, start_x_rad):
    all_station_list = Station.objects.values('coordinate_x', 'coordinate_y').order_by('matrix_index')
    lenth_start = list()
    for station_item in all_station_list:
        coordinate_x = float(station_item['coordinate_x'])*pi/180
        coordinate_y = float(station_item['coordinate_y'])*pi/180
        l_s = acos(sin(start_y_rad)*sin(coordinate_y) + cos(start_y_rad)*cos(coordinate_y)*cos(coordinate_x-start_x_rad))*R/speed_Pesh
        lenth_start += [l_s]
    return lenth_start

# функция создания списка растояний от finish
def get_lenth_finish(finish_y_rad, finish_x_rad):
    all_station_list = Station.objects.values('coordinate_x', 'coordinate_y').order_by('matrix_index')
    lenth_finish = list()
    for station_item in all_station_list:
        coordinate_x = float(station_item['coordinate_x'])*pi/180
        coordinate_y = float(station_item['coordinate_y'])*pi/180
        l_s = acos(sin(finish_y_rad)*sin(coordinate_y) + cos(finish_y_rad)*cos(coordinate_y)*cos(coordinate_x-finish_x_rad))*R/speed_Pesh
        lenth_finish += [l_s]
    return lenth_finish

#ф-ия нахождения х(иксов) всех станций
def get_all_x():
    all_station_list = Station.objects.values('coordinate_x').order_by('matrix_index')
    all_station_x = list()
    for station_item in all_station_list:
        coordinate_x = float(station_item['coordinate_x'])
        all_station_x += [coordinate_x]
    return all_station_x

# нахождение точек в радиусе старта
def get_points_in_radius_start(sx2, sx1, sy1, sy2, all_station_x):
    radius_x_start, points_in_radius_start = list(), list()
    for station_x in all_station_x:
        if sx2 < station_x < sx1:
            radius_x_start += [station_x]
    for x_start in radius_x_start:
        station_for_y = Station.objects.filter(coordinate_x=x_start).values_list('coordinate_y', 'matrix_index')
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
        station_for_y = Station.objects.filter(coordinate_x=x_finish).values_list('coordinate_y', 'matrix_index')
        for station_y in station_for_y:
            if fy2 < station_y[0] < fy1:
                points_in_radius_finish += [station_y[1]]
    return list(set(points_in_radius_finish))

#ф-ия добавления переходов от точек старта и финиша до точек их радиуса
def get_metastations_stations_list(points_in_radius_finish, points_in_radius_start, start_point, end_point):
    metastations_stations_list = list()
    for metastation_item in Metastation.objects.all():
        metastation_station_set = list(metastation_item.station_set.values_list('matrix_index', flat=True))
        metastations_stations_list += [metastation_station_set]

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

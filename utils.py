#!/usr/bin/env python
# -*- coding: utf-8 -*-
from settings import PROJECT_ROOT
from math import *
from apps.point.models import Route, Station, Transport, Onestation
from django.db.models import Max
import os, datetime


# функция нахождения cумы

def sum(seq):

    def add(x, y):
        return x+y
    return reduce(add, seq, 0)


# функция нахождения растояния по шаровым координатам

def len_witput_points(start_point, end_point):
    R = 6376 # радиус земли
    sp1 = start_point[1]*pi/180
    ep1 = end_point[1]*pi/180
    sp0 = start_point[0]*pi/180
    ep0 = end_point[0]*pi/180
    lenth = acos(sin(sp1)*sin(ep1) + cos(sp1)*cos(ep1)*cos(ep0-sp0))*R
    return lenth


# функция создания speed_matrix "с кешем"

def get_speed_matrix(Transport1, Transport2, Transport3, Transport4):
    s_m__txt = os.path.join(PROJECT_ROOT, 'kesh2/speed_matrix.txt')
    s_m__txt1 = os.path.join(PROJECT_ROOT, 'kesh2/speed_matrix1.txt')
    s_m__txt2 = os.path.join(PROJECT_ROOT, 'kesh2/speed_matrix2.txt')
    s_m__txt3 = os.path.join(PROJECT_ROOT, 'kesh2/speed_matrix3.txt')
    s_m__txt4 = os.path.join(PROJECT_ROOT, 'kesh2/speed_matrix4.txt')
    s_m__txt12 = os.path.join(PROJECT_ROOT, 'kesh2/speed_matrix12.txt')
    s_m__txt13 = os.path.join(PROJECT_ROOT, 'kesh2/speed_matrix13.txt')
    s_m__txt14 = os.path.join(PROJECT_ROOT, 'kesh2/speed_matrix14.txt')
    s_m__txt23 = os.path.join(PROJECT_ROOT, 'kesh2/speed_matrix23.txt')
    s_m__txt24 = os.path.join(PROJECT_ROOT, 'kesh2/speed_matrix24.txt')
    s_m__txt34 = os.path.join(PROJECT_ROOT, 'kesh2/speed_matrix34.txt')
    s_m__txt123 = os.path.join(PROJECT_ROOT, 'kesh2/speed_matrix123.txt')
    s_m__txt124 = os.path.join(PROJECT_ROOT, 'kesh2/speed_matrix124.txt')
    s_m__txt134 = os.path.join(PROJECT_ROOT, 'kesh2/speed_matrix134.txt')
    s_m__txt234 = os.path.join(PROJECT_ROOT, 'kesh2/speed_matrix234.txt')
    max_station_timestamp = Station.objects.all().aggregate(Max('timestamp'))
    max_route_timestamp = Route.objects.all().aggregate(Max('timestamp'))
    max_transport_timestamp = Transport.objects.all().aggregate(Max('timestamp'))
    max_onestation_timestamp = Onestation.objects.all().aggregate(Max('timestamp'))
    max_timestamp = max(max_onestation_timestamp, max_station_timestamp, max_route_timestamp, max_transport_timestamp)
    max_timestamp = max_timestamp['timestamp__max']
    if os.path.isfile(s_m__txt) == False:
        open(s_m__txt, 'w')
    if os.path.isfile(s_m__txt1) == False:
        open(s_m__txt1, 'w')
    if os.path.isfile(s_m__txt2) == False:
        open(s_m__txt2, 'w')
    if os.path.isfile(s_m__txt3) == False:
        open(s_m__txt3, 'w')
    if os.path.isfile(s_m__txt4) == False:
        open(s_m__txt4, 'w')
    if os.path.isfile(s_m__txt12) == False:
        open(s_m__txt12, 'w')
    if os.path.isfile(s_m__txt13) == False:
        open(s_m__txt13, 'w')
    if os.path.isfile(s_m__txt14) == False:
        open(s_m__txt14, 'w')
    if os.path.isfile(s_m__txt23) == False:
        open(s_m__txt23, 'w')
    if os.path.isfile(s_m__txt24) == False:
        open(s_m__txt24, 'w')
    if os.path.isfile(s_m__txt34) == False:
        open(s_m__txt34, 'w')
    if os.path.isfile(s_m__txt123) == False:
        open(s_m__txt123, 'w')
    if os.path.isfile(s_m__txt124) == False:
        open(s_m__txt124, 'w')
    if os.path.isfile(s_m__txt134) == False:
        open(s_m__txt134, 'w')
    if os.path.isfile(s_m__txt234) == False:
        open(s_m__txt234, 'w')
    sm_file = os.path.getmtime(s_m__txt)
    stat = os.stat(s_m__txt)
    file_size = stat.st_size
    timestamp = datetime.datetime.fromtimestamp(sm_file)

    if timestamp < max_timestamp or file_size == 0:
        if Transport1 == 0 and Transport2 == 0 and Transport3 == 0 and Transport4 == 0:
            speed_matrix = new_speed_matrix(Transport1, Transport2, Transport3, Transport4)
            fp = open(s_m__txt, 'w')
            fp.write(repr(speed_matrix))
            fp.close()
        if Transport1 == 0 and Transport2 == 1 and Transport3 == 1 and Transport4 == 1:
            speed_matrix = new_speed_matrix(Transport1, Transport2, Transport3, Transport4)
            fp = open(s_m__txt1, 'w')
            fp.write(repr(speed_matrix))
            fp.close()
        if Transport1 == 1 and Transport2 == 0 and Transport3 == 1 and Transport4 == 1:
            speed_matrix = new_speed_matrix(Transport1, Transport2, Transport3, Transport4)
            fp = open(s_m__txt2, 'w')
            fp.write(repr(speed_matrix))
            fp.close()
        if Transport1 == 1 and Transport2 == 1 and Transport3 == 0 and Transport4 == 1:
            speed_matrix = new_speed_matrix(Transport1, Transport2, Transport3, Transport4)
            fp = open(s_m__txt3, 'w')
            fp.write(repr(speed_matrix))
            fp.close()
        if Transport1 == 1 and Transport2 == 1 and Transport3 == 1 and Transport4 == 0:
            speed_matrix = new_speed_matrix(Transport1, Transport2, Transport3, Transport4)
            fp = open(s_m__txt4, 'w')
            fp.write(repr(speed_matrix))
            fp.close()
        if Transport1 == 0 and Transport2 == 0 and Transport3 == 1 and Transport4 == 1:
            speed_matrix = new_speed_matrix(Transport1, Transport2, Transport3, Transport4)
            fp = open(s_m__txt12, 'w')
            fp.write(repr(speed_matrix))
            fp.close()
        if Transport1 == 0 and Transport2 == 1 and Transport3 == 0 and Transport4 == 1:
            speed_matrix = new_speed_matrix(Transport1, Transport2, Transport3, Transport4)
            fp = open(s_m__txt13, 'w')
            fp.write(repr(speed_matrix))
            fp.close()
        if Transport1 == 0 and Transport2 == 1 and Transport3 == 1 and Transport4 == 0:
            speed_matrix = new_speed_matrix(Transport1, Transport2, Transport3, Transport4)
            fp = open(s_m__txt14, 'w')
            fp.write(repr(speed_matrix))
            fp.close()
        if Transport1 == 1 and Transport2 == 0 and Transport3 == 0 and Transport4 == 1:
            speed_matrix = new_speed_matrix(Transport1, Transport2, Transport3, Transport4)
            fp = open(s_m__txt23, 'w')
            fp.write(repr(speed_matrix))
            fp.close()
        if Transport1 == 1 and Transport2 == 0 and Transport3 == 1 and Transport4 == 0:
            speed_matrix = new_speed_matrix(Transport1, Transport2, Transport3, Transport4)
            fp = open(s_m__txt24, 'w')
            fp.write(repr(speed_matrix))
            fp.close()
        if Transport1 == 1 and Transport2 == 1 and Transport3 == 0 and Transport4 == 0:
            speed_matrix = new_speed_matrix(Transport1, Transport2, Transport3, Transport4)
            fp = open(s_m__txt34, 'w')
            fp.write(repr(speed_matrix))
            fp.close()
        if Transport1 == 0 and Transport2 == 0 and Transport3 == 0 and Transport4 == 1:
            speed_matrix = new_speed_matrix(Transport1, Transport2, Transport3, Transport4)
            fp = open(s_m__txt123, 'w')
            fp.write(repr(speed_matrix))
            fp.close()
        if Transport1 == 0 and Transport2 == 0 and Transport3 == 1 and Transport4 == 0:
            speed_matrix = new_speed_matrix(Transport1, Transport2, Transport3, Transport4)
            fp = open(s_m__txt124, 'w')
            fp.write(repr(speed_matrix))
            fp.close()
        if Transport1 == 0 and Transport2 == 1 and Transport3 == 0 and Transport4 == 0:
            speed_matrix = new_speed_matrix(Transport1, Transport2, Transport3, Transport4)
            fp = open(s_m__txt134, 'w')
            fp.write(repr(speed_matrix))
            fp.close()
        if Transport1 == 1 and Transport2 == 0 and Transport3 == 0 and Transport4 == 0:
            speed_matrix = new_speed_matrix(Transport1, Transport2, Transport3, Transport4)
            fp = open(s_m__txt234, 'w')
            fp.write(repr(speed_matrix))
            fp.close()

    else:
        if Transport1 == 0 and Transport2 == 0 and Transport3 == 0 and Transport4 == 0:
            fp = open(s_m__txt, 'r')
            read_file = fp.read()
            speed_matrix = eval(read_file)
            fp.close()
        if Transport1 == 0 and Transport2 == 1 and Transport3 == 1 and Transport4 == 1:
            fp = open(s_m__txt1, 'r')
            read_file = fp.read()
            speed_matrix = eval(read_file)
            fp.close()
        if Transport1 == 1 and Transport2 == 0 and Transport3 == 1 and Transport4 == 1:
            fp = open(s_m__txt2, 'r')
            read_file = fp.read()
            speed_matrix = eval(read_file)
            fp.close()
        if Transport1 == 1 and Transport2 == 1 and Transport3 == 0 and Transport4 == 1:
            fp = open(s_m__txt3, 'r')
            read_file = fp.read()
            speed_matrix = eval(read_file)
            fp.close()
        if Transport1 == 1 and Transport2 == 1 and Transport3 == 1 and Transport4 == 0:
            fp = open(s_m__txt4, 'r')
            read_file = fp.read()
            speed_matrix = eval(read_file)
            fp.close()
        if Transport1 == 0 and Transport2 == 0 and Transport3 == 1 and Transport4 == 1:
            fp = open(s_m__txt12, 'r')
            read_file = fp.read()
            speed_matrix = eval(read_file)
            fp.close()
        if Transport1 == 0 and Transport2 == 1 and Transport3 == 0 and Transport4 == 1:
            fp = open(s_m__txt13, 'r')
            read_file = fp.read()
            speed_matrix = eval(read_file)
            fp.close()
        if Transport1 == 0 and Transport2 == 1 and Transport3 == 1 and Transport4 == 0:
            fp = open(s_m__txt14, 'r')
            read_file = fp.read()
            speed_matrix = eval(read_file)
            fp.close()
        if Transport1 == 1 and Transport2 == 0 and Transport3 == 0 and Transport4 == 1:
            fp = open(s_m__txt23, 'r')
            read_file = fp.read()
            speed_matrix = eval(read_file)
            fp.close()
        if Transport1 == 1 and Transport2 == 0 and Transport3 == 1 and Transport4 == 0:
            fp = open(s_m__txt24, 'r')
            read_file = fp.read()
            speed_matrix = eval(read_file)
            fp.close()
        if Transport1 == 1 and Transport2 == 1 and Transport3 == 0 and Transport4 == 0:
            fp = open(s_m__txt34, 'r')
            read_file = fp.read()
            speed_matrix = eval(read_file)
            fp.close()
        if Transport1 == 0 and Transport2 == 0 and Transport3 == 0 and Transport4 == 1:
            fp = open(s_m__txt123, 'r')
            read_file = fp.read()
            speed_matrix = eval(read_file)
            fp.close()
        if Transport1 == 0 and Transport2 == 0 and Transport3 == 1 and Transport4 == 0:
            fp = open(s_m__txt124, 'r')
            read_file = fp.read()
            speed_matrix = eval(read_file)
            fp.close()
        if Transport1 == 0 and Transport2 == 1 and Transport3 == 0 and Transport4 == 0:
            fp = open(s_m__txt134, 'r')
            read_file = fp.read()
            speed_matrix = eval(read_file)
            fp.close()
        if Transport1 == 1 and Transport2 == 0 and Transport3 == 0 and Transport4 == 0:
            fp = open(s_m__txt234, 'r')
            read_file = fp.read()
            speed_matrix = eval(read_file)
            fp.close()

    return speed_matrix


def new_speed_matrix(Transport1, Transport2, Transport3, Transport4):
    Metastation = new_Metastation(Transport1, Transport2, Transport3, Transport4)
    wating_index = 1/2.0
    speed_Pesh = 3.0
#-------------------------------------------------------------------------------------------------------------------    
    all_station_list = get_dict_x_y()
    index_start = list()
    for station_item in all_station_list:
        lenth_start = list()
        transport = Station.objects.get(matrix_index=station_item['matrix_index']).route.transport_type_id
        if Transport1 == 0 and transport == 1:
            lenth_start += [station_item['matrix_index']]
            lenth_start += [float(station_item['coordinate_x'])]
            lenth_start += [float(station_item['coordinate_y'])]
            index_start += [lenth_start]
        if Transport2 == 0 and transport == 2:
            lenth_start += [station_item['matrix_index']]
            lenth_start += [float(station_item['coordinate_x'])]
            lenth_start += [float(station_item['coordinate_y'])]
            index_start += [lenth_start]
        if Transport3 == 0 and transport == 3:
            lenth_start += [station_item['matrix_index']]
            lenth_start += [float(station_item['coordinate_x'])]
            lenth_start += [float(station_item['coordinate_y'])]
            index_start += [lenth_start]
        if Transport4 == 0 and transport == 4:
            lenth_start += [station_item['matrix_index']]
            lenth_start += [float(station_item['coordinate_x'])]
            lenth_start += [float(station_item['coordinate_y'])]
            index_start += [lenth_start]
#-------------------------------------------------------------------------------------------------------------------    
    points_list = Station.objects.filter(notstations=True).values_list('coordinate_x', 'coordinate_y').order_by('matrix_index')
    len_points = len(points_list)
    speed_matrix = [[0] * len_points  for i in range(len_points)]
    tr_type = list()
    routes_dict, routes_intevals, routes_speeds = dict(), dict(), dict()
    if Transport1 == 0:
        tr_type += [1]
    if Transport2 == 0:
        tr_type += [2]
    if Transport3 == 0:
        tr_type += [3]
    if Transport4 == 0:
        tr_type += [4]

    for route_item in Route.objects.filter(transport_type__in=tr_type):
        routes_dict[route_item.id] = list(route_item.station_set.values_list('matrix_index', flat=True).order_by('order'))
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
        langs_traector = 0
        traector_list_to = list()
        traector_list_from = list()
        route_speed = float(routes_speeds[route_id])
        for item_index in range(len(route_item_list)):
            next_item_index = item_index + 1
            if next_item_index == len(route_item_list):
                break

            from_matrix_index = route_item_list[item_index]
            to_matrix_index = route_item_list[next_item_index]
            if langs_traector != 0 and from_matrix_index != -1:
                langs_traector = 0
                traector_list_to = list()
                traector_list_from = list()
            if to_matrix_index == -1 or from_matrix_index == -1:
                q = Station.objects.filter(route=route_id, order=next_item_index).values_list('coordinate_x', 'coordinate_y')
                a = Station.objects.filter(route=route_id, order=item_index).values_list('coordinate_x', 'coordinate_y')
                qa = len_witput_points(q[0], a[0]) / route_speed
                langs_traector += qa
                traector_list_to += [to_matrix_index]
                traector_list_from += [from_matrix_index]
                if to_matrix_index != -1:
                    speed_matrix[traector_list_to[-1]][traector_list_from[0]] = \
                        speed_matrix[traector_list_from[0]][traector_list_to[-1]] = langs_traector + 0.01

            if  to_matrix_index != -1 and from_matrix_index != -1:
                speed_matrix[to_matrix_index][from_matrix_index] = \
                    speed_matrix[from_matrix_index][to_matrix_index] = len_witput_points(points_list[from_matrix_index],
                                                                                         points_list[to_matrix_index]) / route_speed + 0.01

    for m_list in speed_matrix:
        if sum(m_list) == 0:
            speed_matrix[speed_matrix.index(m_list)] = []

    return speed_matrix


#ф-ия нахождения х(иксов) всех станций "с кешем"

def get_all_x():
    x_txt = os.path.join(PROJECT_ROOT, 'kesh/all_x.txt')
    max_station_timestamp = Station.objects.all().aggregate(Max('timestamp'))
    max_route_timestamp = Route.objects.all().aggregate(Max('timestamp'))
    max_transport_timestamp = Transport.objects.all().aggregate(Max('timestamp'))
    max_onestation_timestamp = Onestation.objects.all().aggregate(Max('timestamp'))
    max_timestamp = max(max_onestation_timestamp, max_station_timestamp, max_route_timestamp, max_transport_timestamp)
    max_timestamp = max_timestamp['timestamp__max']
    if os.path.isfile(x_txt) == False:
        open(x_txt, 'w')
    sm_file = os.path.getmtime(x_txt)
    stat = os.stat(x_txt)
    file_size = stat.st_size
    timestamp = datetime.datetime.fromtimestamp(sm_file)

    if timestamp < max_timestamp or file_size == 0:
        all_station_list = Station.objects.filter(notstations=True).values('coordinate_x').order_by('id')
        all_station_x = list()
        for station_item in all_station_list:
            coordinate_x = float(station_item['coordinate_x'])
            all_station_x += [coordinate_x]

        fp = open(x_txt, "w")
        fp.write(repr(all_station_x))
        fp.close()
    else:
        fp = open(x_txt, 'r')
        read_file = fp.read()
        all_station_x = eval(read_file)
        fp.close()

    return all_station_x

# нахождение точек в радиусе старта

def get_points_in_radius_start(sx2, sx1, sy1, sy2, all_station_x, Transport1, Transport2, Transport3, Transport4):
    radius_x_start, points_in_radius_start = list(), list()
    for station_x in all_station_x:
        if sx2 < station_x < sx1:
            radius_x_start += [station_x]
    for x_start in radius_x_start:
        station_for_y = Station.objects.filter(coordinate_x=x_start, notstations=True).values_list('coordinate_y', 'matrix_index')
        for station_y in station_for_y:
            if sy2 < station_y[0] < sy1:
                transport = Station.objects.get(matrix_index=station_y[1]).route.transport_type_id
                if Transport1 == 0 and transport == 1:
                    points_in_radius_start += [station_y[1]]
                if Transport2 == 0 and transport == 2:
                    points_in_radius_start += [station_y[1]]
                if Transport3 == 0 and transport == 3:
                    points_in_radius_start += [station_y[1]]
                if Transport4 == 0 and transport == 4:
                    points_in_radius_start += [station_y[1]]

    return list(set(points_in_radius_start))


# нахождение точек в радиусе финиша

def get_points_in_radius_finish(fx2, fx1, fy1, fy2, all_station_x, Transport1, Transport2, Transport3, Transport4):
    radius_x_finish, points_in_radius_finish = list(), list()
    for station_x in all_station_x:
        if fx2 < station_x < fx1:
            radius_x_finish += [station_x]
    for x_finish in radius_x_finish:
        station_for_y = Station.objects.filter(coordinate_x=x_finish, notstations=True).values_list('coordinate_y', 'matrix_index')
        for station_y in station_for_y:
            if fy2 < station_y[0] < fy1:
                transport = Station.objects.get(matrix_index=station_y[1]).route.transport_type_id
                if Transport1 == 0 and transport == 1:
                    points_in_radius_finish += [station_y[1]]
                if Transport2 == 0 and transport == 2:
                    points_in_radius_finish += [station_y[1]]
                if Transport3 == 0 and transport == 3:
                    points_in_radius_finish += [station_y[1]]
                if Transport4 == 0 and transport == 4:
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


def new_Metastation(Transport1, Transport2, Transport3, Transport4):
    metastation_txt = os.path.join(PROJECT_ROOT, 'kesh2/metastation.txt')
    metastation1_txt = os.path.join(PROJECT_ROOT, 'kesh2/metastation1.txt')
    metastation2_txt = os.path.join(PROJECT_ROOT, 'kesh2/metastation2.txt')
    metastation3_txt = os.path.join(PROJECT_ROOT, 'kesh2/metastation3.txt')
    metastation4_txt = os.path.join(PROJECT_ROOT, 'kesh2/metastation4.txt')
    metastation124_txt = os.path.join(PROJECT_ROOT, 'kesh2/metastation124.txt')
    metastation134_txt = os.path.join(PROJECT_ROOT, 'kesh2/metastation134.txt')
    metastation234_txt = os.path.join(PROJECT_ROOT, 'kesh2/metastation234.txt')
    metastation123_txt = os.path.join(PROJECT_ROOT, 'kesh2/metastation123.txt')
    metastation12_txt = os.path.join(PROJECT_ROOT, 'kesh2/metastation12.txt')
    metastation13_txt = os.path.join(PROJECT_ROOT, 'kesh2/metastation13.txt')
    metastation14_txt = os.path.join(PROJECT_ROOT, 'kesh2/metastation14.txt')
    metastation23_txt = os.path.join(PROJECT_ROOT, 'kesh2/metastation23.txt')
    metastation24_txt = os.path.join(PROJECT_ROOT, 'kesh2/metastation24.txt')
    metastation34_txt = os.path.join(PROJECT_ROOT, 'kesh2/metastation34.txt')
    max_station_timestamp = Station.objects.all().aggregate(Max('timestamp'))
    max_route_timestamp = Route.objects.all().aggregate(Max('timestamp'))
    max_transport_timestamp = Transport.objects.all().aggregate(Max('timestamp'))
    max_onestation_timestamp = Onestation.objects.all().aggregate(Max('timestamp'))
    max_timestamp = max(max_onestation_timestamp, max_station_timestamp, max_route_timestamp, max_transport_timestamp)
    max_timestamp = max_timestamp['timestamp__max']
    if os.path.isfile(metastation_txt) == False:
        open(metastation_txt, 'w')
    if os.path.isfile(metastation1_txt) == False:
        open(metastation1_txt, 'w')
    if os.path.isfile(metastation2_txt) == False:
        open(metastation2_txt, 'w')
    if os.path.isfile(metastation3_txt) == False:
        open(metastation3_txt, 'w')
    if os.path.isfile(metastation4_txt) == False:
        open(metastation4_txt, 'w')
    if os.path.isfile(metastation124_txt) == False:
        open(metastation124_txt, 'w')
    if os.path.isfile(metastation134_txt) == False:
        open(metastation134_txt, 'w')
    if os.path.isfile(metastation234_txt) == False:
        open(metastation234_txt, 'w')
    if os.path.isfile(metastation123_txt) == False:
        open(metastation123_txt, 'w')
    if os.path.isfile(metastation12_txt) == False:
        open(metastation12_txt, 'w')
    if os.path.isfile(metastation13_txt) == False:
        open(metastation13_txt, 'w')
    if os.path.isfile(metastation14_txt) == False:
        open(metastation14_txt, 'w')
    if os.path.isfile(metastation23_txt) == False:
        open(metastation23_txt, 'w')
    if os.path.isfile(metastation24_txt) == False:
        open(metastation24_txt, 'w')
    if os.path.isfile(metastation34_txt) == False:
        open(metastation34_txt, 'w')
    sm_file = os.path.getmtime(metastation_txt)
    stat = os.stat(metastation_txt)
    file_size = stat.st_size
    timestamp = datetime.datetime.fromtimestamp(sm_file)

    if timestamp < max_timestamp or file_size == 0:
        Metastat, Metastat1, Metastat2, Metastat3, Metastat4 = list(), list(), list(), list(), list()
        Metastat123, Metastat234, Metastat134, Metastat124 = list(), list(), list(), list()
        Metastat12, Metastat23, Metastat34, Metastat24, Metastat14, Metastat13 = list(), list(), list(), list(), list(), list()
        Radius = 0.004
        for station in Station.objects.filter(notstations=True).values_list('matrix_index', flat=True):
            transport = Station.objects.get(matrix_index=station).route.transport_type_id
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
                station_for_y = Station.objects.filter(coordinate_x=x_st, notstations=True).values_list('coordinate_y', 'matrix_index')
                for sy in station_for_y:
                    if y1 < sy[0] < y2:
                        points_in_radius += [sy[1]]
            points_in_radius = list(set(points_in_radius))
            for point in points_in_radius:
                transport2 = Station.objects.get(matrix_index=point).route.transport_type_id
                if point != station:
                    para_point = list()
                    para_point += [station]
                    para_point += [point]
                    if len(para_point) == 2:
                        Metastat += [para_point]
                        if transport == 1 and transport2 == 1:
                            Metastat1 += [para_point]
                        elif transport == 2 and transport2 == 2:
                            Metastat2 += [para_point]
                        elif transport == 3 and transport2 == 3:
                            Metastat3 += [para_point]
                        elif transport == 4 and transport2 == 4:
                            Metastat4 += [para_point]
                        if transport != 1 and transport2 != 1:
                            Metastat234 += [para_point]
                            if transport != 2 and transport2 != 2:
                                Metastat34 += [para_point]
                            if transport != 3 and transport2 != 3:
                                Metastat24 += [para_point]
                            if transport != 4 and transport2 != 4:
                                Metastat23 += [para_point]

                        if transport != 2 and transport2 != 2:
                            Metastat134 += [para_point]
                            if transport != 4 and transport2 != 4:
                                Metastat14 += [para_point]
                            if transport != 3 and transport2 != 3:
                                Metastat13 += [para_point]

                        if transport != 3 and transport2 != 3:
                            Metastat124 += [para_point]
                            if transport != 4 and transport2 != 4:
                                Metastat12 += [para_point]

                        if transport != 4 and transport2 != 4:
                            Metastat123 += [para_point]

        fp = open(metastation_txt, 'w')
        fp.write(repr(Metastat))
        fp.close()
        fp1 = open(metastation1_txt, 'w')
        fp1.write(repr(Metastat1))
        fp1.close()
        fp2 = open(metastation2_txt, 'w')
        fp2.write(repr(Metastat2))
        fp2.close()
        fp3 = open(metastation3_txt, 'w')
        fp3.write(repr(Metastat3))
        fp3.close()
        fp4 = open(metastation4_txt, 'w')
        fp4.write(repr(Metastat4))
        fp4.close()
        fp124 = open(metastation124_txt, 'w')
        fp124.write(repr(Metastat124))
        fp124.close()
        fp134 = open(metastation134_txt, 'w')
        fp134.write(repr(Metastat134))
        fp134.close()
        fp234 = open(metastation234_txt, 'w')
        fp234.write(repr(Metastat234))
        fp234.close()
        fp123 = open(metastation123_txt, 'w')
        fp123.write(repr(Metastat123))
        fp123.close()
        fp12 = open(metastation12_txt, 'w')
        fp12.write(repr(Metastat12))
        fp12.close()
        fp13 = open(metastation13_txt, 'w')
        fp13.write(repr(Metastat13))
        fp13.close()
        fp14 = open(metastation14_txt, 'w')
        fp14.write(repr(Metastat14))
        fp14.close()
        fp23 = open(metastation23_txt, 'w')
        fp23.write(repr(Metastat23))
        fp23.close()
        fp24 = open(metastation24_txt, 'w')
        fp24.write(repr(Metastat24))
        fp24.close()
        fp34 = open(metastation34_txt, 'w')
        fp34.write(repr(Metastat34))
        fp34.close()

    else:
        if Transport1 == 1 and Transport2 == 0 and Transport3 == 0 and Transport4 == 0:
            fp = open(metastation234_txt, 'r')
            read_file = fp.read()
            Metastat = eval(read_file)
            fp.close()
        if Transport1 == 0 and Transport2 == 1 and Transport3 == 0 and Transport4 == 0:
            fp = open(metastation134_txt, 'r')
            read_file = fp.read()
            Metastat = eval(read_file)
            fp.close()
        if Transport1 == 0 and Transport2 == 0 and Transport3 == 1 and Transport4 == 0:
            fp = open(metastation124_txt, 'r')
            read_file = fp.read()
            Metastat = eval(read_file)
            fp.close()
        if Transport1 == 0 and Transport2 == 0 and Transport3 == 0 and Transport4 == 1:
            fp = open(metastation123_txt, 'r')
            read_file = fp.read()
            Metastat = eval(read_file)
            fp.close()
        if Transport1 == 1 and Transport2 == 1 and Transport3 == 0 and Transport4 == 0:
            fp = open(metastation34_txt, 'r')
            read_file = fp.read()
            Metastat = eval(read_file)
            fp.close()
        if Transport1 == 1 and Transport2 == 0 and Transport3 == 1 and Transport4 == 0:
            fp = open(metastation24_txt, 'r')
            read_file = fp.read()
            Metastat = eval(read_file)
            fp.close()
        if Transport1 == 1 and Transport2 == 0 and Transport3 == 0 and Transport4 == 1:
            fp = open(metastation23_txt, 'r')
            read_file = fp.read()
            Metastat = eval(read_file)
            fp.close()
        if Transport1 == 0 and Transport2 == 1 and Transport3 == 1 and Transport4 == 0:
            fp = open(metastation14_txt, 'r')
            read_file = fp.read()
            Metastat = eval(read_file)
            fp.close()
        if Transport1 == 0 and Transport2 == 1 and Transport3 == 0 and Transport4 == 1:
            fp = open(metastation13_txt, 'r')
            read_file = fp.read()
            Metastat = eval(read_file)
            fp.close()
        if Transport1 == 0 and Transport2 == 0 and Transport3 == 1 and Transport4 == 1:
            fp = open(metastation12_txt, 'r')
            read_file = fp.read()
            Metastat = eval(read_file)
            fp.close()
        if Transport1 == 1 and Transport2 == 1 and Transport3 == 1 and Transport4 == 0:
            fp = open(metastation4_txt, 'r')
            read_file = fp.read()
            Metastat = eval(read_file)
            fp.close()
        if Transport1 == 1 and Transport2 == 1 and Transport3 == 0 and Transport4 == 1:
            fp = open(metastation3_txt, 'r')
            read_file = fp.read()
            Metastat = eval(read_file)
            fp.close()
        if Transport1 == 1 and Transport2 == 0 and Transport3 == 1 and Transport4 == 1:
            fp = open(metastation2_txt, 'r')
            read_file = fp.read()
            Metastat = eval(read_file)
            fp.close()
        if Transport1 == 0 and Transport2 == 1 and Transport3 == 1 and Transport4 == 1:
            fp = open(metastation1_txt, 'r')
            read_file = fp.read()
            Metastat = eval(read_file)
            fp.close()
        if Transport1 == 0 and Transport2 == 0 and Transport3 == 0 and Transport4 == 0:
            fp = open(metastation_txt, 'r')
            read_file = fp.read()
            Metastat = eval(read_file)
            fp.close()

    return Metastat

                                        #функция нахождения соседних точек

def points_list(points_in_radius_finish, points_in_radius_start, start_point, end_point):
    routes_dict = dict()
    points_list_item = list()
    for route_item in Route.objects.all():
        routes_dict[route_item.id] = list(route_item.station_set.filter(notstations=True).values_list('matrix_index', flat=True).order_by('matrix_index'))
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


def new_Metastation2(Transport1, Transport2, Transport3, Transport4):
    metastation_txt = os.path.join(PROJECT_ROOT, 'kesh/metastation.txt')
    max_station_timestamp = Station.objects.all().aggregate(Max('timestamp'))
    max_route_timestamp = Route.objects.all().aggregate(Max('timestamp'))
    max_transport_timestamp = Transport.objects.all().aggregate(Max('timestamp'))
    max_onestation_timestamp = Onestation.objects.all().aggregate(Max('timestamp'))
    max_timestamp = max(max_onestation_timestamp, max_station_timestamp, max_route_timestamp, max_transport_timestamp)
    max_timestamp = max_timestamp['timestamp__max']
    if os.path.isfile(metastation_txt) == False:
        open(metastation_txt, 'w')
    sm_file = os.path.getmtime(metastation_txt)
    stat = os.stat(metastation_txt)
    file_size = stat.st_size
    timestamp = datetime.datetime.fromtimestamp(sm_file)

    if timestamp < max_timestamp or file_size == 0:
        Metastat = list()
        Radius = 0.004
        for station in Station.objects.values_list('matrix_index', flat=True):
            transport = Station.objects.get(matrix_index=station).route.transport_type_id
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
                station_for_y = Station.objects.filter(coordinate_x=x_st).values_list('coordinate_y', 'matrix_index')
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

# Ф-ия необходима при расчёте спид_метрикс

def get_dict_x_y():
    x_y_txt = os.path.join(PROJECT_ROOT, 'kesh2/x_y.txt')
    max_station_timestamp = Station.objects.all().aggregate(Max('timestamp'))
    max_route_timestamp = Route.objects.all().aggregate(Max('timestamp'))
    max_transport_timestamp = Transport.objects.all().aggregate(Max('timestamp'))
    max_onestation_timestamp = Onestation.objects.all().aggregate(Max('timestamp'))
    max_timestamp = max(max_onestation_timestamp, max_station_timestamp, max_route_timestamp, max_transport_timestamp)
    max_timestamp = max_timestamp['timestamp__max']
    if os.path.isfile(x_y_txt) == False:
        open(x_y_txt, 'w')
    sm_file = os.path.getmtime(x_y_txt)
    stat = os.stat(x_y_txt)
    file_size = stat.st_size
    timestamp = datetime.datetime.fromtimestamp(sm_file)

    if timestamp < max_timestamp or file_size == 0:
        all_station_list = list(Station.objects.filter(notstations=True).values('coordinate_x', 'coordinate_y', 'matrix_index').order_by('matrix_index'))
        fp = open(x_y_txt, 'w')
        fp.write(repr(all_station_list))
        fp.close()
    else:
        fp = open(x_y_txt, 'r')
        read_file = fp.read()
        all_station_list = eval(read_file)
        fp.close()

    return all_station_list

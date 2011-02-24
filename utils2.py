#!/usr/bin/env python
# -*- coding: utf-8 -*-
from settings import PROJECT_ROOT
from math import *
from apps.point.models import Route, Station, Transport, Onestation
from django.db.models import Max
import os, datetime



# функция нахождения cумы
def sum(seq):
    def add(x, y): return x+y
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


def get_dict_x_y():
    x_y_txt = os.path.join(PROJECT_ROOT, 'kesh2/x_y.txt')
    fp = open(x_y_txt, 'r')
    read_file = fp.read()
    all_station_list = eval(read_file)
    fp.close()            

    return all_station_list

# функция создания списка растояний от start и от finish
def get_lenth_start_finish(finish_y_rad, finish_x_rad, start_y_rad, start_x_rad, Transport1, Transport2, Transport3, Transport4):
    speed_Pesh = 3.0
    R = 6376 # радиус земли
    len_list_finish_start = list()
    all_station_list = get_dict_x_y()
    len_list_start = [[0] * len(all_station_list)][0]
    len_list_finish = [[0] * len(all_station_list)][0]
    for station_item in all_station_list:
        transport = Station.objects.get(matrix_index=station_item['matrix_index']).route.transport_type_id
        if Transport1 == 0 and transport == 1:
            m_i_s = station_item['matrix_index']
            coordinate_x = float(station_item['coordinate_x'])*pi/180
            coordinate_y = float(station_item['coordinate_y'])*pi/180
            l_s = acos(sin(start_y_rad)*sin(coordinate_y) + cos(start_y_rad)*cos(coordinate_y)*cos(coordinate_x-start_x_rad))*R / speed_Pesh
            len_list_start[m_i_s] = l_s
            l_f = acos(sin(finish_y_rad)*sin(coordinate_y) + cos(finish_y_rad)*cos(coordinate_y)*cos(coordinate_x-finish_x_rad))*R / speed_Pesh
            len_list_finish[m_i_s] = l_f
        if Transport2 == 0 and transport == 2:
            m_i_s = station_item['matrix_index']
            coordinate_x = float(station_item['coordinate_x'])*pi/180
            coordinate_y = float(station_item['coordinate_y'])*pi/180
            l_s = acos(sin(start_y_rad)*sin(coordinate_y) + cos(start_y_rad)*cos(coordinate_y)*cos(coordinate_x-start_x_rad))*R / speed_Pesh
            len_list_start[m_i_s] = l_s
            l_f = acos(sin(finish_y_rad)*sin(coordinate_y) + cos(finish_y_rad)*cos(coordinate_y)*cos(coordinate_x-finish_x_rad))*R / speed_Pesh
            len_list_finish[m_i_s] = l_f
        if Transport3 == 0 and transport == 3:
            m_i_s = station_item['matrix_index']
            coordinate_x = float(station_item['coordinate_x'])*pi/180
            coordinate_y = float(station_item['coordinate_y'])*pi/180
            l_s = acos(sin(start_y_rad)*sin(coordinate_y) + cos(start_y_rad)*cos(coordinate_y)*cos(coordinate_x-start_x_rad))*R / speed_Pesh
            len_list_start[m_i_s] = l_s
            l_f = acos(sin(finish_y_rad)*sin(coordinate_y) + cos(finish_y_rad)*cos(coordinate_y)*cos(coordinate_x-finish_x_rad))*R / speed_Pesh
            len_list_finish[m_i_s] = l_f
        if Transport4 == 0 and transport == 4:
            m_i_s = station_item['matrix_index']
            coordinate_x = float(station_item['coordinate_x'])*pi/180
            coordinate_y = float(station_item['coordinate_y'])*pi/180
            l_s = acos(sin(start_y_rad)*sin(coordinate_y) + cos(start_y_rad)*cos(coordinate_y)*cos(coordinate_x-start_x_rad))*R / speed_Pesh
            len_list_start[m_i_s] = l_s
            l_f = acos(sin(finish_y_rad)*sin(coordinate_y) + cos(finish_y_rad)*cos(coordinate_y)*cos(coordinate_x-finish_x_rad))*R / speed_Pesh
            len_list_finish[m_i_s] = l_f

    len_list_finish_start += [len_list_start]
    len_list_finish_start += [len_list_finish]

    return len_list_finish_start


#ф-ия нахождения х(иксов) всех станций "с кешем"
def get_all_x():
    x_txt = os.path.join(PROJECT_ROOT, 'kesh2/all_x.txt')
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


def points_list2(tstart_point, tend_point):
    routes_dict = dict()
    points_list_item = list()
    for route_item in Route.objects.all():
        routes_dict[route_item.id] = list(route_item.station_set.filter(notstations=True).values_list('matrix_index', flat=True).order_by('matrix_index'))
        for route_id in routes_dict:
            list2 = routes_dict[route_id]
            points_list_item += [list2]
            if tend_point in list2 and tstart_point in list2:
                points_list_item = []
                points_list_item = [list2]
                break
    return points_list_item

#функция нахождения соседних точек
def get_border_points(points_price_min, closed_points_list, points_list_item, metastations_stations_list, tend_point, tstart_point):
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

            if tend_point not in list_item:
                for metastation in metastations_stations_list:
                    if points_price_min == metastation[0] and metastation[1] not in closed_points_list:
                        points_list += [metastation[1]]
                    if points_price_min == metastation[1] and metastation[0] not in closed_points_list:
                        points_list += [metastation[0]]
#                if metastation[0] == tend_point:
#                    points_list = [metastation[1]]
#                    break
#                if metastation[1] == tend_point:
#                    points_list = [metastation[0]]
#                    break

    return list(set(points_list))

def transport_types():
    transport_txt = os.path.join(PROJECT_ROOT, 'kesh/transport.txt')
    max_station_timestamp = Station.objects.all().aggregate(Max('timestamp'))
    max_route_timestamp = Route.objects.all().aggregate(Max('timestamp'))
    max_transport_timestamp = Transport.objects.all().aggregate(Max('timestamp'))
    max_onestation_timestamp = Onestation.objects.all().aggregate(Max('timestamp'))
    max_timestamp = max(max_onestation_timestamp, max_station_timestamp, max_route_timestamp, max_transport_timestamp)
    max_timestamp = max_timestamp['timestamp__max']
    if os.path.isfile(transport_txt) == False:
        open(transport_txt, 'w')
    sm_file = os.path.getmtime(transport_txt)
    stat = os.stat(transport_txt)
    file_size = stat.st_size
    timestamp = datetime.datetime.fromtimestamp(sm_file)

    if timestamp < max_timestamp or file_size == 0:
        transports = list()
        for station in Station.objects.filter(notstations=True).values_list('matrix_index', flat=True):
            para = list()
            transport = Station.objects.get(matrix_index=station).route.transport_type_id
            para += [station]
            para += [transport]
            transports += [para]

        fp = open(transport_txt, 'w')
        fp.write(repr(transports))
        fp.close()
    else:
        fp = open(transport_txt, 'r')
        read_file = fp.read()
        transports = eval(read_file)
        fp.close()            

    return transports

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

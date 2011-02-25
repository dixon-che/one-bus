#!/usr/bin/env python
# -*- coding: utf-8 -*-
from settings import PROJECT_ROOT
from math import *
from apps.point.models import Route, Station, Transport, Onestation
from django.db.models import Max
import os
import datetime
from utyls.speed_matrix.speed_matrix124 import speed_matrix124
from utyls.new_route_speed_matrix.new_route_speed_matrix124 import new_route_speed_matrix124
from utyls.points_list3 import points_list_3
from utyls.all_x import all_x
from utyls.route_zazor124 import route_zazor124
from utyls.route_stat124 import route_stat124


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

#ф-ия нахождения х(иксов) всех станций "с кешем"

def get_all_x():
    all_station_x = all_x()
    return all_station_x

# нахождение точек в радиусе старта

def get_points_in_radius_start(start_x, start_y, all_station_x, Transport1, Transport2, Transport3, Transport4):
    KoeRad = 0.01
    sx1 = start_x + KoeRad
    sx2 = start_x - KoeRad
    sy1 = start_y + KoeRad
    sy2 = start_y - KoeRad
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

def get_points_in_radius_finish(finish_x, finish_y, all_station_x, Transport1, Transport2, Transport3, Transport4):
    KoeRad = 0.01
    fx1 = finish_x + KoeRad
    fx2 = finish_x - KoeRad
    fy1 = finish_y + KoeRad
    fy2 = finish_y - KoeRad
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

# ф-ия создания списка маршрутов с остановками внутри маршрута

def points_list3():
    points_list_item = points_list_3()
    return points_list_item

# ф-ия создания словоря маршрутов с остановками внутри маршрута

def points_dict():
    routes_dict = dict()
    for route_item in Route.objects.all():
        routes_dict[route_item.id] = list(route_item.station_set.filter(notstations=True).values_list('matrix_index', flat=True).order_by('matrix_index'))
    return routes_dict


#ф-ии расчётов матриц переходов от станции ко всем остальным станциям внутри маршрута

def new_route_speed_matrix(Transport1, Transport2, Transport3, Transport4):
    para_dict = new_route_speed_matrix124()
    return para_dict


#ф-ии расчётов матриц переходов от станции ко всем остальным станциям внутри маршрута

def get_route_speed_matrix(Transport1, Transport2, Transport3, Transport4):
    order_dict, dict_route_matrix = dict(), dict()
    from_index_list, para_dict = list(), list()
    speed_matrix = get_speed_matrix(Transport1, Transport2, Transport3, Transport4)
    points_dict_item = points_dict()
    for route_id in points_dict_item:
        item = points_dict_item[route_id]
        list_speed_matrix = list()
        len_item = len(item)
        route_matrix = [[0] * len_item  for i in range(len_item)]
        for item_index in range(len_item):
            next_item_index = item_index + 1
            if next_item_index == len_item:
                break
            from_matrix_index = item[item_index]
            to_matrix_index = item[next_item_index]
            list_speed_matrix += [speed_matrix[to_matrix_index][from_matrix_index]]
            order_dict[from_matrix_index] = item_index
            order_dict[to_matrix_index] = next_item_index

        for item_index in range(len_item):
            next_item_index = item_index + 1
            if next_item_index == len_item:
                break
            for item_index2 in range(len_item):
                next_item_index2 = item_index2 + 1
                if next_item_index2 == len_item:
                    break
                if item_index < next_item_index2:
                    route_matrix[item_index][next_item_index2] = sum(list_speed_matrix[item_index:next_item_index2])
                if item_index2 < next_item_index:
                    route_matrix[next_item_index][item_index2] = sum(list_speed_matrix[item_index2:next_item_index])
        dict_route_matrix[route_id] = route_matrix
    para_dict = [dict_route_matrix, order_dict]
    return para_dict


# ф-ия создания словаря с открытыми, закрытыми маршрутами

def points_dict_open():
    routes_dict = dict()
    for route_item in Route.objects.all():
        routes_dict[route_item.id] = 1
    return routes_dict

# ф-ия нахождения времени в радиусе старта и финиша

def len_start_finish(start_x, start_y, finish_x, finish_y, points_in_radius_start, points_in_radius_finish):
    start = [start_x, start_y]
    finish = [finish_x, finish_y]
    len_list_start_finish = []
    points_list = Station.objects.filter(notstations=True).values_list('coordinate_x', 'coordinate_y').order_by('matrix_index')
    list_lenths1 = list()
    for station in points_in_radius_start:
        lenth = len_witput_points(start, points_list[station]) / 3
        list_lenths1 += [lenth]
    len_list_start_finish += [list_lenths1]
    list_lenths2 = list()
    for station in points_in_radius_finish:
        lenth = len_witput_points(finish, points_list[station]) / 3
        list_lenths2 += [lenth]
    len_list_start_finish += [list_lenths2]
    return len_list_start_finish

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
    #s_m__txt124 = os.path.join(PROJECT_ROOT, 'kesh2/speed_matrix124.txt')
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
        speed_matrix = speed_matrix124()
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

# Запустили считать волновой  алгоритм

def volna(station_finish, station_start, points_in_radius_finish, points_in_radius_start, len_list_start_finish, all_station_x, route_speed_matrix, speed_matrix, metastation_sort, points_list):

    Transport1 = Transport2 = Transport4 = 0
    Transport3 = 1
    #points_in_radius_finish = [549]#[station_finish]
    #len_list_start_finish[1] = [0]
    #points_in_radius_finish = [station_finish, 587]#[587, 586, station_finish]
    #len_list_start_finish[1] = [5, 15]#[5, 15, 16]
    route_dict = points_dict_open()
    len_dinamic = len(all_station_x)
    len_dinamic_list = len_dinamic + 2
    dinamic_list = [[100] * len_dinamic_list][0]
    next_points_list = points_in_radius_start#[station_start]
    mass_next_points_list = len_list_start_finish[0]#[0]
    #route_d_st = route_stations(Transport1, Transport2, Transport3, Transport4)
    next_points_list = [160]
    mass_next_points_list = [0]
    test_min1 = 0
    test_min2 = 0
    test_min3 = 0
    test_min4 = 0
    test_min5 = 0
    test_min6 = 0
    test_min7 = 0
    while next_points_list:
        # Находим минимальную остановку среди открытых маршрутов
        len_in = min(mass_next_points_list)
        index_start_point = mass_next_points_list.index(len_in)
        point_in = next_points_list[index_start_point]
        route_key = Station.objects.get(matrix_index=point_in).route_id
        test_min1 += 1
        if route_dict[route_key] == 1:
            test_min2 += 1
            # Берём соответствующий минимальной остановке маршрут и переносим его в словарь всех остановок в
            # соответствующиие места увеличив значение на значение до минимальной остановки.
            route_matrix = route_speed_matrix[0][route_key]
            order_in_matrix = route_speed_matrix[1][point_in]
            list_station_in_route = route_matrix[order_in_matrix]
            len_list_station_in_route = len(list_station_in_route)
            zero_order = point_in - order_in_matrix
            slys_order = zero_order + len_list_station_in_route - 1
            # Приращение маршрута на минимальное
            for station_in in range(len_list_station_in_route):
                test_min3 += 1
                list_station_in_route[station_in] += len_in
                if dinamic_list[zero_order:slys_order + 1][station_in] < list_station_in_route[station_in]:
                    list_station_in_route[station_in] = dinamic_list[zero_order:slys_order + 1][station_in]
            dinamic_list[zero_order:slys_order + 1] = list_station_in_route
            list_index = range(zero_order, slys_order + 1)
            for ob_element in list_index:
                test_min4 += 1
                # Если попалась остановка из списка радиуса finish мы её записываем в список с ключём finish.
                if ob_element in points_in_radius_finish and dinamic_list[-1] > dinamic_list[zero_order:slys_order + 1][list_index.index(ob_element)] + len_list_start_finish[1][points_in_radius_finish.index(ob_element)]:
                    dinamic_list[-1] = dinamic_list[zero_order:slys_order + 1][list_index.index(ob_element)] + len_list_start_finish[1][points_in_radius_finish.index(ob_element)]
                    dinamic_list[-2] = ob_element
                    #print ob_element, dinamic_list[zero_order:slys_order + 1], list_index.index(ob_element), len_list_start_finish[1][points_in_radius_finish.index(ob_element)], dinamic_list[-1], dinamic_list[-2]
                # Считаем все переходы записываем соответствующие значения в словарь и закрываем маршрут.
                for para in metastation_sort[ob_element]:
                    test_min5 += 1
                    if dinamic_list[para] > dinamic_list[ob_element] + speed_matrix[ob_element][para] and para not in list_index and (para not in next_points_list or mass_next_points_list[next_points_list.index(para)] > dinamic_list[ob_element] + speed_matrix[ob_element][para]) and dinamic_list[-1] > dinamic_list[ob_element] + speed_matrix[ob_element][para]:

                        dinamic_for = dinamic_list[ob_element] + speed_matrix[ob_element][para]
                        route_key2 = Station.objects.get(matrix_index=para).route_id
                        if route_dict[route_key2] == 1 and para not in next_points_list:
                            next_points_list += [para]
                            mass_next_points_list += [dinamic_for]

                        if route_dict[route_key2] == 0 or route_dict[route_key2] == 2:
                            route_dict[route_key2] = 2
                        dinamic_list[para] = dinamic_for

                # Закрываем аршрут
                route_dict[route_key] = 0
        # сравниваем с точкой finish если минимальная меньше идём дальше иначе выходим из цикла
        if min(mass_next_points_list) > dinamic_list[-1]:
            break
        next_points_list.remove(point_in)
        mass_next_points_list.remove(len_in)
        if next_points_list == []:
            break
    route_matrix5 = route_speed_matrix[0][32]
    order_in_matrix5 = route_speed_matrix[1][290]
    list_station_in_route5 = route_matrix5[order_in_matrix5]
    print list_station_in_route5
    print '---------------------------------------------------'
    print dinamic_list[287:313], dinamic_list[71:75], dinamic_list[84:90]
    print dinamic_list[287], dinamic_list[288], dinamic_list[289], dinamic_list[71], dinamic_list[72], speed_matrix[71][288]
    print test_min1, test_min2, test_min3, test_min4, test_min5, test_min6, test_min7
    www = route_zazor(Transport1, Transport2, Transport3, Transport4)
    point_dict1 = points_dict()
    for key_in_dict in route_dict:
        if route_dict[key_in_dict] == 2:
            dinamic1 = point_dict1[key_in_dict][0]
            dinamic2 = point_dict1[key_in_dict][-1]
            dinamic_slys = dinamic_list[dinamic1:dinamic2 + 1]
            for index_in_dinamic_slys in range(len(dinamic_slys)):
                next_index_in_dinamic_slys = index_in_dinamic_slys + 1
                if next_index_in_dinamic_slys == len(dinamic_slys):
                    break
                if dinamic_slys[next_index_in_dinamic_slys] > dinamic_slys[index_in_dinamic_slys] + www[key_in_dict][1][index_in_dinamic_slys]:
                    dinamic_slys[next_index_in_dinamic_slys] = dinamic_slys[index_in_dinamic_slys] + www[key_in_dict][1][index_in_dinamic_slys]
            dinamic_slys.reverse()
            for index_in_dinamic_slys in range(len(dinamic_slys)):
                next_index_in_dinamic_slys = index_in_dinamic_slys + 1
                if next_index_in_dinamic_slys == len(dinamic_slys):
                    break
                if dinamic_slys[next_index_in_dinamic_slys] > dinamic_slys[index_in_dinamic_slys] + www[key_in_dict][0][index_in_dinamic_slys]:
                    dinamic_slys[next_index_in_dinamic_slys] = dinamic_slys[index_in_dinamic_slys] + www[key_in_dict][0][index_in_dinamic_slys]
            dinamic_slys.reverse()
            dinamic_list[dinamic1:dinamic2 + 1] = dinamic_slys
    print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
    # print dinamic_list[287:313], dinamic_list[71:75], dinamic_list[84:90]
    # print dinamic_list[287], dinamic_list[288], dinamic_list[289], dinamic_list[71], dinamic_list[72], speed_matrix[71][288]
    print dinamic_list[13], dinamic_list[84], speed_matrix[13][84]
    return dinamic_list

# Минимум в маршруте

def min_in_route(list_p, dinamic_list, list_in, list_of_excluded):
    minimal = list_p
    for index_p in range(len(list_p)):
        #print 'list_of_excluded', list_of_excluded
        # if index_p not in list_of_excluded:
        next_index_p = index_p + 1
        prev_index_p = index_p - 1
        if next_index_p == len(list_p):
            break
        p_i_p = dinamic_list[list_p[prev_index_p]]
        i_p = dinamic_list[list_p[index_p]]
        n_i_p = dinamic_list[list_p[next_index_p]]
        value_list_in0= dinamic_list[list_in[0]]
        if p_i_p > i_p and n_i_p > i_p:
            if index_p < list_p.index(list_in[0]):
                z = list_p[index_p:list_p.index(list_in[0]) + 1]
                #print z, 'z2'
            if index_p > list_p.index(list_in[0]):
                z = list_p[list_p.index(list_in[0]):index_p + 1]
            if len(minimal) > len(z) and list_p[index_p] != list_in[0] and list_p[index_p] not in list_of_excluded and dinamic_list[list_p[index_p]] < value_list_in0:
                minimal = z
                print z, 'z3'
        if dinamic_list[list_p[-1]] < p_i_p and list_p[-1] != list_in[0] and list_p[-1] not in list_of_excluded and dinamic_list[list_p[-1]] < value_list_in0:
            z = list_p[list_p.index(list_in[0]):]
            print z, 'z4'
            if len(minimal) > len(z):
                minimal = z
        if dinamic_list[list_p[0]] < n_i_p and list_p[0] != list_in[0] and list_p[0] not in list_of_excluded and dinamic_list[list_p[0]] < value_list_in0:
            z = list_p[0:list_p.index(list_in[0]) + 1]
            print z, 'z1'
            if len(minimal) > len(z):
                minimal = z

    return minimal

# Запустили считать алгоритм обратной волны

def revers_volna(points_list, dinamic_list, speed_matrix):
    ind_ex_list2 = list()
    print dinamic_list[-2], min(dinamic_list[:866]), dinamic_list.index(min(dinamic_list[:866]))
    list_in = [dinamic_list[-2]]
    list_of_excluded = []
    while list_in:
        print list_in[0]
        for list_p in points_list:
            if list_in[0] in list_p:
                minimal = min_in_route(list_p, dinamic_list, list_in, list_of_excluded)
                #if list_in[0] == 84:
                print minimal#list_in#[0]#, dinamic_list[0:3]
                if list_in[0] == minimal[0]:
                    list_of_excluded += [minimal[-1]]
                if list_in[0] == minimal[-1]:
                    list_of_excluded += [minimal[0]]
                min_dinamic = min(dinamic_list[minimal[0]:minimal[-1] + 1])
                index_min_dinamic = dinamic_list[minimal[0]:minimal[-1] + 1].index(min_dinamic)
                index_station_finish = dinamic_list[minimal[0]:minimal[-1] + 1].index(dinamic_list[list_in[0]])
                index_in_dinamic_list_min = minimal[0] + index_min_dinamic
                #print index_station_finish, index_min_dinamic
                dinamic_slyse = list()
                if index_min_dinamic < index_station_finish:
                    dinamic_slyse = range(minimal[0] + index_min_dinamic, minimal[0] + index_station_finish + 1)
                if index_min_dinamic > index_station_finish:
                    dinamic_slyse = range(minimal[0] + index_station_finish, minimal[0] + index_min_dinamic + 1)
                if dinamic_slyse != []:
                    if dinamic_slyse[-1] == list_in[0]:
                        dinamic_slyse.reverse()
                #print dinamic_slyse
                ind_ex_list2 += dinamic_slyse
                for ind_ex in dinamic_list:
                    if ind_ex < min_dinamic and round(speed_matrix[dinamic_list.index(ind_ex)][index_in_dinamic_list_min], 6) == round(dinamic_list[index_in_dinamic_list_min] - dinamic_list[dinamic_list.index(ind_ex)], 6) and min_dinamic != list_in[0]:
                        list_in += [dinamic_list.index(ind_ex)]
                        list_in.remove(list_in[0])
                #print dinamic_list[minimal[0]:minimal[-1]]
                #print list_p[0], list_p[-1], index_min_dinamic, index_in_dinamic_list_min
                #print dinamic_list[list_p[0]:list_p[-1]], min(dinamic_list[list_p[0]:list_p[-1]])
                        print minimal, list_of_excluded
                        print ind_ex_list2, list_in
        if min_dinamic == min(dinamic_list[:866]):#0:#station_start == index_min_dinamic:
            break
    return ind_ex_list2

# Ф-ия адаптации результатов вывода

def result_adapt(dinamic_list, dinamic_list_min, start_x, start_y, finish_x, finish_y):
    dinamic_list_min.reverse()
    final_views = [{'x': start_x, 'y': start_y, 'idRoute':"-1", 'transportName':"", 'stopName':"Start", 't':'0', 'TransportsType':'', 'routeName':''}]
    i = 0
    q_list = list()
    for q in dinamic_list_min:
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
        item_dict['t'] = round(dinamic_list[q]*60, 2)
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
                item_dict['t'] = round(dinamic_list[q]*60, 2)
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
                item_dict['t'] = round(dinamic_list[q]*60, 2)
                final_views += [item_dict]
        i += 1
    final_views.append({'x': finish_x, 'y': finish_y, 'idRoute': "-1", 'transportName': "", 'stopName': "Finish", 't': round(dinamic_list[-1]*60, 2), 'TransportsType': '', 'routeName': ''})
    final_views.reverse()
    return final_views


def Metastation_sort(Transport1, Transport2, Transport3, Transport4):
    Metastation_sort124_txt = os.path.join(PROJECT_ROOT, 'kesh2/Metastation_sort124.txt')
    max_station_timestamp = Station.objects.all().aggregate(Max('timestamp'))
    max_route_timestamp = Route.objects.all().aggregate(Max('timestamp'))
    max_transport_timestamp = Transport.objects.all().aggregate(Max('timestamp'))
    max_onestation_timestamp = Onestation.objects.all().aggregate(Max('timestamp'))
    max_timestamp = max(max_onestation_timestamp, max_station_timestamp, max_route_timestamp, max_transport_timestamp)
    max_timestamp = max_timestamp['timestamp__max']
    if os.path.isfile(Metastation_sort124_txt) == False:
        open(Metastation_sort124_txt, 'w')
    sm_file = os.path.getmtime(Metastation_sort124_txt)
    stat = os.stat(Metastation_sort124_txt)
    file_size = stat.st_size
    timestamp = datetime.datetime.fromtimestamp(sm_file)

    if timestamp < max_timestamp or file_size == 0:
        list_in_raduus = [[]] * 866
        metastations_stations_list = new_Metastation(Transport1, Transport2, Transport3, Transport4)
        metastations_stations_list.sort()
        for element in range(866):
            one_list = list()
            for para in metastations_stations_list:
                if element == para[0]:
                    one_list += [para[1]]
            list_in_raduus[element] = one_list

        fp = open(Metastation_sort124_txt, "w")
        fp.write(repr(list_in_raduus))
        fp.close()
    else:
        fp = open(Metastation_sort124_txt, 'r')
        read_file = fp.read()
        list_in_raduus = eval(read_file)
        fp.close()

    return list_in_raduus


def route_zazor2(Transport1, Transport2, Transport3, Transport4):
    speed_matrix_short = route_zazor124()
    return speed_matrix_short


def route_zazor(Transport1, Transport2, Transport3, Transport4):
    q = points_dict()
    speed_matrix_short = dict()
    speed_matrix = get_speed_matrix(Transport1, Transport2, Transport3, Transport4)
    for item in q:
        go_in, go_out, all_list = [], [], []
        z = q[item]
        for index in range(len(z)):
            next_index = index + 1
            if next_index == len(z):
                break
            go_in += [speed_matrix[index + z[0]][next_index + z[0]]]
            go_out += [speed_matrix[next_index + z[0]][index + z[0]]]
        go_out.reverse()
        all_list += [go_out]
        all_list += [go_in]
        speed_matrix_short[item] = all_list

    return speed_matrix_short


def volna2(points_in_radius_finish, points_in_radius_start, len_list_start_finish, station_start, station_finish, all_station_x, route_speed_matrix, speed_matrix, metastation_sort, points_list):

    Transport1 = Transport2 = Transport4 = 0
    Transport3 = 1
    points_in_radius_finish = [549]#[587, 586, station_finish]
    len_list_start_finish[1] = [0]#[5, 15, 1]
    route_dict = points_dict_open()
    len_dinamic = len(all_station_x)
    len_dinamic_list = len_dinamic + 2
    dinamic_list = [[100] * len_dinamic_list][0]
    next_points_list = [160]#[station_start, 283, 99]
    mass_next_points_list = [0]#[5, 15, 100]
    #route_d_st = route_stations(Transport1, Transport2, Transport3, Transport4)
    test_min1 = 0
    test_min2 = 0
    test_min3 = 0
    test_min4 = 0
    test_min5 = 0
    test_min6 = 0
    test_min7 = 0
    while next_points_list:
        # Находим минимальную остановку среди открытых маршрутов
        len_in = min(mass_next_points_list)
        index_start_point = mass_next_points_list.index(len_in)
        point_in = next_points_list[index_start_point]
        route_key = Station.objects.get(matrix_index=point_in).route_id
        test_min1 += 1
        if route_dict[route_key] == 1:
            test_min2 += 1
            # Берём соответствующий минимальной остановке маршрут и переносим его в словарь всех остановок в
            # соответствующиие места увеличив значение на значение до минимальной остановки.
            route_matrix = route_speed_matrix[0][route_key]
            order_in_matrix = route_speed_matrix[1][point_in]
            list_station_in_route = route_matrix[order_in_matrix]
            len_list_station_in_route = len(list_station_in_route)
            zero_order = point_in - order_in_matrix
            slys_order = zero_order + len_list_station_in_route - 1
            # Приращение маршрута на минимальное
            for station_in in range(len_list_station_in_route):
                test_min3 += 1
                list_station_in_route[station_in] += len_in
                if dinamic_list[zero_order:slys_order + 1][station_in] < list_station_in_route[station_in]:
                    list_station_in_route[station_in] = dinamic_list[zero_order:slys_order + 1][station_in]
            dinamic_list[zero_order:slys_order + 1] = list_station_in_route
            list_index = range(zero_order, slys_order + 1)
            for ob_element in list_index:
                test_min4 += 1
                # Если попалась остановка из списка радиуса finish мы её записываем в список с ключём finish.
                if ob_element in points_in_radius_finish and dinamic_list[-1] > dinamic_list[zero_order:slys_order + 1][list_index.index(ob_element)] + len_list_start_finish[1][points_in_radius_finish.index(ob_element)]:
                    dinamic_list[-1] = dinamic_list[zero_order:slys_order + 1][list_index.index(ob_element)] + len_list_start_finish[1][points_in_radius_finish.index(ob_element)]
                    dinamic_list[-2] = ob_element
                    #print ob_element, dinamic_list[zero_order:slys_order + 1], list_index.index(ob_element), len_list_start_finish[1][points_in_radius_finish.index(ob_element)], dinamic_list[-1], dinamic_list[-2]
                # Считаем все переходы записываем соответствующие значения в словарь и закрываем маршрут.
                for para in metastation_sort[ob_element]:
                    test_min5 += 1
                    if dinamic_list[para] > dinamic_list[ob_element] + speed_matrix[ob_element][para] and para not in list_index and (para not in next_points_list or mass_next_points_list[next_points_list.index(para)] > dinamic_list[ob_element] + speed_matrix[ob_element][para]) and dinamic_list[-1] > dinamic_list[ob_element] + speed_matrix[ob_element][para]:

                        dinamic_for = dinamic_list[ob_element] + speed_matrix[ob_element][para]
                        route_key2 = Station.objects.get(matrix_index=para).route_id
                        if route_dict[route_key2] == 1 and para not in next_points_list:
                            next_points_list += [para]
                            mass_next_points_list += [dinamic_for]

                        if route_dict[route_key2] == 0 or route_dict[route_key2] == 2:
                            route_dict[route_key2] = 2
                        dinamic_list[para] = dinamic_for

                        if dinamic_list[para] < dinamic_list[-1] and para in points_in_radius_finish:
                            dinamic_list[-1] = dinamic_list[para]
                            dinamic_list[-2] = para
                # Закрываем аршрут
                route_dict[route_key] = 0
        # сравниваем с точкой finish если минимальная меньше идём дальше иначе выходим из цикла
        if min(mass_next_points_list) > dinamic_list[-1]:
            break
        next_points_list.remove(point_in)
        mass_next_points_list.remove(len_in)
        if next_points_list == []:
            break
    print test_min1, test_min2, test_min3, test_min4, test_min5, test_min6, test_min7
    www = route_zazor(Transport1, Transport2, Transport3, Transport4)
    point_dict1 = points_dict()
    for key_in_dict in route_dict:
        if route_dict[key_in_dict] == 2:
            dinamic1 = point_dict1[key_in_dict][0]
            dinamic2 = point_dict1[key_in_dict][-1]
            dinamic_slys = dinamic_list[dinamic1:dinamic2 + 1]
            for index_in_dinamic_slys in range(len(dinamic_slys)):
                next_index_in_dinamic_slys = index_in_dinamic_slys + 1
                if next_index_in_dinamic_slys == len(dinamic_slys):
                    break
                if dinamic_slys[next_index_in_dinamic_slys] > dinamic_slys[index_in_dinamic_slys] + www[key_in_dict][1][index_in_dinamic_slys]:
                    dinamic_slys[next_index_in_dinamic_slys] = dinamic_slys[index_in_dinamic_slys] + www[key_in_dict][1][index_in_dinamic_slys]
            dinamic_slys.reverse()
            for index_in_dinamic_slys in range(len(dinamic_slys)):
                next_index_in_dinamic_slys = index_in_dinamic_slys + 1
                if next_index_in_dinamic_slys == len(dinamic_slys):
                    break
                if dinamic_slys[next_index_in_dinamic_slys] > dinamic_slys[index_in_dinamic_slys] + www[key_in_dict][0][index_in_dinamic_slys]:
                    dinamic_slys[next_index_in_dinamic_slys] = dinamic_slys[index_in_dinamic_slys] + www[key_in_dict][0][index_in_dinamic_slys]
            dinamic_slys.reverse()
            dinamic_list[dinamic1:dinamic2 + 1] = dinamic_slys
    print dinamic_list[282:313], dinamic_list[71:75], dinamic_list[84:90]
    print dinamic_list[287], dinamic_list[288], dinamic_list[289], dinamic_list[71], dinamic_list[72], speed_matrix[71][288]
    return dinamic_list


def revers_volna2(station_finish, station_start, points_list, dinamic_list, speed_matrix):
    ind_ex_list2 = list()
    print dinamic_list[-2], min(dinamic_list[:866]), dinamic_list.index(min(dinamic_list[:866]))
    list_in = [dinamic_list[-2]]
    list_of_excluded = []
    while list_in:
        for list_p in points_list:
            if list_in[0] in list_p:
                #print list_in#[0]#, dinamic_list[0:3]
                minimal = min_in_route(list_p, dinamic_list, list_in, list_of_excluded)
                print minimal, 'min'
                if list_in[0] == minimal[0]:
                    list_of_excluded += [minimal[-1]]
                if list_in[0] == minimal[-1]:
                    list_of_excluded += [minimal[0]]
                set(list_of_excluded)
                min_dinamic = min(dinamic_list[minimal[0]:minimal[-1] + 1])
                index_min_dinamic = dinamic_list[minimal[0]:minimal[-1] + 1].index(min_dinamic)
                index_station_finish = dinamic_list[minimal[0]:minimal[-1] + 1].index(dinamic_list[list_in[0]])
                index_in_dinamic_list_min = minimal[0] + index_min_dinamic
                #print index_station_finish, index_min_dinamic
                dinamic_slyse = list()
                if index_min_dinamic < index_station_finish:
                    dinamic_slyse = range(minimal[0] + index_min_dinamic, minimal[0] + index_station_finish + 1)
                if index_min_dinamic > index_station_finish:
                    dinamic_slyse = range(minimal[0] + index_station_finish, minimal[0] + index_min_dinamic + 1)
                if dinamic_slyse != []:
                    if dinamic_slyse[-1] == list_in[0]:
                        dinamic_slyse.reverse()
                #print dinamic_slyse
                ind_ex_list2 += dinamic_slyse
                for ind_ex in dinamic_list:
                    if ind_ex < min_dinamic and round(speed_matrix[dinamic_list.index(ind_ex)][index_in_dinamic_list_min], 6) == round(dinamic_list[index_in_dinamic_list_min] - dinamic_list[dinamic_list.index(ind_ex)], 6) and min_dinamic != list_in[0]:
                        # route_ind_ex = Station.objects.get(matrix_index=dinamic_list.index(ind_ex)).route_id
                        # route_min_dinamic = Station.objects.get(matrix_index=index_in_dinamic_list_min).route_id
                        # print route_ind_ex, route_min_dinamic
                        # if route_ind_ex != route_min_dinamic:
                        list_in += [dinamic_list.index(ind_ex)]
                        list_in.remove(list_in[0])
                #print dinamic_list[minimal[0]:minimal[-1]]
                #print list_p[0], list_p[-1], index_min_dinamic, index_in_dinamic_list_min
                #print dinamic_list[list_p[0]:list_p[-1]], min(dinamic_list[list_p[0]:list_p[-1]])
                        print ind_ex_list2, list_in, list_of_excluded
        if min_dinamic == min(dinamic_list[:866]):#0:#station_start == index_min_dinamic:
            break
    return ind_ex_list2


def route_stations(Transport1, Transport2, Transport3, Transport4):
    stash = route_stat124
    return stash

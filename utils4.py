#!/usr/bin/env python
# -*- coding: utf-8 -*-
from settings import PROJECT_ROOT
from math import *
from apps.point.models import Route, Station, Transport, Onestation
from django.db.models import Max
import os
import datetime
from utyls1 import new_Metastation
from utyls.speed_matrix.speed_matrix124 import speed_matrix124
from utyls.new_route_speed_matrix.new_route_speed_matrix124 import new_route_speed_matrix124
from utyls.points_list3 import points_list_3
from utyls.all_x import all_x
from utyls.route_zazor124 import route_zazor124
from utyls.route_stat124 import route_stat124
from utyls.points_list_for_sort124 import points_list_for_sort124
from utyls.metastation_sort124 import metastation_sort124


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


#ф-ия нахождения соседних растояний между станциями внутри маршрута

def route_zazor(Transport1, Transport2, Transport3, Transport4):
    speed_matrix_short = route_zazor124()
    return speed_matrix_short


#ф-ия нахождения соответствий между остановкой и её маршрутом

def route_stations(Transport1, Transport2, Transport3, Transport4):
    stash = route_stat124()
    return stash


#ф-ия нахождения соседей каждой остановки

# def Metastation_sort(Transport1, Transport2, Transport3, Transport4):
#     list_in_raduus = metastation_sort124()
#     return list_in_raduus


#ф-ия нахождения переходов везде где это возможно

def get_speed_matrix(Transport1, Transport2, Transport3, Transport4):
    speed_matrix = speed_matrix124()
    return speed_matrix

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


# ф-ия создания списка физ. остоновок

def l_onestation_def():
    l_onestation_txt = os.path.join(PROJECT_ROOT, 'kesh3/l_onestation.txt')
    max_station_timestamp = Station.objects.all().aggregate(Max('timestamp'))
    max_route_timestamp = Route.objects.all().aggregate(Max('timestamp'))
    max_transport_timestamp = Transport.objects.all().aggregate(Max('timestamp'))
    max_onestation_timestamp = Onestation.objects.all().aggregate(Max('timestamp'))
    max_timestamp = max(max_onestation_timestamp, max_station_timestamp, max_route_timestamp, max_transport_timestamp)
    max_timestamp = max_timestamp['timestamp__max']
    if os.path.isfile(l_onestation_txt) == False:
        open(l_onestation_txt, 'w')
    sm_file = os.path.getmtime(l_onestation_txt)
    stat = os.stat(l_onestation_txt)
    file_size = stat.st_size
    timestamp = datetime.datetime.fromtimestamp(sm_file)

    if timestamp < max_timestamp or file_size == 0:
        l_onestation_in_def = list(Onestation.objects.values_list('id', flat=True).order_by('id'))

        fp = open(l_onestation_txt, 'w+')
        fp.write(repr(l_onestation_in_def))
        fp.close()
    else:
        fp = open(l_onestation_txt, 'r')
        read_file = fp.read()
        l_onestation_in_def = eval(read_file)
        fp.close()

    return l_onestation_in_def


# ф-ия создания словоря списков физ. остоновок в маршруте

def d_onestation_def():
    d_onestation_txt = os.path.join(PROJECT_ROOT, 'kesh3/d_onestation.txt')
    max_station_timestamp = Station.objects.all().aggregate(Max('timestamp'))
    max_route_timestamp = Route.objects.all().aggregate(Max('timestamp'))
    max_transport_timestamp = Transport.objects.all().aggregate(Max('timestamp'))
    max_onestation_timestamp = Onestation.objects.all().aggregate(Max('timestamp'))
    max_timestamp = max(max_onestation_timestamp, max_station_timestamp, max_route_timestamp, max_transport_timestamp)
    max_timestamp = max_timestamp['timestamp__max']
    if os.path.isfile(d_onestation_txt) == False:
        open(d_onestation_txt, 'w')
    sm_file = os.path.getmtime(d_onestation_txt)
    stat = os.stat(d_onestation_txt)
    file_size = stat.st_size
    timestamp = datetime.datetime.fromtimestamp(sm_file)

    if timestamp < max_timestamp or file_size == 0:
        routes_dict = dict()
        for route_item in Route.objects.all():
            routes_dict[route_item.id] = list(route_item.station_set.filter(notstations=True).values_list('one_station', flat=True).order_by('matrix_index'))

        fp = open(d_onestation_txt, 'w+')
        fp.write(repr(routes_dict))
        fp.close()
    else:
        fp = open(d_onestation_txt, 'r')
        read_file = fp.read()
        routes_dict = eval(read_file)
        fp.close()

    return routes_dict


def d_interval_route_def():
    d_interval_route_txt = os.path.join(PROJECT_ROOT, 'kesh3/d_interval_route.txt')
    max_station_timestamp = Station.objects.all().aggregate(Max('timestamp'))
    max_route_timestamp = Route.objects.all().aggregate(Max('timestamp'))
    max_transport_timestamp = Transport.objects.all().aggregate(Max('timestamp'))
    max_onestation_timestamp = Onestation.objects.all().aggregate(Max('timestamp'))
    max_timestamp = max(max_onestation_timestamp, max_station_timestamp, max_route_timestamp, max_transport_timestamp)
    max_timestamp = max_timestamp['timestamp__max']
    if os.path.isfile(d_interval_route_txt) == False:
        open(d_interval_route_txt, 'w')
    sm_file = os.path.getmtime(d_interval_route_txt)
    stat = os.stat(d_interval_route_txt)
    file_size = stat.st_size
    timestamp = datetime.datetime.fromtimestamp(sm_file)

    if timestamp < max_timestamp or file_size == 0:
        d_interval_route = dict()
        for route_item in Route.objects.all():
            d_interval_route[route_item.id] = float(route_item.speed)

        fp = open(d_interval_route_txt, 'w+')
        fp.write(repr(d_interval_route))
        fp.close()
    else:
        fp = open(d_interval_route_txt, 'r')
        read_file = fp.read()
        d_interval_route = eval(read_file)
        fp.close()

    return d_interval_route


def d_stations_route_def():
    d_stations_route_txt = os.path.join(PROJECT_ROOT, 'kesh3/d_stations_route.txt')
    max_station_timestamp = Station.objects.all().aggregate(Max('timestamp'))
    max_route_timestamp = Route.objects.all().aggregate(Max('timestamp'))
    max_transport_timestamp = Transport.objects.all().aggregate(Max('timestamp'))
    max_onestation_timestamp = Onestation.objects.all().aggregate(Max('timestamp'))
    max_timestamp = max(max_onestation_timestamp, max_station_timestamp, max_route_timestamp, max_transport_timestamp)
    max_timestamp = max_timestamp['timestamp__max']
    if os.path.isfile(d_stations_route_txt) == False:
        open(d_stations_route_txt, 'w')
    sm_file = os.path.getmtime(d_stations_route_txt)
    stat = os.stat(d_stations_route_txt)
    file_size = stat.st_size
    timestamp = datetime.datetime.fromtimestamp(sm_file)

    if timestamp < max_timestamp or file_size == 0:
        d_stations_route = dict()
        for itemw in Onestation.objects.all():
            d_stations_route[int(itemw.id)] = []
        for item in Station.objects.all():
            if item.one_station != None:
                d_stations_route[int(item.one_station_id)] += [int(item.route_id)]

        fp = open(d_stations_route_txt, 'w+')
        fp.write(repr(d_stations_route))
        fp.close()
    else:
        fp = open(d_stations_route_txt, 'r')
        read_file = fp.read()
        d_stations_route = eval(read_file)
        fp.close()

    return d_stations_route


def l_status_def():
    l_status_txt = os.path.join(PROJECT_ROOT, 'kesh3/l_status.txt')
    max_station_timestamp = Station.objects.all().aggregate(Max('timestamp'))
    max_route_timestamp = Route.objects.all().aggregate(Max('timestamp'))
    max_transport_timestamp = Transport.objects.all().aggregate(Max('timestamp'))
    max_onestation_timestamp = Onestation.objects.all().aggregate(Max('timestamp'))
    max_timestamp = max(max_onestation_timestamp, max_station_timestamp, max_route_timestamp, max_transport_timestamp)
    max_timestamp = max_timestamp['timestamp__max']
    if os.path.isfile(l_status_txt) == False:
        open(l_status_txt, 'w')
    sm_file = os.path.getmtime(l_status_txt)
    stat = os.stat(l_status_txt)
    file_size = stat.st_size
    timestamp = datetime.datetime.fromtimestamp(sm_file)

    if timestamp < max_timestamp or file_size == 0:
        l_status = dict()
        for itemw in Onestation.objects.all():
            l_status[int(itemw.id)] = 1

        fp = open(l_status_txt, 'w+')
        fp.write(repr(l_status))
        fp.close()
    else:
        fp = open(l_status_txt, 'r')
        read_file = fp.read()
        l_status = eval(read_file)
        fp.close()

    return l_status


def d_real_station_def():
    d_real_station_txt = os.path.join(PROJECT_ROOT, 'kesh3/d_real_station.txt')
    max_station_timestamp = Station.objects.all().aggregate(Max('timestamp'))
    max_route_timestamp = Route.objects.all().aggregate(Max('timestamp'))
    max_transport_timestamp = Transport.objects.all().aggregate(Max('timestamp'))
    max_onestation_timestamp = Onestation.objects.all().aggregate(Max('timestamp'))
    max_timestamp = max(max_onestation_timestamp, max_station_timestamp, max_route_timestamp, max_transport_timestamp)
    max_timestamp = max_timestamp['timestamp__max']
    if os.path.isfile(d_real_station_txt) == False:
        open(d_real_station_txt, 'w')
    sm_file = os.path.getmtime(d_real_station_txt)
    stat = os.stat(d_real_station_txt)
    file_size = stat.st_size
    timestamp = datetime.datetime.fromtimestamp(sm_file)

    if timestamp < max_timestamp or file_size == 0:
        d_real_station = dict()
        for itemw in Onestation.objects.all():
            d_real_station[int(itemw.id)] = list(Station.objects.filter(one_station=int(itemw.id)).values_list('matrix_index', flat=True))

        fp = open(d_real_station_txt, 'w+')
        fp.write(repr(d_real_station))
        fp.close()
    else:
        fp = open(d_real_station_txt, 'r')
        read_file = fp.read()
        d_real_station = eval(read_file)
        fp.close()

    return d_real_station


def d_one_station_def():
    d_one_station_txt = os.path.join(PROJECT_ROOT, 'kesh3/d_one_station.txt')
    max_station_timestamp = Station.objects.all().aggregate(Max('timestamp'))
    max_route_timestamp = Route.objects.all().aggregate(Max('timestamp'))
    max_transport_timestamp = Transport.objects.all().aggregate(Max('timestamp'))
    max_onestation_timestamp = Onestation.objects.all().aggregate(Max('timestamp'))
    max_timestamp = max(max_onestation_timestamp, max_station_timestamp, max_route_timestamp, max_transport_timestamp)
    max_timestamp = max_timestamp['timestamp__max']
    if os.path.isfile(d_one_station_txt) == False:
        open(d_one_station_txt, 'w')
    sm_file = os.path.getmtime(d_one_station_txt)
    stat = os.stat(d_one_station_txt)
    file_size = stat.st_size
    timestamp = datetime.datetime.fromtimestamp(sm_file)

    if timestamp < max_timestamp or file_size == 0:
        d_one_station = dict()
        for itemw in Station.objects.all():
            d_one_station[int(itemw.matrix_index)] = itemw.one_station_id

        fp = open(d_one_station_txt, 'w+')
        fp.write(repr(d_one_station))
        fp.close()
    else:
        fp = open(d_one_station_txt, 'r')
        read_file = fp.read()
        d_one_station = eval(read_file)
        fp.close()

    return d_one_station


def l_curret_points(start_x, start_y, all_station_x, Transport1, Transport2, Transport3, Transport4):
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
    stationn = list(set(points_in_radius_start))
    points_in_radius_start = list()
    for s in stationn:
        points_in_radius_start += [Station.objects.get(matrix_index=s).one_station_id]

    return list(set(points_in_radius_start))


def get_points_in_radius_finish2(finish_x, finish_y, all_station_x, Transport1, Transport2, Transport3, Transport4):
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
    stationn = list(set(points_in_radius_finish))
    points_in_radius_finish = list()
    for s in stationn:
        points_in_radius_finish += [Station.objects.get(matrix_index=s).one_station_id]

    return list(set(points_in_radius_finish))


def l_len_start_finish(start_x, start_y, finish_x, finish_y, points_in_radius_start, points_in_radius_finish):
    start = [start_x, start_y]
    finish = [finish_x, finish_y]
    len_list_start_finish = []
    points_list = list(Onestation.objects.all().values_list('coordinate_x', 'coordinate_y').order_by('id'))
    list_lenths1 = list()
    for station in points_in_radius_start:
        lenth = len_witput_points(start, points_list[station - 1]) / 3
        list_lenths1 += [lenth]
    len_list_start_finish += [list_lenths1]
    list_lenths2 = list()
    for station in points_in_radius_finish:
        lenth = len_witput_points(finish, points_list[station - 1]) / 3
        list_lenths2 += [lenth]
    len_list_start_finish += [list_lenths2]
    return len_list_start_finish

# ф-ия создания словаря с открытыми, закрытыми маршрутами

def points_dict_open():
    routes_dict = dict()
    for route_item in Route.objects.all():
        routes_dict[route_item.id] = 1
    return routes_dict

# Алгоритм прямой волны

def volna2(points_in_radius_start, points_in_radius_finish, len_list_start_finish, route_speed_matrix, Transport1, Transport2, Transport3, Transport4):
    print points_in_radius_start, points_in_radius_finish
    l_sort_onestation = Metastation_sort_onestation(Transport1, Transport2, Transport3, Transport4)
    l_sort_time = sort_time(Transport1, Transport2, Transport3, Transport4)
    l_onestation = l_onestation_def()
    l_dinamic = [[100] * (len(l_onestation) + 4)][0]
    d_stations_route = d_stations_route_def()
    d_status_route = points_dict_open()
    d_onestation = d_onestation_def()
    l_status = l_status_def()
    www = route_zazor(Transport1, Transport2, Transport3, Transport4)
    l_transform = l_dinamic[:len(l_dinamic) - 2]
    next_points_list = points_in_radius_start
    next_time_points_list = len_list_start_finish[0]
    test_min1 = 0
    test_min2 = 0
    test_min3 = 0
    test_min4 = 0
    test_min5 = 0
    while next_points_list:
        test_min1 += 1
        min_time = min(next_time_points_list)
        index_min_start_time = next_time_points_list.index(min_time)
        min_ost = next_points_list[index_min_start_time]
        l_status[min_ost] = 0
        l_route_min_ost = d_stations_route[min_ost]
        for route_with_min_ost in l_route_min_ost:
            test_min2 += 1
            if d_status_route[route_with_min_ost] == 1 or min_time < l_dinamic[min_ost]:
                l_min_ost = d_onestation[route_with_min_ost]
                index_min_ost = l_min_ost.index(min_ost)
                route_matrix = route_speed_matrix[0][route_with_min_ost]
                l_station_in_route = route_matrix[index_min_ost]
                len_l_station_in_route = len(l_station_in_route)
                # Приращение маршрута на минимальное
                for station_in in range(len_l_station_in_route):
                    test_min3 += 1
                    l_station_in_route[station_in] += min_time
                    st_in = l_min_ost[station_in]
                    if l_dinamic[st_in] > l_station_in_route[station_in]:
                        l_dinamic[st_in] = l_station_in_route[station_in]
                        l_transform[st_in] = l_station_in_route[station_in]
                        route_stat = d_stations_route[st_in]
                        for ost_stat in route_stat:
                            test_min4 += 1
                            if d_status_route[ost_stat] == 0:
                                d_status_route[ost_stat] = 2
                        if st_in in points_in_radius_finish and l_dinamic[-1] > l_dinamic[st_in] + len_list_start_finish[1][points_in_radius_finish.index(st_in)]:
                            l_dinamic[-1] = l_dinamic[st_in] + len_list_start_finish[1][points_in_radius_finish.index(st_in)]
                            l_dinamic[-2] = st_in
                            print l_dinamic[-1], l_dinamic[-2]

                    # Перебор соседних физ. остановок.
                    if l_sort_onestation[st_in] != []:
                        for neigbor in l_sort_onestation[st_in]:
                            test_min5 += 1
                            index_neigbor = l_sort_onestation[st_in].index(neigbor)
                            if neigbor != st_in and l_dinamic[neigbor] > l_sort_time[st_in][index_neigbor] + l_dinamic[st_in] and neigbor not in l_min_ost and (neigbor not in next_points_list or next_time_points_list[next_points_list.index(neigbor)] > l_sort_time[st_in][index_neigbor] + l_dinamic[st_in]) and l_dinamic[-1] > l_sort_time[st_in][index_neigbor] + l_dinamic[st_in]:
                                time_points = l_sort_time[st_in][index_neigbor] + l_dinamic[st_in]
                                for route in d_stations_route[neigbor]:
                                    if d_status_route[route] == 1 and neigbor not in next_points_list:
                                        next_points_list += [neigbor]
                                        next_time_points_list += [time_points]

                                    if d_status_route[route] == 0 or d_status_route[route] == 2:
                                        d_status_route[route] = 2

                                    if neigbor in next_points_list and next_time_points_list[next_points_list.index(neigbor)] > l_sort_time[st_in][index_neigbor] + l_dinamic[st_in]:
                                        index_next_points_list = next_points_list.index(neigbor)
                                        next_time_points_list[index_next_points_list] = time_points
                                    l_dinamic[neigbor] = time_points

                # Закрываем маршрут
                d_status_route[route_with_min_ost] = 0

        l_transform[min_ost] = 100
        next_points_list += [l_transform.index(min(l_transform))]
        next_time_points_list += [min(l_transform)]
        # Двойная волна
        for item in d_status_route:
            if d_status_route[item] == 2:
                l_slys = d_onestation[item]
                for index_in_slys in range(len(l_slys)):
                    next_index_in_slys = index_in_slys + 1
                    if next_index_in_slys == len(l_slys):
                        break
                    if l_dinamic[l_slys[next_index_in_slys]] > l_dinamic[l_slys[index_in_slys]] + www[item][1][index_in_slys]:
                        l_dinamic[l_slys[next_index_in_slys]] = l_dinamic[l_slys[index_in_slys]] + www[item][1][index_in_slys]
                l_slys.reverse()
                for index_in_slys in range(len(l_slys)):
                    next_index_in_slys = index_in_slys + 1
                    if next_index_in_slys == len(l_slys):
                        break
                    if l_dinamic[l_slys[next_index_in_slys]] > l_dinamic[l_slys[index_in_slys]] + www[item][0][index_in_slys]:
                        l_dinamic[l_slys[next_index_in_slys]] = l_dinamic[l_slys[index_in_slys]] + www[item][0][index_in_slys]
                l_slys.reverse()
                d_status_route[item] = 0
        # Условия выхода
        if l_dinamic[-1] < min_time:
            break

        next_points_list.remove(min_ost)
        next_time_points_list.remove(min_time)

        if next_points_list == []:
            break

    print test_min1, test_min2, test_min3, test_min4, test_min5#, test_min6, test_min7
    return l_dinamic

# Алгоритм обратной волны

def revers_volna2(Transport1, Transport2, Transport3, Transport4, l_dinamic, speed_matrix):
    l_result = []
    d_one_station = d_one_station_def()
    metastation_sort = Metastation_sort(Transport1, Transport2, Transport3, Transport4)
    d_real_station = d_real_station_def()
    opt_ost = l_dinamic[-2]
    l_job = [opt_ost]
    print opt_ost
    while l_job:
        i = 0
        q = l_job[0]
        l_metastat = d_real_station[l_job[0]]
        for station in l_metastat:
            for para in metastation_sort[station]:
                print l_job[0], d_one_station[para], para
                print speed_matrix[para][station], l_dinamic[l_job[0]], l_dinamic[d_one_station[para]], l_dinamic[228]
                if round(speed_matrix[para][station], 6) == round(l_dinamic[l_job[0]] - l_dinamic[d_one_station[para]], 6):
                    i = 1
                    l_result += [para]
                    l_job.remove(q)
                    l_job += [d_one_station[para]]
        if i == 0:
            break
    return l_result


def Metastation_sort(Transport1, Transport2, Transport3, Transport4):
    Metastation_sort124_txt = os.path.join(PROJECT_ROOT, 'kesh3/Metastation_sort124.txt')
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
        for element1 in range(866):
            next_element = element1 + 1
            if next_element < 865:
                if int(Station.objects.get(matrix_index=next_element).order) > int(Station.objects.get(matrix_index=element1).order):
                    list_in_raduus[element1] += [next_element]
            if int(Station.objects.get(matrix_index=element1).order) - 1 >= 0:
                list_in_raduus[element1] += [element1 - 1]

        fp = open(Metastation_sort124_txt, "w")
        fp.write(repr(list_in_raduus))
        fp.close()
    else:
        fp = open(Metastation_sort124_txt, 'r')
        read_file = fp.read()
        list_in_raduus = eval(read_file)
        fp.close()

    return list_in_raduus


def Metastation_sort_onestation(Transport1, Transport2, Transport3, Transport4):
    Metastation_sort_onestation124_txt = os.path.join(PROJECT_ROOT, 'kesh3/Metastation_sort_onestation124.txt')
    max_station_timestamp = Station.objects.all().aggregate(Max('timestamp'))
    max_route_timestamp = Route.objects.all().aggregate(Max('timestamp'))
    max_transport_timestamp = Transport.objects.all().aggregate(Max('timestamp'))
    max_onestation_timestamp = Onestation.objects.all().aggregate(Max('timestamp'))
    max_timestamp = max(max_onestation_timestamp, max_station_timestamp, max_route_timestamp, max_transport_timestamp)
    max_timestamp = max_timestamp['timestamp__max']
    if os.path.isfile(Metastation_sort_onestation124_txt) == False:
        open(Metastation_sort_onestation124_txt, 'w')
    sm_file = os.path.getmtime(Metastation_sort_onestation124_txt)
    stat = os.stat(Metastation_sort_onestation124_txt)
    file_size = stat.st_size
    timestamp = datetime.datetime.fromtimestamp(sm_file)

    if timestamp < max_timestamp or file_size == 0:
        list_in_raduus = [[]] * 398
        metastations_stations_list = new_Metastation(Transport1, Transport2, Transport3, Transport4)
        for para in metastations_stations_list:
            a = para[0]
            b = para[1]
            para[0] = int(Station.objects.get(matrix_index=a).one_station_id)
            para[1] = int(Station.objects.get(matrix_index=b).one_station_id)
        #metastations_stations_list.sort()
        for element in range(398):
            one_list = list()
            for para in metastations_stations_list:
                if element == para[0]:
                    one_list += [para[1]]
            list_in_raduus[element] = one_list
        list_in_radius = list()
        for in_radus in list_in_raduus:
            q = list(set(in_radus))
            list_in_radius += [q]

        fp = open(Metastation_sort_onestation124_txt, "w")
        fp.write(repr(list_in_radius))
        fp.close()
    else:
        fp = open(Metastation_sort_onestation124_txt, 'r')
        read_file = fp.read()
        list_in_radius = eval(read_file)
        fp.close()

    return list_in_radius


def sort_time(Transport1, Transport2, Transport3, Transport4):
    sort_time124_txt = os.path.join(PROJECT_ROOT, 'kesh3/sort_time124.txt')
    max_station_timestamp = Station.objects.all().aggregate(Max('timestamp'))
    max_route_timestamp = Route.objects.all().aggregate(Max('timestamp'))
    max_transport_timestamp = Transport.objects.all().aggregate(Max('timestamp'))
    max_onestation_timestamp = Onestation.objects.all().aggregate(Max('timestamp'))
    max_timestamp = max(max_onestation_timestamp, max_station_timestamp, max_route_timestamp, max_transport_timestamp)
    max_timestamp = max_timestamp['timestamp__max']
    if os.path.isfile(sort_time124_txt) == False:
        open(sort_time124_txt, 'w')
    sm_file = os.path.getmtime(sort_time124_txt)
    stat = os.stat(sort_time124_txt)
    file_size = stat.st_size
    timestamp = datetime.datetime.fromtimestamp(sm_file)

    if timestamp < max_timestamp or file_size == 0:
        q = Metastation_sort_onestation(Transport1, Transport2, Transport3, Transport4)
        time_list = []
        for index in range(len(q)):
            onestat = []
            print index
            if index == 233 or index == 0:
                time_in_list = list()
            if index != 233 and index > 0:
                onestat1 = float(Onestation.objects.get(id=index).coordinate_x)
                onestat += [onestat1]
                onestat2 = float(Onestation.objects.get(id=index).coordinate_y)
                onestat += [onestat2]
                time_in_list = list()
                if q[index] != []:
                    for index_in in q[index]:
                        ones2tat = []
                        if index_in != 233 and index_in <= 397:# and index_in != index + 1:
                            ones2tat1 = float(Onestation.objects.get(id=index_in).coordinate_x)
                            ones2tat += [ones2tat1]
                            ones2tat2 = float(Onestation.objects.get(id=index_in).coordinate_y)
                            ones2tat += [ones2tat2]
                            print ones2tat, index_in, index
                            if index_in != index:
                                time_in_list += [len_witput_points(onestat, ones2tat) / 3]
                            else:
                                time_in_list += [0]
            time_list += [time_in_list]

        fp = open(sort_time124_txt, "w")
        fp.write(repr(time_list))
        fp.close()
    else:
        fp = open(sort_time124_txt, 'r')
        read_file = fp.read()
        time_list = eval(read_file)
        fp.close()

    return time_list

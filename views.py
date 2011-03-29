#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import gmtime, strftime
from django.db.models import Max
from settings import PROJECT_ROOT
from django.shortcuts import render_to_response
from django.http import HttpResponse
from apps.point.models import Route, Station, Transport, Onestation
from apps.all_routes.models import Routes
from math import *
from utils3 import get_all_x, get_points_in_radius_start, get_points_in_radius_finish, new_route_speed_matrix, points_list3, sum, len_witput_points, points_dict, points_dict_open, len_start_finish, new_Metastation, get_speed_matrix, volna, revers_volna, result_adapt, Metastation_sort, route_stations#, points_list_for_sort
#from utyls1 import get_all_x, get_points_in_radius_start, get_points_in_radius_finish, new_route_speed_matrix, points_list3, sum, len_witput_points, points_dict_open, len_start_finish, new_Metastation, get_speed_matrix, volna, revers_volna, result_adapt, Metastation_sort
#from utils4 import l_onestation_def, d_onestation_def, d_interval_route_def, d_stations_route_def, l_status_def, d_real_station_def, l_curret_points, get_points_in_radius_finish2, l_len_start_finish, volna2, d_one_station_def, revers_volna2
import datetime
import json
import os


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
    # print datetime.datetime.now(), '0'
    # # Приняли данные из джава скрипта Transport1, Transport2, Transport3, Transport4, start_x, start_y, finish_y, finish_x
    # Transport1 = Transport2 = Transport4 = 0
    # Transport3 = 1
    # start_x = 36.159245
    # start_y = 49.973507
    # finish_x = 36.270139
    # finish_y = 50.038782
    # #R = 6376 # радиус земли
    # print datetime.datetime.now(), '1'
    # # Пересчитали все х координаты
    # all_station_x = get_all_x()
    # print datetime.datetime.now(), '2'
    # # Расчитали матрицу переходов speed_matrix
    # speed_matrix = get_speed_matrix(Transport1, Transport2, Transport3, Transport4)
    # print datetime.datetime.now(), '5'
    # # Расчитали матрицы переходов от станции ко всем остальным станциям внутри маршрута
    # route_speed_matrix = new_route_speed_matrix(Transport1, Transport2, Transport3, Transport4)
    # print datetime.datetime.now(), '6'
    # # Просчитали все переходы между остановками
    # metastation_sort = Metastation_sort(Transport1, Transport2, Transport3, Transport4)
    # # Нашли все остановки в радиусе старта
    # points_in_radius_start = l_curret_points(start_x, start_y, all_station_x, Transport1, Transport2, Transport3, Transport4)
    # # Нашли все остановки в радиусе финиша
    # points_in_radius_finish = get_points_in_radius_finish2(finish_x, finish_y, all_station_x, Transport1, Transport2, Transport3, Transport4)
    # print datetime.datetime.now(), '8'
    # # Создаём список остановок в маршруте
    # points_list = points_list3()
    # # Поставили время для всех остановок в радиусе старта
    # len_list_start_finish = l_len_start_finish(start_x, start_y, finish_x, finish_y, points_in_radius_start, points_in_radius_finish)
    # print datetime.datetime.now(), '9'
    # 
    # # Запустили считать алгоритм
    # l_dinamic = volna2(points_in_radius_start, points_in_radius_finish, len_list_start_finish, route_speed_matrix, Transport1, Transport2, Transport3, Transport4)
    # print l_dinamic[-2], l_dinamic[-1]
    # # Запустили считать алгоритм обратной волны
    # min_l_dinamic = revers_volna2(Transport1, Transport2, Transport3, Transport4, l_dinamic, speed_matrix)
    # print min_l_dinamic
    text = 'Welcome to "Transplants do not"'
    return render_to_response('base.html', {"text": text})


def transport_list(request):
    transport_list_txt = os.path.join(PROJECT_ROOT, 'kesh2/transport_list.txt')
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
                                                     'coordinate_x', 'coordinate_y').order_by('route__transport_type', 'route__id', 'order'))

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
    print datetime.datetime.now(), '0'
    # Приняли данные из джава скрипта Transport1, Transport2, Transport3, Transport4, start_x, start_y, finish_y, finish_x
    Transport1 = Transport2 = Transport3 = Transport4 = 0
    # if request.GET['Transport1'] == 'undefined':
    #     Transport1 = 1
    # if request.GET['Transport2'] == 'undefined':
    #     Transport2 = 1
    # if request.GET['Transport3'] == 'undefined':
    #     Transport3 = 1
    # if request.GET['Transport4'] == 'undefined':
    #     Transport4 = 1
    Transport3 = 1
    start_x = float(request.GET['x1'])
    start_y = float(request.GET['y1'])
    finish_x = float(request.GET['x2'])
    finish_y = float(request.GET['y2'])
    #R = 6376 # радиус земли
    # Пересчитали все х координаты
    all_station_x = get_all_x()
    # Пересчитали растояние от старта к финишу
    #s_f = (acos(sin(start_y*pi/180)*sin(finish_y*pi/180) + cos(start_y*pi/180)*cos(finish_y*pi/180)*cos(finish_x*pi/180-start_x*pi/180))*R)/3
    # Расчитали матрицу переходов speed_matrix
    speed_matrix = get_speed_matrix(Transport1, Transport2, Transport3, Transport4)
    # Расчитали матрицы переходов от станции ко всем остальным станциям внутри маршрута
    route_speed_matrix = new_route_speed_matrix(Transport1, Transport2, Transport3, Transport4)
    print datetime.datetime.now(), '6'
    # Просчитали все переходы между остановками
    metastation_sort = Metastation_sort(Transport1, Transport2, Transport3, Transport4)
    # Нашли все остановки в радиусе старта
    points_in_radius_start = get_points_in_radius_start(start_x, start_y, all_station_x, Transport1, Transport2, Transport3, Transport4)
    # Нашли все остановки в радиусе финиша
    points_in_radius_finish = get_points_in_radius_finish(finish_x, finish_y, all_station_x, Transport1, Transport2, Transport3, Transport4)
    print datetime.datetime.now(), '8'
    # Поставили время для всех остановок в радиусе старта
    len_list_start_finish = len_start_finish(start_x, start_y, finish_x, finish_y, points_in_radius_start, points_in_radius_finish)
    print datetime.datetime.now(), '9'
    # Создаём список остановок в маршруте
    points_list = points_list3()
    # Запустили считать алгоритм обратной волны
    dinamic_list = volna(points_in_radius_finish, points_in_radius_start, len_list_start_finish, all_station_x, route_speed_matrix, speed_matrix, metastation_sort, points_list, Transport1, Transport2, Transport3, Transport4)
    print datetime.datetime.now(), '10'
                # Запустили считать обратную волну и записывать данные
    dinamic_list_min = revers_volna(points_list, dinamic_list, speed_matrix)
#    points_list_for_sort()
    print dinamic_list_min
    print datetime.datetime.now(), '11'
    # Преобразовали данные для вывода
    final_views = result_adapt(dinamic_list, dinamic_list_min, start_x, start_y, finish_x, finish_y)
    return HttpResponse(json.dumps(final_views), 'application/javascript')

from django.shortcuts import render_to_response
from django.http import HttpResponse
from apps.point.models import Route, Station, Metastation, Transport
import json


def hello(request):
    text = 'Hello world!'
    return render_to_response('base.html', {"text":text})


def transport_list(request):
    stations = list(Station.objects.all().values('route__id', 'route__route',
                                                 'route__color', 'name',
                                                 'coordinate_x', 'coordinate_y'))
    return HttpResponse(json.dumps(stations), 'application/javascript')


def route(request):
    points_list = Station.objects.values_list('coordinate_x', 'coordinate_y').order_by('id')
    len_points = len(points_list)
    go_matrix = [[0] * len_points  for i in range(len_points )]
    speed_matrix = [[0] * len_points  for i in range(len_points )]
    a = Station.objects.values('id', 'route_id', 'coordinate_x', 'coordinate_y', 'name', 'meta_station_id', 'matrix_index')
    z = Route.objects.values('id', 'route', 'speed', 'interval', 'transport_type_id')
    b = Metastation.objects.values('id')
    graphs_dict = dict()
    time_chenge = dict()
    all_speeds = dict()
    points_list_chenge = list()
    lenth_start = list()
    lenth_finish = list()
    zb = list()
    time = list()
    closed_points_list = list()
    radius = list()
    radius_x = list()
    radius_x2 = list()
    radiuss = list()
    radius_y2 = list()
    coord_v_km = 111.1
    coord_v_km2 = 78.56
    speed_Pesh = 3
    wating_time = 1/2.0
    KoeRad = 0.009

    for q in a:
        name = q['name']
        idk = q['id']
        route_id = q['route_id']
        meta_station_id = q['meta_station_id']
        matrix_index = q['matrix_index']
        
    for q in z:
        idk = q['id']
        qwas = Route.objects.get(id=idk).station_set.values_list('matrix_index', flat=True)
        qwas = list(qwas)
        graphs_dict[idk] = qwas
        route = q['route']
        speed = q['speed']
        interval = q['interval']
        all_speeds[idk] = speed
        time_chenge[idk] = interval

    for q in b:
        idk = q['id']
        qwas = Metastation.objects.get(id=idk).station_set.values_list('matrix_index', flat=True)
        qwas = list(qwas)
        points_list_chenge += [qwas]

    def len_witput_points(start_point, end_point):
        lenth = pow((pow(start_point[0] - end_point[0], 2) * coord_v_km2) +
                     (pow(start_point[1] - end_point[1], 2) * coord_v_km), 1/2.0)
        return lenth

    for j in graphs_dict:
        item_list = graphs_dict[j]
        speed_to = all_speeds[j]
        
        for item_index in range(len(item_list)):
            next_item_index = item_index + 1
            if next_item_index == len(item_list):
                break

            from_matrix_index = item_list[item_index]
            to_matrix_index = item_list[next_item_index]
            go_matrix[to_matrix_index][from_matrix_index] = go_matrix[from_matrix_index][to_matrix_index] = len_witput_points(points_list[from_matrix_index],points_list[to_matrix_index])
            print go_matrix[to_matrix_index][from_matrix_index]
            speed_matrix[to_matrix_index][from_matrix_index] = speed_matrix[from_matrix_index][to_matrix_index] = len_witput_points(points_list[from_matrix_index],points_list[to_matrix_index]) / speed_to

    for swaq in points_list_chenge:
        for item in swaq:
            for item_index in range(len(swaq)):
                next = item_index + 1
                if next == len(swaq):
                    break
                next_index = swaq.index(item) - next
                next_item = swaq[next_index]
                for j in graphs_dict:
                    item_list = graphs_dict[j]
                    chenge = time_chenge[j]
                    if next_item in item_list:
                        speed_matrix[next_item][item] = chenge * wating_time

    start_x = request.GET['x1']
    start_x = float(start_x)
    sx1 = start_x + KoeRad
    sx2 = start_x - KoeRad
    start_y = request.GET['y1']
    start_y = float(start_y)
    sy1 = start_y + KoeRad
    sy2 = start_y - KoeRad
    finish_x = request.GET['x2']
    finish_x = float(finish_x)
    fx1 = finish_x + KoeRad
    fx2 = finish_x - KoeRad
    finish_y = request.GET['y2']
    finish_y = float(finish_y)
    fy1 = finish_y + KoeRad
    fy2 = finish_y - KoeRad

    for q in a:
        coordinate_x = q['coordinate_x']
        coordinate_x = float(coordinate_x)
        radius_x += [coordinate_x]
        coordinate_y = q['coordinate_y']
        coordinate_y = float(coordinate_y) 
        
        l_s = pow((pow(start_x - coordinate_x, 2) * coord_v_km2) +
                     (pow(start_y - coordinate_y, 2) * coord_v_km), 1/2.0) / speed_Pesh
        lenth_start += [l_s]

        l_f = pow((pow(finish_x - coordinate_x, 2) * coord_v_km2) +
                    (pow(finish_y - coordinate_y, 2) * coord_v_km), 1/2.0) / speed_Pesh
        lenth_finish += [l_f]

    s_f = pow((pow(finish_x - start_x, 2) * coord_v_km2) +
                    (pow(finish_y - start_y, 2) * coord_v_km), 1/2.0) / speed_Pesh

    lenth_finish_min = min(lenth_finish)
    T_pesh_finish = lenth_finish_min
    lenth_start_min = min(lenth_start)
    tstart_point = lenth_start.index(lenth_start_min)
    tend_point = lenth_finish.index(lenth_finish_min)

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

    end_point = index_Mass + 2
    start_point = index_Mass +1

    for z in radius_x:
        if sx2 < z < sx1:
            radius_x2 += [z]
    for j in radius_x2:
        qwesd = Station.objects.filter(coordinate_x=j).values_list('coordinate_y', 'matrix_index')
        for wq in qwesd:
            if sy2 < wq[0] < sy1:
                radius += [wq[1]]
    for q in radius:
        that = list()
        that += [start_point]
        that += [q]
        points_list_chenge += [that]

    for z in radius_x:
        if fx2 < z < fx1:
            radius_y2 += [z]
    for j in radius_y2:
        qwesd = Station.objects.filter(coordinate_x=j).values_list('coordinate_y', 'matrix_index')
        for wq in qwesd:
            if fy2 < wq[0] < fy1:
                radiuss += [wq[1]]
    for q in radiuss:
        thet = list()
        thet += [end_point]
        thet += [q]
        points_list_chenge += [thet]

    if radiuss == []:
        end_point = tend_point
    if radius == []:
        start_point = tstart_point
#    print points_list_chenge
    def get_border_points(points_price_min, closed_points_list):
        points_list = []
        for graph_key in graphs_dict:
            points_list_item = graphs_dict[graph_key]
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

                for swaq in points_list_chenge :
                    if points_price_min in swaq:
                        for M_index in range(len(swaq)):
                            next = M_index + 1
                            if next == len(swaq):
                                break
                            next_index = swaq.index(points_price_min) - next
                            next_item = swaq[next_index]
                            if next_item not in closed_points_list:
                                points_list += [next_item]
            
        for swaq in points_list_chenge :
            if points_price_min in swaq:
                for M_index in range(len(swaq)):
                    next = M_index + 1
                    if next == len(swaq):
                        break
                    next_index = swaq.index(points_price_min) - next
                    next_item = swaq[next_index]
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
#        print active_point, next_points_list
        for item_point_index in border_points:
            go_price = speed_matrix[active_point][item_point_index]
            if str(item_point_index) not in points_price:
                zb = [item_point_index]
                go_price_time = active_point_price + go_price
                time = [go_price_time]
                points_price[str(item_point_index)] = [go_price_time, active_point_P + zb, active_point_Pe + time]
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
    points_price[str(end_point)][1].remove(start_point)
    points_price[str(end_point)][1].remove(end_point)
    points_price[str(end_point)][2].remove(0)
    i = 0
    for q in points_price[str(end_point)][1]:
        item_dict = {}
        point = Station.objects.get(matrix_index=q)
        point_name = point.name
        item_dict['stopName'] = point_name
        point_route_id = point.route_id
        P_route_id = str(point_route_id)
        item_dict['idRoute'] = P_route_id
        transport_id = Route.objects.get(id=point_route_id).transport_type_id
        transportT_id = str(transport_id)
        item_dict['transportName'] = transportT_id
        point_coordinate_x = point.coordinate_x
        item_dict['x'] = str(point_coordinate_x)
        point_coordinate_y = point.coordinate_y
        item_dict['y'] = str(point_coordinate_y)
        item_dict['t'] = str(points_price[str(end_point)][2][i])
        final_views += [item_dict]
        i += 1
    T = points_price[str(end_point)][2][-1] + T_pesh_finish 
    final_views.append({'x': finish_x, 'y': finish_y, 'idRoute':"-1", 'transportName':"", 'stopName':"Finish", 't':T})
    final_views.reverse()

    return HttpResponse(json.dumps(final_views), 'application/javascript')

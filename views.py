from django.shortcuts import render_to_response
from django.http import HttpResponse
from apps.point.models import Route, Station, Metastation, Transport
from django.db.models import F
import json


def hello(request):
    text = 'Hello world!'
    points_list = Station.objects.values_list('coordinate_x', 'coordinate_y').order_by('id')
    a = Station.objects.values('id', 'route_id', 'coordinate_x', 'coordinate_y', 'name', 'meta_station_id', 'matrix_index')
    z = Route.objects.values('id', 'route', 'speed', 'interval')
    b = Metastation.objects.values('id')
    graphs_dict = dict()
    time_chenge = dict()
    all_speeds = dict()
    points_list_chenge = list()
    
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


    len_points = len(points_list)
    go_matrix = [[0] * len_points  for i in range(len_points )]
    speed_matrix = [[0] * len_points  for i in range(len_points )]

    def len_witput_points(start_point, end_point):
        lenth = pow((pow(start_point[0] - end_point[0], 2) +
                     pow(start_point[1] - end_point[1], 2)), 1/2.0)
        return lenth

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
                        next_index = swaq.index(points_price_min) - 1
                        next_item = swaq[next_index]
                        if next_item not in closed_points_list:
                            points_list += [next_item]
        return list(set(points_list))

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

            speed_matrix[to_matrix_index][from_matrix_index] = speed_matrix[from_matrix_index][to_matrix_index] = len_witput_points(points_list[from_matrix_index],points_list[to_matrix_index])*speed_to

    for swaq in points_list_chenge:
        for item in swaq:
            next_index = swaq.index(item) - 1
            next_item = swaq[next_index]
            for j in graphs_dict:
                item_list = graphs_dict[j]
                chenge = time_chenge[j]
                if next_item in item_list:
                    speed_matrix[next_item][item] = chenge

    start_point = raw_input('Input start point: ')
    start_point = int(start_point)
    if start_point > 400:
        print "start_point < 401"
        exit(-1)

    end_point = raw_input('Input end point: ')
    end_point = int(end_point)
    if end_point > 400:
        print "end_point < 401"
        exit(-1)

    name_start_point = Station.objects.get(matrix_index=start_point)
    name_end_point = Station.objects.get(matrix_index=end_point)
    
    points_price = {str(start_point): [0, str(start_point)]}

    next_points_list = [start_point]
    closed_points_list = []

    while next_points_list:
        p = [[next_key, points_price[str(next_key)][0]] for next_key in next_points_list]
        active_point = min(p, key=lambda x: x[1])[0]
        active_point_price = points_price[str(active_point)][0]
        active_point_P = points_price[str(active_point)][1]
        border_points = get_border_points(active_point, closed_points_list)

        for item_point_index in border_points:
            go_price = speed_matrix[active_point][item_point_index]
            if str(item_point_index) not in points_price:
                points_price[str(item_point_index)] = [active_point_price + go_price, active_point_P + "-%d" %item_point_index ]
            else:
                item_point_price = points_price[str(active_point)][0] + speed_matrix[active_point][item_point_index]
                if item_point_price < points_price[str(item_point_index)][0]:
                    points_price[str(item_point_index)][0] = item_point_price

        closed_points_list.append(active_point)
        next_points_list.remove(active_point)
        next_points_list += border_points
        next_points_list = list(set(next_points_list))
        if end_point in closed_points_list:
            break

    if str(end_point) in points_price:
        print "Your way is:", points_price[str(end_point)]
        swat = points_price[str(end_point)]
    else:
        print "No way here"
        
    return render_to_response("base.html", {'text': text, 'swat':swat, 'name_start_point':name_start_point, 'name_end_point':name_end_point})


def transport_list(request):
    stations = list(Station.objects.all().values('route__id', 'route__route',
                                                 'route__color', 'name',
                                                 'coordinate_x', 'coordinate_y'))
    return HttpResponse(json.dumps(stations), 'application/javascript')


def route(request):
    start_x = request.GET['x1']
    start_x = float(start_x)
    start_y = request.GET['y1']
    start_y = float(start_y)
    finish_x = request.GET['x2']
    finish_x = float(finish_x)
    finish_y = request.GET['y2']
    finish_y = float(finish_y)
    q = Station.objects.values('coordinate_x', 'coordinate_y', 'matrix_index')
    lenth_start = list()
    lenth_finish = list()
    for z in q:
        coordinate_x = z['coordinate_x']
        coordinate_x = float(coordinate_x)
        coordinate_y = z['coordinate_y']
        coordinate_y = float(coordinate_y) 
        
        l_s = pow((pow(start_x - coordinate_x, 2) +
                     pow(start_y - coordinate_y, 2)), 1/2.0)
        lenth_start += [l_s]

        l_f = pow((pow(finish_x - coordinate_x, 2) +
                     pow(finish_y - coordinate_y, 2)), 1/2.0)
        lenth_finish += [l_f]

    lenth_finish_min = min(lenth_finish)
    lenth_start_min = min(lenth_start)
    end_point = lenth_finish.index(lenth_finish_min)
    start_point = lenth_start.index(lenth_start_min)

    print lenth_start_min, lenth_finish_min, end_point, start_point

    a = [{"x":"36.217984836548595","y":"50.02102632247681","stopName":"Finish","transportName":"","idRoute":"-1","t":"88.8201072680"},{"x":"36.21334387","y":"50.01951181","stopName":"\u0443\u043b. \u041d\u043e\u0432\u0433\u043e\u0440\u043e\u0434\u0441\u043a\u0430\u044f","transportName": None,"idRoute":"4","t":"74.1746370680"},{"x":"36.21674000","y":"50.01545400","stopName":"\u0421\u043e\u0441\u043d\u043e\u0432\u0430\u044f \u0433\u043e\u0440\u043a\u0430","transportName":None,"idRoute":"4","t":"72.0580587080"},{"x":"36.21833851","y":"50.01206210","stopName":"\u0443\u043b. \u041a\u043e\u0441\u043c\u0438\u0447\u0435\u0441\u043a\u0430\u044f","transportName":None,"idRoute":"4","t":"70.5581867480"},{"x":"36.21820376","y":"50.00766235","stopName":"\u0443\u043b. \u0425\u0435\u0440\u0441\u043e\u043d\u0441\u043a\u0430\u044f","transportName":None,"idRoute":"4","t":"68.7974641880"},{"x":"36.21810352","y":"50.00308571","stopName":"\u0421\u043f\u0443\u0441\u043a \u041f\u0430\u0441\u0441\u0438\u043e\u043d\u0430\u0440\u0438\u0435\u0432","transportName":None,"idRoute":"4","t":"66.9663727520"},{"x":"36.20510632","y":"49.99823626","stopName":"\u0414\u041a \u0416\u0435\u043b\u0435\u0437\u043d\u043e\u0434\u043e\u0440\u043e\u0436\u043d\u0438\u043a\u043e\u0432","transportName":None,"idRoute":"1","t":"51.4174009960"},{"x":"36.20314800","y":"50.00035556","stopName":"\u042d\u043b\u0435\u043a\u0442\u0440\u043e\u0430\u043f\u043f\u0430\u0440\u0430\u0442\u043d\u044b\u0439 \u0437-\u0434","transportName":None,"idRoute":"1","t":"50.2631809180"},{"x":"36.20127950","y":"50.00385856","stopName":"\u0443\u043b. \u041a\u043e\u043a\u0447\u0435\u0442\u0430\u0432\u0441\u043a\u0430\u044f","transportName":None,"idRoute":"1","t":"48.6751154380"},{"x":"36.19935505","y":"50.00774595","stopName":"\u0418\u0432\u0430\u043d\u043e\u0432\u043a\u0430","transportName":"","idRoute":"","t":"36.9400512000"},{"x":"36.194982212036884","y":"50.01925668337604","stopName":"Start","transportName":"","idRoute":"-1","t":"0"}] 

    return HttpResponse(json.dumps(a), 'application/javascript')



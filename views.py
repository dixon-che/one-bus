from django.shortcuts import render_to_response
from django.http import HttpResponse
from apps.point.models import Route, Station, Metastation
import json


def hello(request):
    text = 'Hello world!'
    return render_to_response("base.html", {'text': text})


def transport_list(request):
    stations = list(Station.objects.all().values('route__id', 'route__route',
                                                 'route__color', 'name',
                                                 'coordinate_x', 'coordinate_y'))
    return HttpResponse(json.dumps(stations), 'application/javascript')


def route(request):
    start_x = request.GET['x1']
    start_y = request.GET['y1']
    finish_x = request.GET['x2']
    finish_y = request.GET['y2']


    a = [{"x":"36.217984836548595","y":"50.02102632247681","stopName":"Finish","transportName":"","idRoute":"-1","t":"88.8201072680"},{"x":"36.21334387","y":"50.01951181","stopName":"\u0443\u043b. \u041d\u043e\u0432\u0433\u043e\u0440\u043e\u0434\u0441\u043a\u0430\u044f","transportName": None,"idRoute":"4","t":"74.1746370680"},{"x":"36.21674000","y":"50.01545400","stopName":"\u0421\u043e\u0441\u043d\u043e\u0432\u0430\u044f \u0433\u043e\u0440\u043a\u0430","transportName":None,"idRoute":"4","t":"72.0580587080"},{"x":"36.21833851","y":"50.01206210","stopName":"\u0443\u043b. \u041a\u043e\u0441\u043c\u0438\u0447\u0435\u0441\u043a\u0430\u044f","transportName":None,"idRoute":"4","t":"70.5581867480"},{"x":"36.21820376","y":"50.00766235","stopName":"\u0443\u043b. \u0425\u0435\u0440\u0441\u043e\u043d\u0441\u043a\u0430\u044f","transportName":None,"idRoute":"4","t":"68.7974641880"},{"x":"36.21810352","y":"50.00308571","stopName":"\u0421\u043f\u0443\u0441\u043a \u041f\u0430\u0441\u0441\u0438\u043e\u043d\u0430\u0440\u0438\u0435\u0432","transportName":None,"idRoute":"4","t":"66.9663727520"},{"x":"36.20510632","y":"49.99823626","stopName":"\u0414\u041a \u0416\u0435\u043b\u0435\u0437\u043d\u043e\u0434\u043e\u0440\u043e\u0436\u043d\u0438\u043a\u043e\u0432","transportName":None,"idRoute":"1","t":"51.4174009960"},{"x":"36.20314800","y":"50.00035556","stopName":"\u042d\u043b\u0435\u043a\u0442\u0440\u043e\u0430\u043f\u043f\u0430\u0440\u0430\u0442\u043d\u044b\u0439 \u0437-\u0434","transportName":None,"idRoute":"1","t":"50.2631809180"},{"x":"36.20127950","y":"50.00385856","stopName":"\u0443\u043b. \u041a\u043e\u043a\u0447\u0435\u0442\u0430\u0432\u0441\u043a\u0430\u044f","transportName":None,"idRoute":"1","t":"48.6751154380"},{"x":"36.19935505","y":"50.00774595","stopName":"\u0418\u0432\u0430\u043d\u043e\u0432\u043a\u0430","transportName":"","idRoute":"","t":"36.9400512000"},{"x":"36.194982212036884","y":"50.01925668337604","stopName":"Start","transportName":"","idRoute":"-1","t":"0"}] 

    return HttpResponse(json.dumps(a), 'application/javascript')

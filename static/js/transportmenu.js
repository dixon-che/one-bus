YMaps.jQuery(function()
{
	var Start_x, Start_y, Finish_x, Finish_y;
	var map;
	var http_request;
	var Marks;
	var Lines;
	var placemark;
	var TransportMenu;

	BusInit();
	CreateStyles();

        YMaps.jQuery(document).ready(function() {
	    YMaps.jQuery('#routes1').hide();
	    YMaps.jQuery('#routes2').hide();
	    YMaps.jQuery('#routes3').hide();
	    YMaps.jQuery('#routes4').hide();
	    YMaps.jQuery("#show_route1").bind('click', function(){ YMaps.jQuery('#routes1').show() })
	    YMaps.jQuery("#hide_route1").bind('click', function(){ YMaps.jQuery('#routes1').hide() })
	    YMaps.jQuery("#show_route2").bind('click', function(){ YMaps.jQuery('#routes2').show() })
	    YMaps.jQuery("#hide_route2").bind('click', function(){ YMaps.jQuery('#routes2').hide() })
	    YMaps.jQuery("#show_route3").bind('click', function(){ YMaps.jQuery('#routes3').show() })
	    YMaps.jQuery("#hide_route3").bind('click', function(){ YMaps.jQuery('#routes3').hide() })
	    YMaps.jQuery("#show_route4").bind('click', function(){ YMaps.jQuery('#routes4').show() })
	    YMaps.jQuery("#hide_route4").bind('click', function(){ YMaps.jQuery('#routes4').hide() })

	    YMaps.jQuery("#push").bind('click', function(event) {
		var geocoder1 = new YMaps.Geocoder('Украина, г. Харьков, ' + YMaps.jQuery('#start:input').val(), {results: 1});
		var geocoder2 = new YMaps.Geocoder('Украина, г. Харьков, ' + YMaps.jQuery('#finish:input').val(), {results: 1});
		YMaps.Events.observe(geocoder1, geocoder1.Events.Load, pointFound1);
		YMaps.Events.observe(geocoder2, geocoder2.Events.Load, pointFound2);
	                                                         }
                                       )
		function pointFound1()
	    {
		if(this.length())
		{
		    var new_point = this.get(0);
		    if(new_point.kind == 'house')
			{
			    map.removeOverlay(placemark);
			    placemark = new YMaps.Placemark(new_point.getGeoPoint(), {draggable: true, style: "default#redSmallPoint"});
			    if(Start_x == -1)
				{
				    Start_x = new_point.getGeoPoint().getLng();
				    Start_y = new_point.getGeoPoint().getLat();
				    placemark.name = 'Start';
				    placemark.description = 'Start';
				    YMaps.Events.observe(placemark, placemark.Events.Drag, function (obj)
							 {
							     Start_x = obj.getGeoPoint().getLng();
							     Start_y = obj.getGeoPoint().getLat();
							 });

				}
			}
		}
	    }

		function pointFound2()
	    {
		if(this.length())
		{
		    var new_point = this.get(0);
		    if(new_point.kind == 'house')
			{
			    Finish_x = new_point.getGeoPoint().getLng();
			    Finish_y = new_point.getGeoPoint().getLat();
			    placemark.name = 'Finish';
			    placemark.description = 'Finish';
			    http_request.onreadystatechange = function()
			    {
				if (http_request.readyState == 4) 
				{
				    map.removeOverlay(Marks);
				    map.removeOverlay(Lines);
				    Marks = new YMaps.GeoObjectCollection();
				    Lines = new YMaps.GeoObjectCollection();
				    var Line;
				
				    p = JSON.parse(http_request.responseText);
				    
				    oldRouteid = 0;
				    var human_readable = '';
				    var human_readable2 = '';
				    var a = '';
				    var b = '';
				    var final_time = '';
				    var pm ;
				    for (var i in p)
				    {
					if(p[i].idRoute != oldRouteid)
					{
					    if(i != 0)
					    {
						if(p[i].idRoute != -1)
						    Line.addPoint(new YMaps.GeoPoint(p[i].x, p[i].y));
						Lines.add(Line);
					    }
					    Line = new YMaps.Polyline();
					    if(p[i].idRoute == -1)
					    {
						Line.setStyle("1bus#Peshkom");
						if(i != 0)
						    Line.addPoint(new YMaps.GeoPoint(p[i-1].x, p[i-1].y));										
					    }
					    else
						Line.setStyle(p[i].idRoute);
							
					    oldRouteid = p[i].idRoute;
					}
					if(p[i].idRoute == -1)
					    pm = new YMaps.Placemark(new YMaps.GeoPoint(p[i].x,p[i].y),{draggable: false, style:"1bus#Peshehod"});			
					else {
					    if (p[i].route__transport_type == 1)
						pm = new YMaps.Placemark(new YMaps.GeoPoint(p[i].x,p[i].y),{draggable: false, style:"1bus#TramvayStation"});
					    else {
						if (p[i].route__transport_type == 2)
						    pm = new YMaps.Placemark(new YMaps.GeoPoint(p[i].x,p[i].y),{draggable: false, style:"1bus#MetroStation"});
						else {
						    if (p[i].route__transport_type == 3)
							pm = new YMaps.Placemark(new YMaps.GeoPoint(p[i].x,p[i].y),{draggable: false, style:"1bus#BusStation"});
						    else {
							if (p[i].route__transport_type == 4)
							    pm = new YMaps.Placemark(new YMaps.GeoPoint(p[i].x,p[i].y),{draggable: false, style:"1bus#TrolStation"});
							else
							    pm = new YMaps.Placemark(new YMaps.GeoPoint(p[i].x,p[i].y),{draggable: false, style:"1bus#PovorotStation"});
							    }}}}
					pm.name = p[i].stopName;
					pm.description = p[i].transportName + " t=" + p[i].t;
					Marks.add(pm);
					Line.addPoint(new YMaps.GeoPoint(p[i].x, p[i].y));
					if(p[i].stopName == 'Finish'){ final_time = p[i].t }
					if(p[i].TransportsType != undefined)
					    {
					    if(p[i].stopName == 'Start'){ human_readable = 'Пешком - ' + human_readable;}
					    else
					    {
						if(p[i].stopName == 'Finish'){ human_readable = 'Пешком' + human_readable;}
						else
						{
						    if(p[i].TransportsType == 'trolley'){p[i].TransportsType = 'Тс'}
						    if(p[i].TransportsType == 'Metro'){p[i].TransportsType = 'M.'}
						    if(p[i].TransportsType == 'tram'){p[i].TransportsType = 'Tй'}
						    if(p[i].TransportsType == 'bus'){p[i].TransportsType = 'А'}
						    if(p[i].routeName == 'SALTOVKA'){p[i].routeName = 'S'}
						    if(p[i].routeName == 'Holodnogorskaya'){p[i].routeName = 'H'}
						    if(p[i].routeName == 'Alekseevka'){p[i].routeName = 'A'}
						    if(p[i].TransportsType != a || p[i].routeName != b)
						    {
							a = p[i].TransportsType;
							b = p[i].routeName;
							human_readable = p[i].TransportsType + '(' + p[i].routeName + '' + ') -' + human_readable;
						    }
						}
					    }}
					    if(p[i].stopName != 'Start' && p[i].stopName != 'Finish' && p[i].TransportsType != undefined)
					    {
						human_readable2 = '<ul>' + p[i].TransportsType + '(' + p[i].routeName + ' )' + p[i].stopName + '--' + p[i].t + '</ul>' + human_readable2;
					    }
					}
				    human_readable2 = human_readable2 + '<input type="button" id="more3" value="Скрыть"></br>';
				    YMaps.jQuery('#human_readable2').html(human_readable2);
				    YMaps.jQuery('#human_readable2').hide();
				    YMaps.jQuery('#human_readable').html('<table border=1 cellspacing=0 width=800><tr><td>№</td><td>Время</td><td>Длительность</td><td>Цена</td><td>Транспорт</td></tr><tr><td>1</td><td></td><td>' + final_time + '</td><td></td><td>' + human_readable + '</td></tr></table><input type="button" id="more2" value="Подробней"></br>');
				    YMaps.jQuery("#more2").bind('click', function()
				    				{
				    				    YMaps.jQuery('#human_readable2').show();
				    				});
				    YMaps.jQuery("#more3").bind('click', function()
				    				{
				    				    YMaps.jQuery('#human_readable2').hide();
				    				});
				    Lines.add(Line);
				    map.addOverlay(Lines);								
				    map.addOverlay(Marks);
				    Start_x = Start_y = Finish_x = Finish_y = -1;
				    map.removeOverlay(placemark);
				}
			    };
			    var url = "/route/?x1=" + encodeURI(Start_x) 
				+ "&y1=" + encodeURI(Start_y)
				+ "&x2=" + encodeURI(Finish_x) 
				+ "&y2=" + encodeURI(Finish_y)
			        + "&Transport1=" + YMaps.jQuery('#Transport1:checked').val()
			        + "&Transport2=" + YMaps.jQuery('#Transport2:checked').val()
			        + "&Transport3=" + YMaps.jQuery('#Transport3:checked').val()
			        + "&Transport4=" + YMaps.jQuery('#Transport4:checked').val();
			    http_request.open("GET", url, true);
			    http_request.send(null);
			}
		    map.addOverlay(placemark);
		    placemark.openBalloon();
		}
	    }
                                                  }
                                      );


	var myEventListener = YMaps.Events.observe(map, map.Events.Click, function (map, mEvent)

	{
		map.removeOverlay(placemark);
		placemark = new YMaps.Placemark(mEvent.getGeoPoint(), {draggable: true, style: "default#redSmallPoint"});
		if(Start_x == -1)
		{
			Start_x = mEvent.getGeoPoint().getLng();
			Start_y = mEvent.getGeoPoint().getLat();
			placemark.name = 'Start';
			placemark.description = 'Start';
			YMaps.Events.observe(placemark, placemark.Events.Drag, function (obj)
			{
				Start_x = obj.getGeoPoint().getLng();
				Start_y = obj.getGeoPoint().getLat();
			});
		}
		else
		{		    
			Finish_x = mEvent.getGeoPoint().getLng();
			Finish_y = mEvent.getGeoPoint().getLat();
			placemark.name = 'Finish';
			placemark.description = 'Finish';
			http_request.onreadystatechange = function()
			{
				if (http_request.readyState == 4) 
				{
					map.removeOverlay(Marks);
					map.removeOverlay(Lines);
					Marks = new YMaps.GeoObjectCollection();
					Lines = new YMaps.GeoObjectCollection();
					var Line;
				
				        p = JSON.parse(http_request.responseText);
				    
				    oldRouteid = 0;
				    var human_readable = '';
				    var human_readable2 = '';
				    var myyy_route = '';
				    var a = '';
				    var b = '';
				    var final_time = '';
					var pm ;
					for (var i in p)
					{
						if(p[i].idRoute != oldRouteid)
						{
							if(i != 0)
							{
								if(p[i].idRoute != -1)
									Line.addPoint(new YMaps.GeoPoint(p[i].x, p[i].y));
								Lines.add(Line);
							}
							Line = new YMaps.Polyline();
							if(p[i].idRoute == -1)
							{
								Line.setStyle("1bus#Peshkom");
								if(i != 0)
									Line.addPoint(new YMaps.GeoPoint(p[i-1].x, p[i-1].y));										
							}
							else
								Line.setStyle(p[i].idRoute);
							
							oldRouteid = p[i].idRoute;
						}
						if(p[i].idRoute == -1)
							pm = new YMaps.Placemark(new YMaps.GeoPoint(p[i].x,p[i].y),{draggable: false, style:"1bus#Peshehod"});			
						else {
						    if (p[i].route__transport_type == 1)
							pm = new YMaps.Placemark(new YMaps.GeoPoint(p[i].x,p[i].y),{draggable: false, style:"1bus#TramvayStation"});
						    else {
							if (p[i].route__transport_type == 2)
							    pm = new YMaps.Placemark(new YMaps.GeoPoint(p[i].x,p[i].y),{draggable: false, style:"1bus#MetroStation"});
							else {
							    if (p[i].route__transport_type == 3)
								pm = new YMaps.Placemark(new YMaps.GeoPoint(p[i].x,p[i].y),{draggable: false, style:"1bus#BusStation"});
							    else {
								if (p[i].route__transport_type == 4)
								    pm = new YMaps.Placemark(new YMaps.GeoPoint(p[i].x,p[i].y),{draggable: false, style:"1bus#TrolStation"});
								else
								    pm = new YMaps.Placemark(new YMaps.GeoPoint(p[i].x,p[i].y),{draggable: false, style:"1bus#PovorotStation"});
							    }}}}
						pm.name = p[i].stopName;
						pm.description = p[i].transportName + " t=" + p[i].t;
						Marks.add(pm);
						Line.addPoint(new YMaps.GeoPoint(p[i].x, p[i].y));
					    if(p[i].stopName == 'Finish'){ final_time = p[i].t }
					    if(p[i].TransportsType != undefined)
					    {
					    if(p[i].stopName == 'Start'){ human_readable = 'Пешком - ' + human_readable; }
					    else
					    {
						if(p[i].stopName == 'Finish'){ human_readable = 'Пешком' + human_readable; }
						else
						{
						    if(p[i].TransportsType == 'trolley'){p[i].TransportsType = 'Тс'}
						    if(p[i].TransportsType == 'Metro'){p[i].TransportsType = 'M.'}
						    if(p[i].TransportsType == 'tram'){p[i].TransportsType = 'Tй'}
						    if(p[i].TransportsType == 'bus'){p[i].TransportsType = 'А'}
						    if(p[i].routeName == 'SALTOVKA'){p[i].routeName = 'S'}
						    if(p[i].routeName == 'Holodnogorskaya'){p[i].routeName = 'H'}
						    if(p[i].routeName == 'Alekseevka'){p[i].routeName = 'A'}
						    if(p[i].TransportsType != a || p[i].routeName != b)
						    {
							a = p[i].TransportsType;
							b = p[i].routeName;
							human_readable = p[i].TransportsType + '(' + p[i].routeName + '' + ') -' + human_readable;
						    }
						}
					    }}
					    if(p[i].stopName != 'Start' && p[i].stopName != 'Finish' && p[i].TransportsType != undefined)
					    {
						human_readable2 = '<ul>' + p[i].TransportsType + '(' + p[i].routeName + ' )' + p[i].stopName + '--' + p[i].t + '</ul>' + human_readable2;
					    }
					}
				    human_readable2 = human_readable2 + '<input type="button" id="more3" value="Скрыть"></br>';
				    YMaps.jQuery('#human_readable2').html(human_readable2);
				    YMaps.jQuery('#human_readable2').hide();
				    YMaps.jQuery('#human_readable').html('<table border=1 cellspacing=0 width=800><tr><td>№</td><td>Время</td><td>Длительность</td><td>Цена</td><td>Транспорт</td></tr><tr><td>1</td><td></td><td>' + final_time + '</td><td></td><td>' + human_readable + '</td></tr></table><input type="button" id="more2" value="Подробней"></br>');
				    YMaps.jQuery("#more2").bind('click', function()
				    				{
				    				    YMaps.jQuery('#human_readable2').show();
				    				});
				    YMaps.jQuery("#more3").bind('click', function()
				    				{
				    				    YMaps.jQuery('#human_readable2').hide();
				    				});
				    Lines.add(Line);
				    map.addOverlay(Lines);								
				    map.addOverlay(Marks);
				    Start_x = Start_y = Finish_x = Finish_y = -1;
				    map.removeOverlay(placemark);
				} 
			};
			var url = "/route/?x1=" + encodeURI(Start_x) 
				+ "&y1=" + encodeURI(Start_y)
				+ "&x2=" + encodeURI(Finish_x) 
				+ "&y2=" + encodeURI(Finish_y)
			        + "&Transport1=" + YMaps.jQuery('#Transport1:checked').val()
			        + "&Transport2=" + YMaps.jQuery('#Transport2:checked').val()
			        + "&Transport3=" + YMaps.jQuery('#Transport3:checked').val()
			        + "&Transport4=" + YMaps.jQuery('#Transport4:checked').val();
			http_request.open("GET", url, true);
			http_request.send(null);
		}
		map.addOverlay(placemark);
		placemark.openBalloon();
	}, this);
	
	function addMenuItem (group, menuContainer, col) 
	{
		YMaps.jQuery("<a class=\"title\" href=\"#\">" + group.title + "</a><div style=\"z-index: 1; width: 100px; height: 10px; background-color:#"+col+"; layer-background-color:#"+col+"; visibility: visible\"></div>")			
			.bind("click", function () 
			{
				var link = YMaps.jQuery(this);
				if (link.hasClass("active")) 
				{
					map.removeOverlay(group);
				} else 
				{
					map.addOverlay(group);
				}
				link.toggleClass("active");
				return false;
			})
			.appendTo
			(
				YMaps.jQuery("<li></li>").appendTo(menuContainer)
			)
	};
	
	function BusInit()
	{
		map = new YMaps.Map(YMaps.jQuery("#YMapsID")[0]);
		
		Start_x = Start_y = Finish_x = Finish_y = -1;

		if (window.XMLHttpRequest) 
		{ 
			http_request = new XMLHttpRequest();
		}else if (window.ActiveXObject) 
		{ 
			http_request = new ActiveXObject("Microsoft.XMLHTTP");
		}
		http_request.overrideMimeType('text/xml');

		Marks = new YMaps.GeoObjectCollection();
		Lines = new YMaps.GeoObjectCollection();
		TransportMenu = new YMaps.GeoObjectCollection();
		
		map.addControl(new YMaps.TypeControl());
		map.addControl(new YMaps.Zoom());
		map.addControl(new YMaps.ScaleLine());
		map.addControl(new YMaps.ToolBar());
		map.setCenter(new YMaps.GeoPoint(36.21232000, 49.99702000),13);
	}
	
	function CreateStyles()
	{
		PeshehodStyle = new YMaps.Style();
		PeshehodStyle.iconStyle = new YMaps.IconStyle();
		PeshehodStyle.iconStyle.href = "/s/images/only_peshehod_small.png";
		PeshehodStyle.iconStyle.size = new YMaps.Point(30,40);
		PeshehodStyle.iconStyle.offset = new YMaps.Point(-15, -20);
		PeshehodStyle.hintContentStyle = new YMaps.HintContentStyle(new YMaps.Template("<b>$[name]</b><div>$[description]</div>"));
		PeshehodStyle.hasHint = true;
		YMaps.Styles.add("1bus#Peshehod", PeshehodStyle);
		
		TramvayStationStyle = new YMaps.Style();
		TramvayStationStyle.iconStyle = new YMaps.IconStyle();
		TramvayStationStyle.iconStyle.href = "/s/images/only_tramvay_small.png";
		TramvayStationStyle.iconStyle.size = new YMaps.Point(20, 14);
		TramvayStationStyle.iconStyle.offset = new YMaps.Point(-10, -7);
		TramvayStationStyle.hintContentStyle = new YMaps.HintContentStyle(new YMaps.Template("<b>$[name]</b><div>$[description]</div>"));
		TramvayStationStyle.hasHint = true;
		YMaps.Styles.add("1bus#TramvayStation", TramvayStationStyle);

		BusStationStyle = new YMaps.Style();
		BusStationStyle.iconStyle = new YMaps.IconStyle();
		BusStationStyle.iconStyle.href = "/s/images/only_bus_small.png";
		BusStationStyle.iconStyle.size = new YMaps.Point(20, 10);
		BusStationStyle.iconStyle.offset = new YMaps.Point(-10, -7);
		BusStationStyle.hintContentStyle = new YMaps.HintContentStyle(new YMaps.Template("<b>$[name]</b><div>$[description]</div>"));
		BusStationStyle.hasHint = true;
		YMaps.Styles.add("1bus#BusStation", BusStationStyle);

		TrolStationStyle = new YMaps.Style();
		TrolStationStyle.iconStyle = new YMaps.IconStyle();
		TrolStationStyle.iconStyle.href = "/s/images/only_trol_small.png";
		TrolStationStyle.iconStyle.size = new YMaps.Point(20, 14);
		TrolStationStyle.iconStyle.offset = new YMaps.Point(-10, -7);
		TrolStationStyle.hintContentStyle = new YMaps.HintContentStyle(new YMaps.Template("<b>$[name]</b><div>$[description]</div>"));
		TrolStationStyle.hasHint = true;
		YMaps.Styles.add("1bus#TrolStation", TrolStationStyle);


		MetroStationStyle = new YMaps.Style();
		MetroStationStyle.iconStyle = new YMaps.IconStyle();
		MetroStationStyle.iconStyle.href = "/s/images/only_metro_small.png";
		MetroStationStyle.iconStyle.size = new YMaps.Point(14, 14);
		MetroStationStyle.iconStyle.offset = new YMaps.Point(-10, -7);
		MetroStationStyle.hintContentStyle = new YMaps.HintContentStyle(new YMaps.Template("<b>$[name]</b><div>$[description]</div>"));
		MetroStationStyle.hasHint = true;
		YMaps.Styles.add("1bus#MetroStation", MetroStationStyle);

		PovorotStationStyle = new YMaps.Style();
		PovorotStationStyle.iconStyle = new YMaps.IconStyle();
		PovorotStationStyle.iconStyle.href = "/s/images/stop.png";
		PovorotStationStyle.iconStyle.size = new YMaps.Point(10, 10);
		PovorotStationStyle.iconStyle.offset = new YMaps.Point(-5, -5);
		PovorotStationStyle.hintContentStyle = new YMaps.HintContentStyle(new YMaps.Template("<b>$[name]</b><div>$[description]</div>"));
		PovorotStationStyle.hasHint = true;
		YMaps.Styles.add("1bus#PovorotStation", PovorotStationStyle);

		
		style = new YMaps.Style();
		style.polygonStyle = new YMaps.PolygonStyle();
		style.polygonStyle.fillColor = "FF0000FF";
		style.lineStyle = new YMaps.LineStyle();
		style.lineStyle.strokeColor = "FF0000FF";
		style.lineStyle.strokeWidth = 1;
		style.hasHint = true;
		YMaps.Styles.add("1bus#Peshkom", style);
		
		http_request.onreadystatechange = function()
		{
			if (http_request.readyState == 4) 
			{
				Transports = JSON.parse(http_request.responseText);
			        oldid = -1;
				var tstyle;
				var tline;
				for (var i in Transports)
				{
					if(Transports[i].route__id != oldid)
					{
						tstyle = new YMaps.Style();
						tstyle.polygonStyle = new YMaps.PolygonStyle();
						tstyle.polygonStyle.fillColor = Transports[i].route__color;
						tstyle.lineStyle = new YMaps.LineStyle();
						tstyle.lineStyle.strokeColor = Transports[i].route__color;
						tstyle.lineStyle.strokeWidth = 3;
						tstyle.hasHint = true;
						YMaps.Styles.add(Transports[i].route__id, tstyle);
						TransportMenuItem = new YMaps.GeoObjectCollection();
						TransportMenuItem.title = Transports[i].route__route;
						c = Transports[i].route__color[0] + Transports[i].route__color[1] + Transports[i].route__color[2] + Transports[i].route__color[3] + Transports[i].route__color[4] + Transports[i].route__color[5];
					    if(Transports[i].route__transport_type == 1)
					    {
						addMenuItem(TransportMenuItem, YMaps.jQuery("#menu1"), c);
					    }
					    if(Transports[i].route__transport_type == 2)
					    {
						addMenuItem(TransportMenuItem, YMaps.jQuery("#menu2"), c);
					    }
					    if(Transports[i].route__transport_type == 3)
					    {
						addMenuItem(TransportMenuItem, YMaps.jQuery("#menu3"), c);
					    }
					    if(Transports[i].route__transport_type == 4)
					    {
						addMenuItem(TransportMenuItem, YMaps.jQuery("#menu4"), c);
					    }

						tline = new YMaps.Polyline();
						TransportMenuItem.add(tline);
						tline.setStyle(tstyle);
					}
				    if(Transports[i].route__transport_type == 1)
					    {
						pm = new YMaps.Placemark(new YMaps.GeoPoint(Transports[i].coordinate_x,Transports[i].coordinate_y),{draggable: false, style:TramvayStationStyle});
					    }
				        else {
					    if(Transports[i].route__transport_type == 2)
						pm = new YMaps.Placemark(new YMaps.GeoPoint(Transports[i].coordinate_x,Transports[i].coordinate_y),{draggable: false, style:MetroStationStyle});
					    else {
						if(Transports[i].route__transport_type == 3)
						    pm = new YMaps.Placemark(new YMaps.GeoPoint(Transports[i].coordinate_x,Transports[i].coordinate_y),{draggable: false, style:BusStationStyle});
						else {
						pm = new YMaps.Placemark(new YMaps.GeoPoint(Transports[i].coordinate_x,Transports[i].coordinate_y),{draggable: false, style:TrolStationStyle});
					    }}}	
					pm.name = Transports[i].name;
					pm.description = Transports[i].route__route;
					TransportMenuItem.add(pm);
					tline.addPoint(new YMaps.GeoPoint(Transports[i].coordinate_x, Transports[i].coordinate_y));											
					oldid = Transports[i].route__id;
				}

			} 

		};
	        http_request.open("GET", "/transport_list/", true);
		http_request.send(null);		

	}
})

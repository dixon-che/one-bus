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
						else
							pm = new YMaps.Placemark(new YMaps.GeoPoint(p[i].x,p[i].y),{draggable: false, style:"1bus#TramvayStation"});			
						pm.name = p[i].stopName;
						pm.description = p[i].transportName + " t=" + p[i].t;
						Marks.add(pm);
						Line.addPoint(new YMaps.GeoPoint(p[i].x, p[i].y));
					}
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
				+ "&y2=" + encodeURI(Finish_y);
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
						addMenuItem(TransportMenuItem, YMaps.jQuery("#menu"), c);
						tline = new YMaps.Polyline();
						TransportMenuItem.add(tline);
						tline.setStyle(tstyle);
					}
					pm = new YMaps.Placemark(new YMaps.GeoPoint(Transports[i].coordinate_x,Transports[i].coordinate_y),{draggable: false, style:TramvayStationStyle});
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

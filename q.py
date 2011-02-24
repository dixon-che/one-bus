    while next_points_list:
		len_in = min(mass_next_points_list)
		index_start_point = mass_next_points_list.index(len_in)
		point_in = next_points_list[index_start_point]
		route_key = Station.objects.get(matrix_index=point_in).route_id
		if route_dict[route_key] == 1:
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
				list_station_in_route[station_in] += len_in
			dinamic_list[zero_order:slys_order + 1] = list_station_in_route
			list_index = range(zero_order, slys_order + 1)
			for ob_element in list_index:
                    # Если попалась остановка из списка радиуса finish мы её записываем в список с ключём finish.
				if ob_element in points_in_radius_finish and dinamic_list[-1] > dinamic_list[zero_order:slys_order + 1][list_index.index(ob_element)] + len_list_start_finish[1][points_in_radius_finish.index(ob_element)]:
					dinamic_list[-1] = dinamic_list[zero_order:slys_order + 1][list_index.index(ob_element)]
				route_dict[route_key] = 0
                # Считаем все переходы записываем соответствующие значения в словарь и закрываем маршрут.
				for para in metastations_stations_list:
					if ob_element == para[0]:
						if para[1] not in next_points_list and dinamic_list[para[1]] > dinamic_list[ob_element] + speed_matrix[ob_element][para[1]] and para[1] not in list_index:
								dinamic_for = dinamic_list[ob_element] + speed_matrix[ob_element][para[1]]
								next_points_list += [para[1]]
								mass_next_points_list += [dinamic_for]
								if para[1] in points_in_radius_finish:
									dinamic_list[-1] = dinamic_for
            # сравниваем с точкой finish если минимальная меньше идём дальше иначе выходим из цикла
		if min(mass_next_points_list) > dinamic_list[-1]:
			break
		next_points_list.remove(point_in)
		mass_next_points_list.remove(len_in)         


#!/usr/bin/env python
# -*- coding: utf-8 -*-


from apps.point.models import Station

for s in Station.objects.all():
    s.matrix_index=1
    s.save()
    i+=1


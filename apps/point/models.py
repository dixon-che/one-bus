from django.db import models



class Transport(models.Model):
    name = models.CharField(max_length=155)
    ico = models.ImageField(upload_to="ico_transport")
    price = models.IntegerField()

class Route(models.Model):
    transport = models.ForeignKey(Transport)
    route = models.CharField(max_length=155)
    interval = models.IntegerField()
    speed = models.IntegerField()
    price = models.IntegerField()

class Point(models.Model):
    route = models.ForeignKey(Route)
    name = models.CharField(max_length=155)
    coordinate_x = models.IntegerField()
    coordinate_y = models.IntegerField()

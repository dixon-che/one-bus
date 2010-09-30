from django.db import models



class Transport(models.Model):
    name = models.CharField(max_length=155)
    ico = models.ImageField(upload_to="ico_transport")
    price = models.FloatField()
    description = models.TextField()

    def __unicode__(self):
        return self.name

class Route(models.Model):
    transport_type = models.ForeignKey(Transport)
    route = models.CharField(max_length=155)
    interval = models.FloatField()
    speed = models.FloatField()
    price = models.FloatField() 
    one_pay = models.BooleanField()

    def __unicode__(self):
        return self.route

class Metastation(models.Model):
    name = models.CharField(max_length=55)
    address = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class Station(models.Model):
    route = models.ForeignKey(Route)
    name = models.CharField(max_length=155)
    coordinate_x = models.FloatField()
    coordinate_y = models.FloatField()
    next_station = models.CharField(max_length=155)
    prev_station = models.CharField(max_length=155)
    meta_station = models.ForeignKey(Metastation)

    def __unicode__(self):
        return self.name

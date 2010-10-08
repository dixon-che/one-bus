from django.db import models


class Transport(models.Model):
    name = models.CharField(max_length=155)
    ico = models.ImageField(upload_to="ico_transport")
    price = models.FloatField()
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Route(models.Model):
    transport_type = models.ForeignKey(Transport)
    route = models.CharField(max_length=155)
    interval = models.FloatField()
    speed = models.FloatField()
    price = models.FloatField() 
    one_pay = models.BooleanField()

    class Meta:
        ordering = ['route']

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
    order = models.IntegerField()
    meta_station = models.ForeignKey(Metastation)

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.name

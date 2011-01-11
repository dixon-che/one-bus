from django.db import models
from apps.point.customfields import HexColorField


class Transport(models.Model):
    name = models.CharField(max_length=155)
    ico = models.ImageField(upload_to="images")
    price = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True, blank=True, null=True)

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
    color = HexColorField(max_length=8)
    timestamp = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        ordering = ['route']

    def __unicode__(self):
        return self.route


class Onestation(models.Model):
    name = models.CharField(max_length=155)
    coordinate_x = models.FloatField()
    coordinate_y = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Station(models.Model):
    route = models.ForeignKey(Route)
    name = models.CharField(max_length=255)
    coordinate_x = models.FloatField()
    coordinate_y = models.FloatField()
    order = models.IntegerField(blank=True, null=True)
    one_station = models.ForeignKey(Onestation, blank=True, null=True)
    matrix_index = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True, blank=True, null=True)
    notstations = models.BooleanField()

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.name

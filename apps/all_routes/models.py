from django.db import models


class Routes(models.Model):
    start_point = models.IntegerField()
    finish_point = models.IntegerField()
    route = models.TextField()

from builtins import staticmethod

from django.db import models


# Create your models here.

class Config(models.Model):
    last_pulled_index = models.IntegerField(default=0)

    @staticmethod
    def get_config():
        if Config.objects.count() == 0:
            return Config.objects.create()
        return Config.objects.first()

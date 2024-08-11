from django.db import models


class Config(models.Model):
    last_pulled_index = models.IntegerField(default=0)

    @staticmethod
    def get_config():
        if Config.objects.count() == 0:
            return Config.objects.create()
        return Config.objects.first()

class ZellularTransaction(models.Model):
    PULL = 'pull'
    PUSH = 'push'
    TYPES = (
        (PULL, 'Pull'),
        (PUSH, 'Push'),
    )

    type = models.CharField(max_length=4, choices=TYPES)
    method = models.CharField(max_length=255)
    data = models.JSONField(default=dict)

    def __str__(self):
        return f'{self.id} - {self.type}:{self.method}'
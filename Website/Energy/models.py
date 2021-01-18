from django.db import models

class Observation(models.Model):
    building = models.CharField(max_length = 150, unique = False, null = True)
    Time = models.DateTimeField(max_length = 150, unique = False, null = True)
    Quantity = models.FloatField(unique = False, null = True)

    def __str__(self):
        return self.building

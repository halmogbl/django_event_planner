from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=255)
    location = models.CharField(max_length=120)
    date = models.DateField()
    time = models.TimeField()
    seats = models.IntegerField()
    added_by = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

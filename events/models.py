from django.db import models
from django.contrib.auth.models import User

class Events(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=255)
    location = models.CharField(max_length=120)
    date = models.DateField()
    time = models.TimeField()
    seats = models.IntegerField()

class Tickets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    

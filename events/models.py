from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=255)
    location = models.CharField(max_length=120)
    date = models.DateField()
    time = models.TimeField()
    seats = models.IntegerField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='events')

    def seats_left(self):
        booked = sum(self.tickets.all().values_list('tickets', flat=True))
        return self.seats - booked


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='tickets')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=1, related_name='tickets')
    datetime = models.DateTimeField(auto_now=True)
    tickets = models.IntegerField(default=0)


class Following(models.Model):
	user_follow = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_follow')
	user_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_followed')

	def __str__(self):
		return "%s favorited %s"%(self.user_follow.username, self.user_followed.username)




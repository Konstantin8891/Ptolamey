from django.db import models

from users.models import User


class Room(models.Model):
    number_or_title = models.CharField(max_length=20, unique=True)
    cost = models.FloatField()
    population = models.SmallIntegerField()
    users = models.ManyToManyField(
        User, through='BookingUser', related_name='rooms'
    )

    def __str__(self):
        return self.number_or_title


class BookingUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date_start = models.DateField()
    date_end = models.DateField()

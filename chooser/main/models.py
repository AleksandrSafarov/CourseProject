import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Voting(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(hours=3))

class VoteFor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Votes for"

class VoteAgainst(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Votes against"

class StaffRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)
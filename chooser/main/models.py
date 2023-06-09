import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Voting(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(hours=3))

    def get_datetime(self):
        return f'{str(self.date.day).zfill(2)}.{str(self.date.month).zfill(2)}.{self.date.year}'

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

class Complaint(models.Model):
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(default="")
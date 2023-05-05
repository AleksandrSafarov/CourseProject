import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Theme(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(hours=3))

class VoteFor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "VotesFor"

class VoteAgainst(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "VotesAgainst"
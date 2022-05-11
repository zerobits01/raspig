from django.contrib.auth.models import User
from django.db import models


class Goal(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    tasks = models.JSONField(default=[], null=False, blank=False)
    point = models.IntegerField(default=1, null=False, blank=False)
    done = models.BooleanField(default=False, null=False, blank=False)


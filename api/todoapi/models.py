from django.contrib.auth.models import User
from django.db import models


class ToDo(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    description = models.TextField(max_length=256)
    weight = models.IntegerField(default=1, null=False, blank=False)
    
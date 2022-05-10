from django.contrib.auth.models import User
from django.db import models


class ToDo(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    t1 = models.TextField(max_length=256)
    t2 = models.TextField(max_length=256)
    t3 = models.TextField(max_length=256)
    t4 = models.TextField(max_length=256)
    t1_done = models.BooleanField(default=False, null=False, blank=False)
    t2_done = models.BooleanField(default=False, null=False, blank=False)
    t3_done = models.BooleanField(default=False, null=False, blank=False)
    t4_done = models.BooleanField(default=False, null=False, blank=False)
    weight = models.IntegerField(default=1, null=False, blank=False)
    done = models.BooleanField(default=False, null=False, blank=False)


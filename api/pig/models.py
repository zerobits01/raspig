from django.db import models
from django.contrib.auth.models import User


class Pig(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    uuid  = models.CharField(max_length=255, unique=True, null=False, blank=False)
    point_count = models.IntegerField(default=0, null=False, blank=False)
    get_new_task_count = models.IntegerField(default=0, null=False, blank=False)
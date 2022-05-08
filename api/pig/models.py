from django.db import models
from django.contrib.auth.models import User


class Pig(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid  = models.CharField(max_length=255, unique=True, null=False, blank=False)    
from django.contrib.auth.models import Group
from django.db import models

class CustomGroup(models.Model):
        """
        Overwrites original Django Group.
        """
        def __str__(self):
            return "{}".format(self.group.name)

        group = models.OneToOneField('auth.Group', unique=True, on_delete=models.CASCADE,)
        picture_size = models.EmailField(max_length=70, blank=True, default="")
from django.db import models
from django.conf import settings

# Create your models here.
class Picture(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    uploaded=models.ImageField(null=False, blank=False,upload_to="images/")
    class Meta:
        permissions = [
            ("change_task_status", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        ]
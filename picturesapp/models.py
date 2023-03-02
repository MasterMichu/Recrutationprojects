from django.db import models
from django.conf import settings

# Create your models here.
class Picture(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    uploaded = models.ImageField(null=False, blank=False, upload_to="images/")
    def __str__(self):
        return self.name
    class Meta:
        permissions = [
            ("arbitrary thumbnail sizes", "Will recive arbitrary thumbnail sizes"),
            ("Originally uploaded picture", "presence of the link to the originally uploaded file"),
            ("Generate expiring links", "Ability to generate expiring links with custom expiration time"),
            ("200px thumbnail", "Ability to generate 200px thumbnail"),
            ("400px thumbnail", "Ability to generate 400px thumbnail"),
        ]
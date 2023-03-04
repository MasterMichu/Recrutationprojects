from django.forms import ModelForm
from .models import Picture, Expiringlink


class Pictureform(ModelForm):

    class Meta:
        model = Picture
        fields = ("name", "uploaded")


class Expiringlinkform(ModelForm):
    class Meta:
        model = Expiringlink
        fields = ("duration",)

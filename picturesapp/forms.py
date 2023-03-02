from django import forms
from django.forms import ModelForm
from .models import Picture


#create form
class Pictureform(ModelForm):

    class Meta:
        model = Picture
        fields = ("name", "uploaded")
        #widgets={"user":forms.HiddenInput()}

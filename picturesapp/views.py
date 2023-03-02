from django.shortcuts import render
from .models import Picture
from .forms import Pictureform
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def add_picture(request):
    submitted=False
    if request.method=="POST":
        form = Pictureform(request.POST, request.FILES)
        if form.is_valid():
            print("form is valid")
            fs=form.save(commit=False)
            fs.user=request.user
            fs.save()
        return HttpResponseRedirect('/add_picture?submitted=True')
    else:
        form=Pictureform
        if 'submitted' in request.GET:
            submitted=True
    return render(request,"add_picture.html",{"form": form, "submitted": submitted})


@login_required
def all_pictures(request):
    picture_list = Picture.objects.filter(user=request.user)
    return render(request,"pictures_list.html",{"pictures_list": picture_list})

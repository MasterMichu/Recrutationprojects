from django.shortcuts import render
from .models import Picture
from .forms import Pictureform
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
import requests

from PIL import Image
import os
# Create your views here.


@login_required
def add_picture(request):
    submitted=False
    if request.method=="POST":
        form = Pictureform(request.POST, request.FILES)
        if form.is_valid():
            print("form is valid")
            fs = form.save(commit=False)
            fs.user = request.user
            if verify_picture(fs.uploaded):
                pict=fs.uploaded
                fs.save()
                shrink_picture(pict, request)
            else:
                fs.uploaded = None
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
    print(picture_list)
    print(request.user.has_perm("picturesapp.arbitrary_thumbnail_sizes"))
    print(request.user.has_perm("picturesapp.Originally_uploaded_picture"))
    print(request.user.has_perm("picturesapp.Generate_expiring_links"))
    print(request.user.has_perm("picturesapp.200px_thumbnail"))
    print(request.user.has_perm("picturesapp.400px_thumbnail"))
    return render(request,"pictures_list.html",{
        "pictures_list": picture_list,
        "200px_thumbnail": request.user.has_perm("picturesapp.200px_thumbnail"),
        "400px_thumbnail": request.user.has_perm("picturesapp.400px_thumbnail"),
        "Originally_uploaded_picture": request.user.has_perm("picturesapp.Originally_uploaded_picture"),
        "arbitrary_thumbnail_sizes": request.user.has_perm("picturesapp.arbitrary_thumbnail_sizes"),
        "Generate_expiring_links": request.user.has_perm("picturesapp.Generate_expiring_links"),
    })


def verify_picture(file):
    ext=os.path.splitext(file.name)[-1].lower()
    if ext==".jpg" or ext==".png":
        print("mamy zdjecie")
        return True
    else:
        return False


def shrink_picture(file,request):
    if request.user.has_perm("picturesapp.Originally_uploaded_picture"):
        print("oryginal")
        return file
    else:
        resolution=bigest_picture_posible_for_user(request)
        print(resolution)
        mediapath = "media/"
        print(os.path.join(mediapath,file.name))
        newname=os.path.join(mediapath,file.name)
        size = (resolution, resolution,)
        im = Image.open(file)
        im.thumbnail(size)

        im.save("media/"+ file.name, "JPEG")
        im.show()
        return im


def bigest_picture_posible_for_user(request):
    top_resolution = 0
    if request.user.has_perm("picturesapp.arbitrary_thumbnail_sizes"):
        top_resolution = get_arbitrary_picturesize(request)
    if request.user.has_perm("picturesapp.400px_thumbnail"):
        if top_resolution < 400:
            top_resolution = 400
    if request.user.has_perm("picturesapp.200px_thumbnail"):
        if top_resolution < 200:
            top_resolution = 200
    return top_resolution


def get_arbitrary_picturesize(request):
    group = Group.objects.get(name=request.user.groups.all()[0].name)  # example name
    arbitrary_picturesize = group.customgroup.picture_size
    print(arbitrary_picturesize)
    return arbitrary_picturesize
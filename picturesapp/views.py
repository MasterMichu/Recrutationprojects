from django.shortcuts import render, redirect
from .models import Picture, Expiringlink
from .forms import Pictureform, Expiringlinkform
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
import hashlib
import time
from urllib.parse import urlencode
from PIL import Image
import os
# Create your views here.


@login_required
def add_picture(request):
    if request.method == "POST":
        form = Pictureform(request.POST, request.FILES)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.user = request.user
            if verify_picture(fs.uploaded):
                pict = fs.uploaded
                fs.save()
                shrink_picture(pict, request)
            else:
                fs.uploaded = None
                fs.save()

        return all_pictures(request)
    else:
        form = Pictureform
    return render(request, "add_picture.html", {"form": form, })


@login_required
def all_pictures(request):
    picture_list = Picture.objects.filter(user=request.user)
    arbitrary_size = 0
    if request.user.has_perm("picturesapp.arbitrary_thumbnail_sizes"):
        arbitrary_size = get_arbitrary_picturesize(request)
    return render(request, "pictures_list.html", {
        "pictures_list": picture_list,
        "200px_thumbnail": request.user.has_perm("picturesapp.200px_thumbnail"),
        "400px_thumbnail": request.user.has_perm("picturesapp.400px_thumbnail"),
        "Originally_uploaded_picture": request.user.has_perm("picturesapp.Originally_uploaded_picture"),
        "arbitrary_thumbnail_sizes": request.user.has_perm("picturesapp.arbitrary_thumbnail_sizes"),
        "Generate_expiring_links": request.user.has_perm("picturesapp.Generate_expiring_links"),
        "arbitrary_size": arbitrary_size,
    })


def view_image(request):
    imagesrc = request.GET['image']
    imagesize = request.GET['size']
    create_temporary_thumbnail(imagesrc, imagesize)
    return render(request, "view_picture.html", {"imagesrc": "temporary/tempict.jpg", })


def generate_expiring(request):
    if request.method == "POST":
        form = Expiringlinkform(request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.linkto = Picture.objects.filter(uploaded=request.GET["image"])[0]
            validuntil = int(time.time())+fs.duration
            fs.validuntil = validuntil
            hash_object = hashlib.md5(request.GET["image"].encode("ascii"))
            fs.link = hash_object.hexdigest()
            fs.save()
            base_url = '/showexpiring'
            query_string = urlencode({'hashed': hash_object.hexdigest()})  # 2 category=42
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)
    else:
        form = Expiringlinkform
        return render(request, "expiring.html", {"form": form, })


def show_expiring(request):
    expiringlink = request.GET['hashed']
    expiringlinkobject = Expiringlink.objects.filter(link=expiringlink).latest("id")
    if expiringlinkobject.validuntil < int(time.time()):
        return render(request, "expiring_picture.html", {"imagesrc": "temporary/tempict.jpg", "expired": True, })
    else:
        picturelink = expiringlinkobject.linkto
        src = str(picturelink.uploaded)
        create_temporary_thumbnail(src, 0)
        return render(request, "expiring_picture.html", {"imagesrc": "temporary/tempict.jpg", "expired": False, })
    pass


def verify_picture(file):
    ext = os.path.splitext(file.name)[-1].lower()
    if ext == ".jpg" or ext == ".png":
        return True
    else:
        return False


def shrink_picture(file, request):
    if request.user.has_perm("picturesapp.Originally_uploaded_picture"):

        return file
    else:
        resolution = bigest_picture_posible_for_user(request)
        size = (resolution, resolution,)
        im = Image.open(file)
        im.thumbnail(size)
        im.save("media/" + file.name, "JPEG")
        return im


def create_temporary_thumbnail(file, size):
    thumbnailsize = (int(size), int(size),)
    im = Image.open("media/"+file)
    if int(size) > 0:
        im.thumbnail(thumbnailsize)
    im.save("media/temporary/tempict.jpg", "JPEG")
    pass


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
    return arbitrary_picturesize

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

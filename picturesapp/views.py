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
    print(request.user.has_perm("picturesapp.arbitrary thumbnail sizes"))
    print(request.user.has_perm("picturesapp.Originally uploaded picture"))
    print(request.user.has_perm("picturesapp.Generate expiring links"))
    print(request.user.has_perm("picturesapp.200px thumbnail"))
    print(request.user.has_perm("picturesapp.400px thumbnail"))
    return render(request,"pictures_list.html",{
        "pictures_list": picture_list,
        "200px thumbnail":request.user.has_perm("picturesapp.200px thumbnail"),
        "400px thumbnail":request.user.has_perm("picturesapp.400px thumbnail"),
        "Originally uploaded picture":request.user.has_perm("picturesapp.Originally uploaded picture"),
        "arbitrary thumbnail sizes":request.user.has_perm("picturesapp.arbitrary thumbnail sizes"),
        "Generate expiring links":request.user.has_perm("picturesapp.Generate expiring links"),
    })

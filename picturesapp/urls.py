from django.urls import path
from . import views
urlpatterns = [
    path("pictures_list",views.all_pictures,name="list-pictures"),
    path("add_picture",views.add_picture,name="add-pictures"),
    path("",views.all_pictures,name="list-pictures"),
]
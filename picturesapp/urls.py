from django.urls import path
from . import views
urlpatterns = [
    path("pictures_list", views.all_pictures, name="list-pictures"),
    path("add_picture", views.add_picture, name="add-pictures"),
    path("images", views.view_image, name="view-pictures"),
    path("expiring", views.generate_expiring, name='expiringlink'),
    path("showexpiring", views.show_expiring, name='link_will_expire'),
    path("", views.all_pictures, name="list-pictures"),
]

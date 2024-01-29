from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("mylistings/", views.mylistings, name="mylistings"),
    path("<str:listing_id>/makebid/", views.makebid, name="makebid"),
    path("<str:listing_id>/", views.listinfo, name="listinfo"),
]

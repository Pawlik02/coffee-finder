from django.urls import path
from django.views.generic.base import RedirectView
from . import views

app_name = "coffee_finder"

urlpatterns = [
    path("",views.index,name="index"),
    path("signup/",views.signup,name="signup"),
    path("login/",views.login_handler,name="login"),
    path("favourites_handler/",views.js_favourites_handler,name="favourites_request"),
    path("favourites/favourites_delete/",views.js_favourites_delete,name="favourites_delete"),
    path("favourites/",views.favourites,name="favourites"),
    path("favourites/<place>/",views.place,name="place")
]
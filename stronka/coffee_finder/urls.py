from django.urls import path
from . import views

app_name = "coffee_finder"
urlpatterns = [
    path("",views.index,name="index"),
    path("signup/",views.signup,name="signup"),
    path("login/",views.login_handler,name="login"),
    path("favourites_handler/",views.js_favourites_handler,name="favourites_request"),
    path("favourites/",views.favourites,name="favourites"),
    path("favourites/<str:place>/",views.place,name="place")
]

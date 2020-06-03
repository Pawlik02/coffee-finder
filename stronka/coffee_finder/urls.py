from django.urls import path
from . import views

app_name = "coffee_finder"
urlpatterns = [
    path("",views.index,name="index"),
    path("signup/",views.signup,name="signup"),
    path("login/",views.login_handler,name="login"),
    path("favourite_handler/",views.js_favourite_handler,name="favourite_request"),
    path("favourites/",views.favourites,name="favourites")
]

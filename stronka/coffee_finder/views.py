import requests
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Profile, Places, Favourites, Rejected

api_key = "AIzaSyA10sWJ6IOVGEIyHuygj8tIBDKr8RjDyEU"

def index(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse("coffee_finder:login"))

    # INFO BAR
    username = request.user
    profile = Profile.objects.get()
    location = profile.location

    # Jak nie ma propozycji to ładuje nowe
    if len(Places.objects.all())==0:
        response = requests.post("https://maps.googleapis.com/maps/api/place/textsearch/json?query="+location+"&type=cafe&key="+api_key)
        response = json.loads(response.text)
        if response["status"] == "OK":
            info = response["results"]
            for i in range(len(info)):
                Places.objects.create(profile=profile,my_places=info[i])
        else:
            return render(request,"coffee_finder/index.html",{"name":"NO INFORMATION","location":location,"username":username,"formatted_address":"NO INFORMATION"})

    info = Places.objects.all()[0].my_places
    formatted_address = info["formatted_address"]
    name = info["name"]
    if 'opening_hours' in info:
        isopen = info["opening_hours"]
        isopen = isopen["open_now"]

        if "photos" in info:
            photo = info["photos"]
            photo = photo[0]
            photo = photo["photo_reference"]
            photo = "https://maps.googleapis.com/maps/api/place/photo?maxheight=800&photoreference="+photo+"&key="+api_key
        else:
            photo = "https/://maps.googleapis.com/maps/api/place/photo?maxheight=800&photoreference=CmRaAAAAZOkFJe830BVBm2Glk2rOxwMSnEtkR5PO1z1_VSMmxiPbdQkWLFzVXX9enkSdqECGHVDM4Qxt4bQIrfEajTi6NNsQVtwzskFXGT_pgxi6kH9sF8yr7JPQfJxSCW7H0xWQEhAVC39nIeFLkTiTxSaLoMydGhT14LkzvSTbfg2F74__oiET-t8ltA&key=AIzaSyA10sWJ6IOVGEIyHuygj8tIBDKr8RjDyEU"
        v_id = info["id"]

        if request.method == "POST":
            location = request.POST.get("location")
            user = request.user
            Profile.objects.update(user=user,location=location)
            Places.objects.all().delete()
        return render(request,"coffee_finder/index.html",{"name":name,"location":location,"username":username,"formatted_address":formatted_address,"photo":photo,"id":v_id,"isopen":isopen})
    else:
        if "photos" in info:
            photo = info["photos"]
            photo = photo[0]
            photo = photo["photo_reference"]
            photo = "https://maps.googleapis.com/maps/api/place/photo?maxheight=800&photoreference="+photo+"&key="+api_key
        else:
            photo = "https://maps.googleapis.com/maps/api/place/photo?maxheight=800&photoreference=CmRaAAAAZOkFJe830BVBm2Glk2rOxwMSnEtkR5PO1z1_VSMmxiPbdQkWLFzVXX9enkSdqECGHVDM4Qxt4bQIrfEajTi6NNsQVtwzskFXGT_pgxi6kH9sF8yr7JPQfJxSCW7H0xWQEhAVC39nIeFLkTiTxSaLoMydGhT14LkzvSTbfg2F74__oiET-t8ltA&key=AIzaSyA10sWJ6IOVGEIyHuygj8tIBDKr8RjDyEU"
        v_id = info["id"]

        if request.method == "POST":
            location = request.POST.get("location")
            user = request.user
            Profile.objects.update(user=user,location=location)
            Places.objects.all().delete()
        return render(request,"coffee_finder/index.html",{"name":name,"location":location,"username":username,"formatted_address":formatted_address,"photo":photo,"id":v_id,"isopen":"NO INFORMATION"})        

def favourites(request):
    username = request.user
    counter = []
    counter = range(10)
    return render(request,"coffee_finder/favourites.html",{"counter":counter,"username":username})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username,password=raw_password)
            login(request,user)
            user = request.user
            profile = Profile(user=user)
            profile.save()
            return HttpResponseRedirect(reverse("coffee_finder:index"))
    else:
        form = UserCreationForm()
    return render(request,"coffee_finder/signup.html",{"form":form})

def login_handler(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            return HttpResponseRedirect(reverse("coffee_finder:index"))
        else:
            return HttpResponse("Wrong data")
    return render(request, "coffee_finder/login.html")

def js_favourites_handler(request):
    profile = Profile.objects.get()
    if request.method == "GET":
        # handle right swipe
        if request.GET["direction"] == "right" :
            right = Places.objects.all()[0]
            Favourites.objects.create(profile=profile,my_favourites=right.my_places)
            right.delete()
            return HttpResponse("Wybrałeś prawo")
        # handle left swipe
        elif request.GET["direction"] == "left" :
            left = Places.objects.all()[0]
            Rejected.objects.create(profile=profile,my_rejected=left.my_places)
            left.delete()
            return HttpResponse("Wybrałeś lewo")
        # handle middle
        else :
            return HttpResponse("Wybrałeś środek")

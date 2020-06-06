import requests
import json
import time
import threading
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.template.defaulttags import register
from .models import Profile, Places, Favourites, Rejected

api_key = "AIzaSyA10sWJ6IOVGEIyHuygj8tIBDKr8RjDyEU"

def ParsedCafeData(info):
    formatted_address = info["formatted_address"]
    name = info["name"]
    if "opening_hours" in info and "open_now" in info["opening_hours"]:
        isopen = info["opening_hours"]
        isopen = isopen["open_now"]
    else:
        isopen = "No data"

    if "photos" in info:
        photo = info["photos"]
        photo = photo[0]
        photo = photo["photo_reference"]
        photo = "https://maps.googleapis.com/maps/api/place/photo?maxheight=800&photoreference="+photo+"&key="+api_key
    else:
        photo = "https://maps.googleapis.com/maps/api/place/photo?maxheight=800&photoreference=CmRaAAAAZOkFJe830BVBm2Glk2rOxwMSnEtkR5PO1z1_VSMmxiPbdQkWLFzVXX9enkSdqECGHVDM4Qxt4bQIrfEajTi6NNsQVtwzskFXGT_pgxi6kH9sF8yr7JPQfJxSCW7H0xWQEhAVC39nIeFLkTiTxSaLoMydGhT14LkzvSTbfg2F74__oiET-t8ltA&key=AIzaSyA10sWJ6IOVGEIyHuygj8tIBDKr8RjDyEU"
    return {"name":name,"formatted_address":formatted_address,"photo":photo,"isopen":isopen}

def NextPage(response,location,profile,username,request):
    while "next_page_token" in response:
        time.sleep(1.51)
        next_page_token = response["next_page_token"]
        response = requests.post("https://maps.googleapis.com/maps/api/place/textsearch/json?query="+location+"&type=cafe&pagetoken="+next_page_token+"&key="+api_key)
        response = json.loads(response.text)
        if response["status"] == "OK":
            info = response["results"]
            for i in range(len(info)):
                Places.objects.create(profile=profile,my_places=info[i])
        else:
            return render(request,"coffee_finder/index.html",{"name":"NO DATA","location":location,"username":username,"formatted_address":"NO DATA","photo":"NO PHOTO","isopen":"NO DATA"})

def index(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse("coffee_finder:login"))

    # INFO BAR
    username = request.user
    profile = Profile.objects.filter(user=request.user).get()
    location = profile.location
    # Jak nie ma propozycji to ładuje nowe
    if len(profile.places_set.all())==0:
        response = requests.post("https://maps.googleapis.com/maps/api/place/textsearch/json?query="+location+"&type=cafe&key="+api_key)
        response = json.loads(response.text)
        if response["status"] == "OK":
            info = response["results"]
            for i in range(len(info)):
                Places.objects.create(profile=profile,my_places=info[i])
        else:
            return render(request,"coffee_finder/index.html",{"name":"NO DATA","location":location,"username":username,"formatted_address":"NO DATA","photo":"NO PHOTO","isopen":"NO DATA"})

        stuff = threading.Thread(target=NextPage, name="\n", args=[response,location,profile,username,request])
        stuff.start()
    data = ParsedCafeData(profile.places_set.all()[0].my_places)

    if request.method == "POST":
        previous_location = location
        location = request.POST.get("location")
        user = request.user
        Profile.objects.filter(user=user).update(user=user,location=location)

        response = requests.post("https://maps.googleapis.com/maps/api/place/textsearch/json?query="+location+"&type=cafe&key="+api_key)
        response = json.loads(response.text)
        if response["status"] == "OK":
            profile.places_set.filter(profile=profile).delete()
            info = response["results"]
            for i in range(len(info)):
                Places.objects.create(profile=profile,my_places=info[i])
            stuff = threading.Thread(target=NextPage, name="\n", args=[response,location,profile,username,request])
            stuff.start()
        else:
            Profile.objects.filter(user=user).update(user=user,location=previous_location)
            location = previous_location
            return render(request,"coffee_finder/index.html",{"name":"NO DATA","location":location,"username":username,"formatted_address":"NO DATA","photo":"NO PHOTO","isopen":"NO DATA"})

    return render(request,"coffee_finder/index.html",{"name":data["name"],"location":location,"username":username,"formatted_address":data["formatted_address"],"photo":data["photo"],"isopen":data["isopen"]})

@register.filter
def get_item(dict,key):
    return dict.get(key)

def favourites(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse("coffee_finder:login"))
    profile = Profile.objects.filter(user=request.user).get()
    username = request.user
    location = profile.location
    favourites = []

    for object in profile.favourites_set.all():
        favourites.append(ParsedCafeData(object.my_favourites))

    return render(request,"coffee_finder/favourites.html",{"username":username,"location":location,"favourites":favourites})

def place(request, place):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse("coffee_finder:login"))
    profile = Profile.objects.filter(user=request.user).get()
    username = request.user
    location = profile.location
    name = place
    for object in profile.favourites_set.all():
        if object.my_favourites["name"] == name:
            if "photos" in object.my_favourites:
                photo = object.my_favourites["photos"]
                photo = photo[0]
                photo = photo["photo_reference"]
                photo = "https://maps.googleapis.com/maps/api/place/photo?maxheight=800&photoreference="+photo+"&key="+api_key
            else:
                photo = "https://maps.googleapis.com/maps/api/place/photo?maxheight=800&photoreference=CmRaAAAAZOkFJe830BVBm2Glk2rOxwMSnEtkR5PO1z1_VSMmxiPbdQkWLFzVXX9enkSdqECGHVDM4Qxt4bQIrfEajTi6NNsQVtwzskFXGT_pgxi6kH9sF8yr7JPQfJxSCW7H0xWQEhAVC39nIeFLkTiTxSaLoMydGhT14LkzvSTbfg2F74__oiET-t8ltA&key=AIzaSyA10sWJ6IOVGEIyHuygj8tIBDKr8RjDyEU"
            details = requests.post("https://maps.googleapis.com/maps/api/place/details/json?place_id="+object.my_favourites["place_id"]+"&key="+api_key)
            details = json.loads(details.text)
            details = details["result"]
            rating = object.my_favourites["rating"]
            if "opening_hours" in details:
                schedule = details["opening_hours"]
                isopen = schedule["open_now"]
                schedule = schedule["weekday_text"]
            else:
                schedule = ["No data"]
                isopen = "No data"
            if "reviews" in details:
                review = details["reviews"]
                review = review[0]
                map = "https://www.google.com/maps/embed/v1/place?q=place_id:"+object.my_favourites["place_id"]+"&key="+api_key
                return render(request, "coffee_finder/place.html",{"object":object.my_favourites,"details":details,"username":username,"location":location,"isopen":isopen,"photo":photo,"review":review,"schedule":schedule,"map":map})
            else:
                map = "https://www.google.com/maps/embed/v1/place?q=place_id:"+object.my_favourites["place_id"]+"&key="+api_key
                return render(request, "coffee_finder/place.html",{"object":object.my_favourites,"details":details,"username":username,"location":location,"isopen":isopen,"photo":photo,"review":"","schedule":schedule,"map":map})

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

def js_favourites_delete(request):
    pass

def js_favourites_handler(request):
    profile = Profile.objects.filter(user=request.user).get()
    if request.method == "GET":
        # handle right swipe
        if request.GET["direction"] == "right" :
            right = profile.places_set.all()[0]
            if len(profile.favourites_set.all())>0:
                for i in range (len(profile.favourites_set.all())):
                    if (ParsedCafeData(profile.places_set.all()[0].my_places))["name"] == (ParsedCafeData(profile.favourites_set.all()[i].my_favourites))["name"]:
                        right.delete()
                        data = json.dumps(ParsedCafeData(profile.places_set.all()[0].my_places))
                        return HttpResponse(data)
            Favourites.objects.create(profile=profile,my_favourites=right.my_places)
            right.delete()
            data = json.dumps(ParsedCafeData(profile.places_set.all()[0].my_places))
            return HttpResponse(data)
        # handle left swipe
        elif request.GET["direction"] == "left" :
            left = profile.places_set.all()[0]
            Rejected.objects.create(profile=profile,my_rejected=left.my_places)
            left.delete()
            data = json.dumps(ParsedCafeData(profile.places_set.all()[0].my_places))
            return HttpResponse(data)
        # handle middle
        else :
            return HttpResponse("Wybrałeś środek")

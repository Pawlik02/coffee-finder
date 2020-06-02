import requests
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Profile, Favourite

api_key = "AIzaSyA10sWJ6IOVGEIyHuygj8tIBDKr8RjDyEU"

def index(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse("coffee_finder:login"))
    response = requests.post("https://maps.googleapis.com/maps/api/place/textsearch/json?query=plac+ratajskiego&type=cafe&key="+api_key)
    response = json.loads(response.text)
    info = response["results"]
    info = info[0]
    formatted_address = info["formatted_address"]
    name = info["name"]
    if "photos" in info:
        photo = info["photos"]
        photo = photo[0]
        photo = photo["photo_reference"]
        photo = "https://maps.googleapis.com/maps/api/place/photo?maxheight=800&photoreference="+photo+"&key="+api_key
    else:
        photo = "https://maps.googleapis.com/maps/api/place/photo?maxheight=800&photoreference=CmRaAAAAZOkFJe830BVBm2Glk2rOxwMSnEtkR5PO1z1_VSMmxiPbdQkWLFzVXX9enkSdqECGHVDM4Qxt4bQIrfEajTi6NNsQVtwzskFXGT_pgxi6kH9sF8yr7JPQfJxSCW7H0xWQEhAVC39nIeFLkTiTxSaLoMydGhT14LkzvSTbfg2F74__oiET-t8ltA&key=AIzaSyA10sWJ6IOVGEIyHuygj8tIBDKr8RjDyEU"
    v_id = info["id"]
    isopen = info["opening_hours"]
    isopen = isopen["open_now"]
    # Do zapisywania ulubionych
    profile = Profile.objects.get()
    favourite = Favourite(profile=profile,my_favourite=response)
    profile.save()
    #Complete sheit
    # response = json.loads(response)
    # candidates = response["candidates"]
    # id = candidates[0]
    # id = id["place_id"]
    # response = requests.post("https://maps.googleapis.com/maps/api/place/details/json?place_id="+str(id)+"&key="+api_key)
    # name = response.text
    username = request.user
    location = Profile.objects.get()
    location = location.location
    if request.method == "POST":
        location = request.POST.get("location")
        user = request.user
        Profile.objects.update(user=user,location=location)
    # else:
    #     return render(request,"coffee_finder/index.html",{"name":name,"username":username,"location":location,"formatted_address":formatted_address,"photo":photo,"id":v_id})
    return render(request,"coffee_finder/index.html",{"name":name,"location":location,"username":username,"formatted_address":formatted_address,"photo":photo,"id":v_id,"isopen":isopen})

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
def parssing():
    response = requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json?query="+place_id+"&radius=50000&type=cafe&key="+api_key)
    res = json.loads(response.text)
    info = res["results"]
    info = info[0]
    formatted_address = info["formatted_address"]
    name = info["name"]
    photos = info["photo"]
    v_id = info["id"]

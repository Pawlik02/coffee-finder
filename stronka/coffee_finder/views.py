import requests
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Profile

api_key = "AIzaSyA10sWJ6IOVGEIyHuygj8tIBDKr8RjDyEU"

def index(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse("coffee_finder:login"))
    response = requests.post("https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=kahawa&inputtype=textquery&key="+api_key)
    response = response.text
    response = json.loads(response)
    candidates = response["candidates"]
    id = candidates[0]
    id = id["place_id"]
    response = requests.post("https://maps.googleapis.com/maps/api/place/details/json?place_id="+str(id)+"&key="+api_key)
    name = response.text
    if request.method == "POST":
        location = request.POST.get("location")
        user = request.user
        if Profile.objects.filter(user=user).exists():
            Profile.objects.update(user=user,location=location)
        else:
            data = Profile(user=user,location=location)
            data.save()
    else:
        return render(request,"coffee_finder/index.html",{"name":name})
    return render(request,"coffee_finder/index.html",{"name":name,"location":location})

# def test(request):
#     if request.method == "POST":
#         location = request.POST.get("location")
#         user = request.user
#         if Profile.objects.filter(user=user).exists():
#             Profile.objects.update(user=user,location=location)
#         else:
#             data = Profile(user=user,location=location)
#             data.save()
#     else:
#         return render(request,"coffee_finder/test.html")
#     return render(request,"coffee_finder/test.html",{"location":location})

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username,password=raw_password)
            login(request,user)
            return redirect("/coffee_finder")
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

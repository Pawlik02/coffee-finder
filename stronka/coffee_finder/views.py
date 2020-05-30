import requests
import json
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
import requests
import json

api_key = "AIzaSyA10sWJ6IOVGEIyHuygj8tIBDKr8RjDyEU"

api_key = "AIzaSyA10sWJ6IOVGEIyHuygj8tIBDKr8RjDyEU"

def index(request):
    response = requests.post("https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=kahawa&inputtype=textquery&key="+api_key)
    response = response.text
    response = json.loads(response)
    candidates = response["candidates"]
    id = candidates[0]
    id = id["place_id"]
    response = requests.post("https://maps.googleapis.com/maps/api/place/details/json?place_id="+str(id)+"&key="+api_key)
    name = response.text
    return render(request,"coffee_finder/index.html",{"name":name})

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
            return render(request, "coffee_finder/index.html")
        else:
            return HttpResponse("Wrong data")
    return render(request, "coffee_finder/login.html")

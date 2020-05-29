import request
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

api_key = "AIzaSyBF_3OJcvP2e1eP0lk0Q9Qyo6-MWI8yX3M"

def index(request):
    name = request.get("https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=kahawa&key="+api_key)
    return render(request,"coffee_finder/index.html")

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

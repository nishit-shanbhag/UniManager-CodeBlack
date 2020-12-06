import django
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect


# Create your views here.


def main(request):
    return render(request, "home.html", {})


def auth(request):
    return render(request,"userAuth.html",{})

def register(request):
    if request.method == "GET":
        raise Http404
    else:
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        if User.objects.filter(email=email).count()>0:
            return render(request,"userAuth.html",{"error":"Email already exists"})
        if User.objects.filter(username=username).count()>0:
            return render(request,"userAuth.html",{"error":"Username already exists"})
        user = User.objects.create_user(username=username,email=email,password=password)
        request.session['email'] = email
        request.session['username'] = username
        django.contrib.auth.login(request, user)
        authenticate(username=username, password=password)
        return render(request,"home.html",{})

def login(request):
    if request.method == "GET":
        raise Http404
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            django.contrib.auth.login(request, user)
            print("LOGGED IN",username)
            request.session['username'] = username
            return render(request,"home.html",{})
        else:
            print("ERROR - incorrect credentials", username)
            return render(request, "userAuth.html", {"error": "Incorrect credentials"})

def signout(request):
    logout(request)
    request.session.flush()
    return render(request,"home.html",{})
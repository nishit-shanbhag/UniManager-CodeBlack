import django
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
from .models import *

# Create your views here.


def home(request):
    return render(request, "home.html", {})


def auth(request):
    if request.user.is_authenticated:
        return redirect("/home")

    return render(request, "userAuth.html", {})


def register(request):
    if request.method == "GET":
        raise Http404
    else:
        email = request.POST.get("email")
        college_id = request.POST.get("college_id")
        password = request.POST.get("password")
        name = request.POST.get("name")
        if User.objects.filter(email=email).count() > 0:
            return render(request, "userAuth.html", {"error": "Email already exists"})
        if User.objects.filter(username=college_id).count() > 0:
            return render(request, "userAuth.html", {"error": "Username already exists"})
        user = User.objects.create_user(first_name=name, username=email, password=password)
        profile = Profile.objects.create(user = user, college_id = college_id)
        request.session['email'] = email
        request.session['name'] = name
        django.contrib.auth.login(request, user)
        authenticate(username=email, password=password)
        return redirect("/home")


def login(request):
    if request.method == "GET":
        raise Http404
    else:
        email = request.POST.get("login_email")
        password = request.POST.get("login_password")
        user = authenticate(username=email, password=password)
        if user is not None:
            django.contrib.auth.login(request, user)
            print("LOGGED IN", email)
            request.session['email'] = email
            # return render(request, "home.html", {})
            return redirect("/home")

        else:
            print("ERROR - incorrect credentials", email)
            return render(request, "userAuth.html", {"error": "Incorrect credentials"})


def signout(request):
    logout(request)
    request.session.flush()
    return render(request, "home.html", {})

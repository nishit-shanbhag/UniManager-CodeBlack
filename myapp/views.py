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
        profile = Profile.objects.create(user=user, college_id=college_id)
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
    return redirect("/")


# Send request.user
def add_lost_and_found_complain(user_ob, item_name, info):
    lost_and_found_ob = LostAndFound.objects.create(submit_user=user_ob, name=item_name, information=info)


def get_lost_and_found_complains(request):
    lost_and_found_obs = LostAndFound.objects.order_by("-submit_date").all()
    print(list(lost_and_found_obs.values()))
    return list(lost_and_found_obs.values())


def get_lost_and_found_by_id(request, id: int):
    lost_and_found_ob = LostAndFound.objects.filter(id=id)
    return list(lost_and_found_ob.values())


def change_lnf_status(id, status):
    LostAndFound.objects.filter(id=id).update(status=status)


def place_order(request):
    order_ob = Order.objects.create(submit_user=request.user, delivery_date=request.POST.get("delivery_date"))

    items = []
    for i in range(1, 10):
        item = int(request.POST.get(str(i)))
        if int(item) > 0:
            items.append([i, item])
            Order_items.objects.create(order_ob, Menu.objects.filter(id=i))

    total_cost = 0
    items_ob = Menu.objects.all().values()
    for item in items:
        total_cost += items_ob[item[0] + 1]["price"] * item[1]

    order_ob.update(total_cost=total_cost)

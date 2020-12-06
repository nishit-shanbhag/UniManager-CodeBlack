import django
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import Http404
from django.shortcuts import render, redirect

from .models import *


# Create your views here.


def home(request):
    return render(request, "home.html",
                  {"user_type": request.session.get("user_type"), "name": request.session['name'].split()[0]})


def auth(request):
    if request.user.is_authenticated:
        return redirect("/home")

    return render(request, "userAuth.html")


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
            request.session['name'] = user.first_name
            user_type = Profile.objects.filter(user=request.user).first().type
            request.session["user_type"] = user_type
            return redirect("/home")

        else:
            print("ERROR - incorrect credentials", email)
            return render(request, "userAuth.html", {"error": "Incorrect credentials"})


def signout(request):
    logout(request)
    request.session.flush()
    return redirect("/")


def canteen_admin(request):
    return render(request, "canteen_admin.html", {"name": request.session['name'].split()[0]})


def canteen_user(request):
    orders = list(Order.objects.filter(submit_user=request.user).order_by("-delivery_date").values())

    for order in range(len(orders)):
        itemob = list(Order_items.objects.filter(order_id=orders[order]["id"]).values())
        orders[order]["delivery_date"] = orders[order]["delivery_date"].strftime('%H:%M:%S %d/%m/%Y')
        food_items = []
        for item in itemob:
            menu_item = Menu.objects.filter(id=item["item_id_id"]).first()

            food_items.append([str(item["quantity"]) + " x " + menu_item.name])

        orders[order]["items"] = food_items
    print(orders)
    return render(request, "canteen_user.html", {"name": request.session['name'].split()[0], "orders": orders})


def complaints_admin(request):
    return render(request, "complaints_admin.html", {"name": request.session['name'].split()[0]})


def complaints_user(request):
    if request.method == "POST":
        print(request.POST)
        if request.FILES.get('myimage', False):
            myfile = request.FILES["myimage"]
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)

            Complaint.objects.create(location=request.POST.get("location"), info=request.POST.get("message"),
                                     photo=uploaded_file_url, submit_user=request.user,
                                     category=request.POST.get("category"))
        else:
            Complaint.objects.create(location=request.POST.get("location"), info=request.POST.get("message"),
                                     submit_user=request.user, category=request.POST.get("category"))

        return render(request, "complaints_user.html", {"name": request.session['name'].split()[0]})
    else:
        return render(request, "complaints_user.html", {"name": request.session['name'].split()[0]})


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

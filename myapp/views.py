import json
from datetime import datetime

import django
from dateutil import tz
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import Http404, HttpResponse
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
        request.session["user_type"] = 0
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
    orders = list(Order.objects.filter(status=0).order_by("-delivery_date").values())
    for order in range(len(orders)):
        itemob = list(Order_items.objects.filter(order_id=orders[order]["id"]).values())
        orders[order]["delivery_date"] = orders[order]["delivery_date"].strftime('%H:%M:%S %d/%m/%Y')
        orders[order]["order_date"] = orders[order]["order_date"].strftime('%H:%M:%S %d/%m/%Y')
        orders[order]["user_name"] = User.objects.filter(id=orders[order]["submit_user_id"]).first().first_name
        food_items = []
        for item in itemob:
            menu_item = Menu.objects.filter(id=item["item_id_id"]).first()

            food_items.append([str(item["quantity"]) + " x " + menu_item.name])

        orders[order]["items"] = food_items

    return render(request, "canteen_admin.html", {"name": request.session['name'].split()[0], "orders": orders})


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
    return render(request, "canteen_user.html", {"name": request.session['name'].split()[0], "orders": orders})


def complaints_admin(request):
    complaints = list(Complaint.objects.filter(status=0).order_by("requested_date").values())
    print(complaints)

    for complaint in range(len(complaints)):
        complaints[complaint]["submit_user_id"] = User.objects.filter(
            id=complaints[complaint]["submit_user_id"]).first().first_name
        complaints[complaint]["requested_date"] = complaints[complaint]["requested_date"].strftime('%H:%M:%S %d/%m/%Y')
    return render(request, "complaints_admin.html",
                  {"name": request.session['name'].split()[0], "complaints": complaints})


def complaints_user(request):
    if request.method == "POST":
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


def lost_and_found(request):
    l_and_f = list(LostAndFound.objects.filter(status=0).order_by("-submit_date").values())

    for lf in range(len(l_and_f)):
        l_and_f[lf]["submit_date"] = l_and_f[lf]["submit_date"].strftime('%H:%M:%S %d/%m/%Y')

    return render(request, "lostfound_user.html",
                  {"name": request.session['name'].split()[0], "lost_and_found": l_and_f})


def lost_and_found_report(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        LostAndFound.objects.create(name=name, information=description, submit_user=request.user)
        return redirect("/home/lost-and-found")
    else:
        return render(request, "lostfound_user_report.html",
                      {"name": request.session['name'].split()[0]})


def lost_and_found_admin(request):
    l_and_f = list(LostAndFound.objects.filter(status=0).order_by("-submit_date").values())
    for lf in range(len(l_and_f)):
        l_and_f[lf]["submit_date"] = l_and_f[lf]["submit_date"].strftime('%H:%M:%S %d/%m/%Y')
    return render(request, "lostfound_admin.html",
                  {"name": request.session['name'].split()[0], "lost_and_found": l_and_f})


def lost_and_found_admin_info(request, id):
    if request.method == "POST":
        name = request.POST.get("name1")
        description = request.POST.get("description1")
        delivery_date = request.POST.get("delivery_date")
        upload_email = request.POST.get("upload_email")
        # takeaway_date = request.POST.get("takeaway_date")
        takeaway_email = request.POST.get("takeaway_email")

        if takeaway_email != "":
            LostAndFound.objects.filter(id=id).update(name=name, information=description, submit_date=delivery_date,
                                                      submit_user=User.objects.filter(username=upload_email).first(),
                                                      takeaway_user=User.objects.filter(
                                                          username=takeaway_email).first(), takeaway_date=datetime.now(),
                                                      status=1)
        else:
            LostAndFound.objects.filter(id=id).update(name=name, information=description, submit_date=delivery_date,
                                                      submit_user_id=User.objects.filter(username=upload_email).first())

        return redirect("/home/lost-and-found-admin")
    else:

        l_and_f = list(LostAndFound.objects.filter(id=id).values())[0]
        print(l_and_f)

        IST = tz.gettz('Asia/Kolkata')
        t = l_and_f["submit_date"].replace(tzinfo=IST)
        print(t)

        l_and_f["submit_date"] = l_and_f["submit_date"].strftime("%Y-%m-%dT%H:%M:%S")
        l_and_f["user_name"] = User.objects.filter(id=l_and_f["submit_user_id"]).first().first_name
        l_and_f["email"] = User.objects.filter(id=l_and_f["submit_user_id"]).first().username

        return render(request, "lostfound_admin_info.html",
                      {"name": request.session['name'].split()[0], "l_and_f": l_and_f})


# Send request.user
def add_lost_and_found_complain(user_ob, item_name, info):
    lost_and_found_ob = LostAndFound.objects.create(submit_user=user_ob, name=item_name, information=info)


def get_lost_and_found_complains(request):
    lost_and_found_obs = LostAndFound.objects.order_by("-submit_date").all()
    return list(lost_and_found_obs.values())


def get_lost_and_found_by_id(request, id: int):
    lost_and_found_ob = LostAndFound.objects.filter(id=id)
    return list(lost_and_found_ob.values())


def change_lnf_status(id, status):
    LostAndFound.objects.filter(id=id).update(status=status)


def place_order(request):
    order_ob = Order.objects.create(submit_user=request.user, delivery_date=request.POST.get("delivery_date"))

    items = []
    for i in range(1, 9):
        item = int(request.POST.get(str(i)))
        if int(item) > 0:
            items.append([i, item])
            Order_items.objects.create(order_ob, Menu.objects.filter(id=i))

    total_cost = 0
    items_ob = Menu.objects.all().values()
    for item in items:
        total_cost += items_ob[item[0] + 1]["price"] * item[1]

    order_ob.update(total_cost=total_cost)


def canteen_user_order(request):
    if request.POST:
        order_ob = Order.objects.create(submit_user=request.user,
                                        delivery_date=datetime.strptime(request.POST.get("delivery_date"),
                                                                        "%Y-%m-%dT%H:%M:%S"))

        items = []
        for i in range(1, 9):
            item = int(request.POST.get(str(i)))
            if int(item) > 0:
                items.append([i, item])
                Order_items.objects.create(order_id=order_ob, item_id=Menu.objects.filter(id=i).first(), quantity=item)

        total_cost = 0
        items_ob = Menu.objects.all().values()
        for item in items:
            total_cost += items_ob[item[0] - 1]["price"] * item[1]

        Order.objects.filter(id=order_ob.id).update(total_cost=total_cost)
        return redirect("/home/canteen")
    else:
        menu_items = list(Menu.objects.all().values())
        return render(request, "canteen_user_order.html", {"menu_items": menu_items})


def canteen_admin_status_change(request):
    id = request.POST.get("id")
    category = request.POST.get("category")

    if category == "Completed":
        Order.objects.filter(id=id).update(status=1)
    elif category == "Cancelled":
        Order.objects.filter(id=id).update(status=2)
    return HttpResponse(json.dumps({}))


def complaint_admin_status_change(request):
    id = request.POST.get("id")
    status = request.POST.get("status")

    if status == "Resolved":
        Complaint.objects.filter(id=id).update(status=1)
    elif status == "Rejected":
        Complaint.objects.filter(id=id).update(status=2)
    return HttpResponse(json.dumps({}))

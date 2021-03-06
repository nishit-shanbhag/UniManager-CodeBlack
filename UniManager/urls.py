"""UniManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth, name="auth"),
    path('register', register, name="register"),
    path('login', login, name="login"),
    path('logout', signout, name='logout'),
    path('home/', home, name='home'),

    path("home/lost-and-found", lost_and_found, name="lost-and-found"),
    path("home/lost-and-found/report", lost_and_found_report, name="lost_and_found_report"),
    path("home/complaints", complaints_user, name="complaints"),
    path("home/canteen", canteen_user, name="canteen"),
    path("home/canteen/new", canteen_user_order, name="canteen"),
    path("home/lost-and-found-admin", lost_and_found_admin, name="lost-and-found-admin"),
    path("home/lost-and-found-admin/<int:id>", lost_and_found_admin_info, name="lost-and-found-admin-info"),
    path("home/complaints-admin", complaints_admin, name="complaints-admin"),
    path("home/canteen-admin", canteen_admin, name="canteen-admin"),
    path("home/canteen-admin-stats", canteen_admin_statistics, name="canteen-admin-stats"),
    path("canteen_admin_status_change", canteen_admin_status_change, name="canteen_admin_status_change"),
    path("complaint_admin_status_change", complaint_admin_status_change, name="complaint_admin_status_change"),
    path("home/events", event_user, name="event_user"),
    path("home/events-admin", event_admin, name="event_admin"),
    # path("temp/", get_lost_and_found_complains, name="temp"),
    # path("temp/<int:id>", get_lost_and_found_by_id, name="temp")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

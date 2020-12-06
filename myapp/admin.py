from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Profile)
admin.site.register(LostAndFound)
admin.site.register(Complaint)
admin.site.register(Order)
admin.site.register(Menu)
admin.site.register(Order_items)
admin.site.register(Event)

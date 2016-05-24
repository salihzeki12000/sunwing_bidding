from django.contrib import admin

# Register your models here.
from .models import Pilot, SeniorityList

admin.site.register(Pilot)
admin.site.register(SeniorityList)

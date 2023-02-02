from django.contrib import admin

# Register your models here.
from .models import Userlogin, Complains

admin.site.register(Userlogin)
admin.site.register(Complains)

from unittest import addModuleCleanup

from django.contrib import admin

# from .models.user import DealershipUser
from .models.car import Car

# Register your models here.
admin.site.register(Car)
# admin.site.register(DealershipUser)

from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'phone_number', 'name')


@admin.register(Reservation)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', )


@admin.register(Wash)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(Service)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', )


@admin.register(ServiceType)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(Slot)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', )

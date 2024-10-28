from django.contrib import admin
from restaurant.models import Table, Booking

"""Вывод списка столов и бронирований"""


@admin.register(Table)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'description', 'seats')
    search_fields = ('number', 'seats',)


@admin.register(Booking)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'time', 'owner', 'table')
    list_filter = ('time', 'table',)

from django.contrib import admin
from restaurant.models import Table, Booking

"""Вывод списка столов и бронирований"""


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'description', 'seats')
    search_fields = ('number', 'seats',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'datetime_booking', 'owner', 'table')
    list_filter = ('datetime_booking', 'table',)

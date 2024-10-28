from django.core.cache import cache

from restaurant.models import Booking
from config.settings import CACHE_ENABLED


def get_bookings_from_cache():
    """Метод получения кешированной инфы по товарам"""
    if not CACHE_ENABLED:
        return Booking.objects.all()
    key = "bookings_list"
    bookings = cache.get(key)
    # Если бронирование есть в кеше, то метод его вернет, а если нет - то сходит в БД и вернет
    if bookings is not None:
        return bookings
    bookings = Booking.objects.all()
    cache.set(key, bookings)
    return bookings

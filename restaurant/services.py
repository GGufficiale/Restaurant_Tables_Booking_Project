from django.conf import settings
from django.core.cache import cache

from restaurant.models import Product
from config.settings import CACHE_ENABLED


def get_products_from_cache():
    """Метод получения кешированной инфы по товарам"""
    if not CACHE_ENABLED:
        return Product.objects.all()
    key = "products_list"
    products = cache.get(key)
    # Если товар есть в кеше, то метод его вернет, а если нет - то сходит в БД и вернет
    if products is not None:
        return products
    products = Product.objects.all()
    cache.set(key, products)
    return products
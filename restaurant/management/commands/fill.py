# Специальный файл для создания кастомных команд.
# Создается по адресу myapp/management/commands/fill.py
import json
from django.core.management import BaseCommand
from restaurant.models import Category, Product


class Command(BaseCommand):
    @staticmethod
    def json_read_categories():
        """Получение данных из фикстур с категориями"""
        with open("restaurant.json", encoding='utf-8') as file:
            data = json.load(file)
        return [i for i in data if i['model'] == 'restaurant.category']

    @staticmethod
    def json_read_products():
        """Получение данных из фикстур с продуктами"""
        with open("restaurant.json", encoding='utf-8') as file:
            data = json.load(file)
        return [i for i in data if i['model'] == 'restaurant.product']

    def handle(self, *args, **options):
        """Удаление всех продуктов и категорий"""
        Product.objects.all().delete()
        Category.objects.all().delete()

        """Создание списков для хранения объектов"""
        product_for_create = []
        category_for_create = []

        """Обход всех значений категорий из фикстуры для получения информации об одном объекте"""
        for category in Command.json_read_categories():
            category_for_create.append(
                Category(id=category['pk'],
                         name=category["fields"]["name"],
                         description=category["fields"]["description"])
            )

        """Создание объектов в базе"""
        Category.objects.bulk_create(category_for_create)

        """Обход всех значений продуктов из фикстуры для получения информации об одном объекте"""
        for product in Command.json_read_products():
            product_for_create.append(
                Product(id=product['pk'],
                        name=product["fields"]["name"],
                        description=product["fields"]["description"],
                        category=Category.objects.get(pk=product["fields"]["category"]),
                        price=product["fields"]["price"])
            )

        """Создание объектов в базе"""
        Product.objects.bulk_create(product_for_create)

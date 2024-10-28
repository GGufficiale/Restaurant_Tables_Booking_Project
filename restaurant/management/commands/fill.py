# Специальный файл для создания кастомных команд.
# Создается по адресу myapp/management/commands/fill.py
import json
from django.core.management import BaseCommand
from restaurant.models import Table, Booking


class Command(BaseCommand):
    @staticmethod
    def json_read_tables():
        """Получение данных из фикстур со столами"""
        with open("restaurant.json", encoding='utf-8') as file:
            data = json.load(file)
        return [i for i in data if i['model'] == 'restaurant.table']

    @staticmethod
    def json_read_bookings():
        """Получение данных из фикстур с бронированиями"""
        with open("restaurant.json", encoding='utf-8') as file:
            data = json.load(file)
        return [i for i in data if i['model'] == 'restaurant.booking']

    def handle(self, *args, **options):
        """Удаление всех столов и бронирований"""
        Table.objects.all().delete()
        Booking.objects.all().delete()

        """Создание списков для хранения объектов"""
        table_for_create = []
        booking_for_create = []

        """Обход всех значений категорий из фикстуры для получения информации об одном объекте"""
        for table in Command.json_read_tables():
            table_for_create.append(
                Table(id=table['pk'],
                      number=table["fields"]["number"],
                      description=table["fields"]["description"])
            )

        """Создание объектов в базе"""
        Table.objects.bulk_create(table_for_create)

        """Обход всех значений продуктов из фикстуры для получения информации об одном объекте"""
        for booking in Command.json_read_bookings():
            booking_for_create.append(
                Booking(id=booking['pk'],
                        name=booking["fields"]["name"],
                        description=booking["fields"]["description"],
                        table=Booking.objects.get(pk=booking["fields"]["table"]),
                        time=booking["fields"]["time"])
            )

        """Создание объектов в базе"""
        Booking.objects.bulk_create(booking_for_create)

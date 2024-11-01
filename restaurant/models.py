from django.db import models

from users.models import User

"""Создание модели для БД с объектами каталога"""
NULLABLE = {'blank': True, 'null': True}  # форма, если параметр необязателен


class Table(models.Model):
    number = models.IntegerField(verbose_name='№ стола', help_text='Укажите № стола')
    description = models.CharField(max_length=1000, verbose_name='Описание стола', help_text='Укажите тип стола',
                                   **NULLABLE)
    seats = models.IntegerField(verbose_name='К-во мест', help_text='Укажите к-во мест', **NULLABLE)

    def __str__(self):
        return f'{self.number}: {self.description}, {self.seats}'

    class Meta:
        verbose_name = 'стол'
        verbose_name_plural = 'столы'
        ordering = ['number', 'description', 'seats']


class Booking(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя гостя', help_text="Введите имя или имэйл")
    description = models.CharField(max_length=1000, verbose_name='Пожелания',
                                   help_text="Введите пожелания при бронировании",
                                   **NULLABLE)
    datetime_booking = models.DateTimeField(max_length=25, verbose_name='Дата и время брони', **NULLABLE)
    photo = models.ImageField(upload_to='catalog/photo', verbose_name="Фото",
                              help_text="Загрузите скрин из ваших соцсетей для получения скидки", **NULLABLE)
    # Для работы с изображениями в Джанго надо установить пакет Pillow"""
    owner = models.ForeignKey(User, verbose_name='Юзер', help_text='Укажите создателя бронирования', **NULLABLE,
                              on_delete=models.SET_NULL)
    table = models.ForeignKey(Table, verbose_name='Стол', help_text='Укажите № стола', **NULLABLE,
                              on_delete=models.SET_NULL)
    is_active = models.BooleanField(verbose_name='Активность брони', editable=False, **NULLABLE,
                                    default=False)

    def __str__(self):
        print(f'{self.name}: {self.description}. Время:{self.datetime_booking}. Стол: {self.table}')
        return f'{self.name}: {self.description}. Время:{self.datetime_booking}. Стол: {self.table}'

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ['name', 'description', 'datetime_booking', 'table']
        # Поля для функционала прав доступа - варианты редактирования
        # permissions = [
        #     ('cancel_publication', 'Can cancel publication'),
        #     ('edit_description', 'Can edit description'),
        #     ('change_category', 'Can change category'),
        # ]

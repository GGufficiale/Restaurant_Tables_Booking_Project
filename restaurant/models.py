from django.db import models

from users.models import User

"""Создание модели для БД с объектами каталога"""
NULLABLE = {'blank': True, 'null': True}  # форма, если параметр необязателен


class Booking(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя гостя', help_text="Введите имя или имэйл")
    description = models.CharField(max_length=1000, verbose_name='Пожелания',
                                   help_text="Введите пожелания при бронировании",
                                   **NULLABLE)
    time = models.TimeField(max_length=25, verbose_name='Время брони')
    photo = models.ImageField(upload_to='catalog/photo', verbose_name="Фото",
                              help_text="Загрузите скрин из ваших соцсетей для получения скидки", **NULLABLE)
    # Для работы с изображениями в Джанго надо установить пакет Pillow"""
    created_at = models.DateField(**NULLABLE, verbose_name='дата создания брони в БД', auto_now_add=True)
    updated_at = models.DateField(**NULLABLE, verbose_name='дата последнего изменения брони в БД', auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    slug = models.CharField(max_length=150, verbose_name='slug', null=True, blank=True)
    owner = models.ForeignKey(User, verbose_name='владелец товара', help_text='Укажите владельца товара', **NULLABLE,
                              on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.name}: {self.description}. Цена: {self.price}'

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ['name', 'description', 'price']
        # Поля для функционала прав доступа - варианты редактирования
        permissions = [
            ('cancel_publication', 'Can cancel publication'),
            ('edit_description', 'Can edit description'),
            ('change_category', 'Can change category'),
        ]


class Table(models.Model):
    number = models.IntegerField(max_length=100, verbose_name='№ стола')
    description = models.CharField(max_length=1000, verbose_name='описание стола', **NULLABLE)
    owner = models.ForeignKey(User, verbose_name='гость, забронировавший стол',
                              help_text='Укажите гостя, забронировавшего стол', **NULLABLE,
                              on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.number}: {self.description}, {self.owner}'

    class Meta:
        verbose_name = 'стол'
        verbose_name_plural = 'столы'
        ordering = ['name', 'description', 'owner']

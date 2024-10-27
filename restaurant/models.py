from django.db import models

from users.models import User

"""Создание модели для БД с объектами каталога"""
NULLABLE = {'blank': True, 'null': True}  # форма, если параметр необязателен


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')
    description = models.CharField(max_length=1000, verbose_name='описание')

    # Сразу после внесения изменений в модель создаем миграцию"""
    def __str__(self):
        return f'{self.name}: {self.description}'

    class Meta:
        verbose_name = 'штука'
        verbose_name_plural = 'штуки'
        ordering = ['name', 'description']


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')
    description = models.CharField(max_length=1000, verbose_name='описание', help_text="Введите описание товара",
                                   **NULLABLE)
    photo = models.ImageField(upload_to='catalog/photo', verbose_name="фото товара", **NULLABLE)
    # Для работы с изображениями в Джанго надо не забыть установить пакет Pillow"""
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, verbose_name='категория', **NULLABLE,
                                 related_name="product")
    # При связи продукта и категории (ForeignKey) не забыть добавить 'to'."""
    price = models.IntegerField(verbose_name='цена')
    created_at = models.DateField(**NULLABLE, verbose_name='дата создания записи в БД', auto_now_add=True)
    updated_at = models.DateField(**NULLABLE, verbose_name='дата последнего изменения записи в БД', auto_now=True)
    manufactured_at = models.DateField(**NULLABLE, verbose_name='дата производства продукта')
    views_counter = models.PositiveIntegerField(verbose_name='Счетчик просмотров', help_text='Укажите к-во просмотров',
                                                default=0)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    slug = models.CharField(max_length=150, verbose_name='slug', null=True, blank=True)
    owner = models.ForeignKey(User, verbose_name='владелец товара', help_text='Укажите владельца товара', **NULLABLE,
                              on_delete=models.SET_NULL)

    # Поле owner указывает на владельца прав доступа к товару и является ссылкой на модель пользователя
    # Сразу после внесения изменений в модель создаем миграцию

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


class Version(models.Model):
    product = models.ForeignKey(Product, related_name='versions', on_delete=models.SET_NULL, **NULLABLE,
                                verbose_name='товар')
    version_number = models.PositiveIntegerField(verbose_name='№ версии товара', default=0, **NULLABLE)
    version_name = models.CharField(max_length=100, verbose_name="Название", help_text='Введите название')
    current_version_sign = models.BooleanField(default=True, verbose_name='Текущая версия')

    class Meta:
        verbose_name = 'Версия товара'
        verbose_name_plural = 'Версии товара'
        ordering = ['product', 'version_number', 'version_name']

    def __str__(self):
        return self.version_name

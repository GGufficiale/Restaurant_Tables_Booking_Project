# Generated by Django 5.1.2 on 2024-10-28 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите имя или имэйл', max_length=100, verbose_name='Имя гостя')),
                ('description', models.CharField(blank=True, help_text='Введите пожелания при бронировании', max_length=1000, null=True, verbose_name='Пожелания')),
                ('time', models.TimeField(max_length=25, verbose_name='Дата и время брони')),
                ('photo', models.ImageField(blank=True, help_text='Загрузите скрин из ваших соцсетей для получения скидки', null=True, upload_to='catalog/photo', verbose_name='Фото')),
                ('slug', models.CharField(blank=True, max_length=150, null=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Бронирование',
                'verbose_name_plural': 'Бронирования',
                'ordering': ['name', 'description', 'time', 'table'],
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(help_text='Укажите № стола', max_length=100, verbose_name='№ стола')),
                ('description', models.CharField(blank=True, help_text='Укажите тип стола', max_length=1000, null=True, verbose_name='Описание стола')),
                ('seats', models.IntegerField(blank=True, help_text='Укажите к-во мест', max_length=20, null=True, verbose_name='К-во мест')),
            ],
            options={
                'verbose_name': 'стол',
                'verbose_name_plural': 'столы',
                'ordering': ['number', 'description', 'seats'],
            },
        ),
    ]
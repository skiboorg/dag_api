# Generated by Django 4.2.4 on 2023-08-31 08:48

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Отображать?')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='Город')),
                ('days', models.CharField(blank=True, max_length=255, null=True, verbose_name='Дней')),
                ('price', models.CharField(blank=True, max_length=255, null=True, verbose_name='Стоимость')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Название')),
                ('slug', models.CharField(blank=True, help_text='Если не заполнено, создается на основе поля Назавание', max_length=255, null=True, verbose_name='ЧПУ')),
                ('short_description', models.TextField(blank=True, null=True, verbose_name='Короткое описание')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Описание')),
                ('tour_include', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Что включено в тур')),
                ('tour_route', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='WEBP', keep_meta=True, null=True, quality=95, scale=None, size=[790, 480], upload_to='product/gallery')),
            ],
            options={
                'verbose_name': 'Тур',
                'verbose_name_plural': 'Туры',
            },
        ),
        migrations.CreateModel(
            name='TourCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Название')),
                ('slug', models.CharField(blank=True, help_text='Если не заполнено, создается на основе поля Назавание', max_length=255, null=True, verbose_name='ЧПУ')),
            ],
            options={
                'verbose_name': 'Категория тура',
                'verbose_name_plural': 'Категории туров',
            },
        ),
        migrations.CreateModel(
            name='TourGalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', django_resized.forms.ResizedImageField(crop=None, force_format='WEBP', keep_meta=True, null=True, quality=95, scale=None, size=[840, 580], upload_to='product/gallery')),
                ('imageThumb', models.ImageField(blank=True, editable=False, null=True, upload_to='product/gallery/')),
                ('is_main', models.BooleanField(default=False, verbose_name='Основная картинка')),
                ('tour', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gallery', to='data.tour')),
            ],
            options={
                'verbose_name': 'Картинка товара',
                'verbose_name_plural': 'Картинки товаров',
                'ordering': ('is_main',),
            },
        ),
        migrations.CreateModel(
            name='TourFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.ImageField(blank=True, null=True, upload_to='product/gallery/')),
                ('text', models.CharField(max_length=255, null=True, verbose_name='Текст')),
                ('tour', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='features', to='data.tour')),
            ],
            options={
                'verbose_name': 'Элемент в описание тура',
                'verbose_name_plural': 'Элементы в описание тура',
            },
        ),
        migrations.CreateModel(
            name='TourDayPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=255, null=True, verbose_name='День')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Описание')),
                ('tour', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='day_plans', to='data.tour')),
            ],
            options={
                'verbose_name': 'План на день',
                'verbose_name_plural': 'Планы на дни',
            },
        ),
        migrations.AddField(
            model_name='tour',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tours', to='data.tourcategory'),
        ),
        migrations.CreateModel(
            name='NearestTour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, null=True, verbose_name='Текст')),
                ('tour', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nearest_days', to='data.tour')),
            ],
            options={
                'verbose_name': 'Ближайшая дата тура',
                'verbose_name_plural': 'Ближайшие даты тура',
            },
        ),
    ]

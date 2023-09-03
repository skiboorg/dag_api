from django.db import models
from django_resized import ResizedImageField
from pytils.translit import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.files import File


class TourCategory(models.Model):
    name = models.CharField('Название', max_length=255, blank=False, null=True)

    slug = models.CharField('ЧПУ', max_length=255,
                            help_text='Если не заполнено, создается на основе поля Назавание',
                            blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        #ordering = ('order_num',)
        verbose_name = 'Категория тура'
        verbose_name_plural = 'Категории туров'

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Tour(models.Model):
    is_active = models.BooleanField('Отображать?', default=True)
    city = models.CharField('Город', max_length=255, blank=True, null=True)
    days = models.CharField('Дней', max_length=255, blank=True, null=True)
    price = models.CharField('Стоимость', max_length=255, blank=True, null=True)
    name = models.CharField('Название', max_length=255, blank=False, null=True)

    slug = models.CharField('ЧПУ',max_length=255,
                                 help_text='Если не заполнено, создается на основе поля Назавание',
                                 blank=True, null=True)

    category = models.ForeignKey(TourCategory, blank=True, null=True, on_delete=models.SET_NULL, related_name='tours')
    short_description = models.TextField('Короткое описание', blank=True, null=True)
    description = RichTextUploadingField('Описание', blank=True, null=True)
    tour_include = RichTextUploadingField('Что включено в тур', blank=True, null=True)
    tour_route = ResizedImageField(size=[790, 480], quality=95, force_format='WEBP', upload_to='product/gallery',
                              blank=True, null=True)



    def __str__(self):
        return f'{self.name}'

    class Meta:
        #ordering = ('order_num',)
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class TourFeature(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, null=True, blank=False,
                                related_name='features')

    icon = models.ImageField(upload_to='product/gallery/', blank=True, null=True)
    text = models.CharField('Текст', max_length=255, blank=False, null=True)

    def __str__(self):
        return f'{self.text}'


    class Meta:
        #ordering = ('is_main',)
        verbose_name = 'Элемент в описание тура'
        verbose_name_plural = 'Элементы в описание тура'


class NearestTour(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, null=True, blank=False,
                             related_name='nearest_days')
    text = models.CharField('Текст', max_length=255, blank=False, null=True)

    def __str__(self):
        return f'{self.text}'

    class Meta:
        #ordering = ('is_main',)
        verbose_name = 'Ближайшая дата тура'
        verbose_name_plural = 'Ближайшие даты тура'

class TourDayPlan(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, null=True, blank=False,
                             related_name='day_plans')
    day = models.CharField('День', max_length=255, blank=False, null=True)
    description = RichTextUploadingField('Описание', blank=True, null=True)
    def __str__(self):
        return f'{self.day}'

    class Meta:
        #ordering = ('is_main',)
        verbose_name = 'План на день'
        verbose_name_plural = 'Планы на дни'


class TourGalleryImage(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, null=True, blank=False,
                                related_name='gallery')
    image = ResizedImageField(size=[840, 580], quality=95, force_format='WEBP', upload_to='product/gallery',
                              blank=False, null=True)
    imageThumb = models.ImageField(upload_to='product/gallery/', blank=True, null=True, editable=False)
    is_main = models.BooleanField('Основная картинка', default=False)

    def __str__(self):
        return f''

    def save(self, *args, **kwargs):
        from .services import create_thumb
        if not self.imageThumb:
            self.imageThumb.save(f'{self.tour.slug}-thumb.jpg', File(create_thumb(self.image)), save=False)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('is_main',)
        verbose_name = 'Картинка галерей'
        verbose_name_plural = 'Картинки галерей'


class CallbackForm(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, null=True, blank=False)
    days = models.CharField(max_length=255,blank=True, null=True)
    phone = models.CharField(max_length=255,blank=True, null=True)
    peoples = models.CharField(max_length=255,blank=True, null=True)
    name = models.CharField(max_length=255,blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'От {self.name} {self.phone} Дата создания: {self.created_at}'

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Форма обратной связи'
        verbose_name_plural = 'Формы обратной связи'


class Feedback(models.Model):
    avatar = ResizedImageField(size=[100, 100], quality=95, force_format='WEBP', upload_to='ava/',
                              blank=False, null=True)
    text = RichTextUploadingField(max_length=255,blank=True, null=True)
    name = models.CharField(max_length=255,blank=True, null=True)
    tour = models.CharField(max_length=255,blank=True, null=True)

    def __str__(self):
        return f'От {self.name}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'



class FeedbackImage(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, null=True, blank=False,
                                related_name='images')
    image = ResizedImageField(size=[120, 200], quality=95, force_format='WEBP', upload_to='fb/gallery',
                              blank=False, null=True)

    def __str__(self):
        return f''


    class Meta:
        verbose_name = 'Картинка отзыва'
        verbose_name_plural = 'Картинки отзывов'
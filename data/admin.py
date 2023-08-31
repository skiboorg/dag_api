from django.contrib import admin
from django.utils.safestring import mark_safe
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from .models import *




class TourFeatureInline(NestedStackedInline):
    model = TourFeature
    extra = 0

class NearestTourInline(NestedStackedInline):
    model = NearestTour
    extra = 0

class TourDayPlanInline(NestedStackedInline):
    model = TourDayPlan
    extra = 0
class TourGalleryImageImageInline(NestedStackedInline):
    model = TourGalleryImage
    extra = 0
    readonly_fields = ['image_preview']

    def image_preview(self, obj):

        if obj.image:
            return mark_safe(
                '<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(obj.image.url))
        else:
            return 'Нет изображения'

    image_preview.short_description = 'Текущее изображение'


class TourAdmin(NestedModelAdmin):
    model = Tour
    list_display = ('image_preview','name',)
    readonly_fields = ['image_preview']
    inlines = [TourGalleryImageImageInline, TourFeatureInline,NearestTourInline,TourDayPlanInline]
    fields = [
        'category',
        'image_preview',
        'is_active',
        'city',
        'days',
        'price',
        'name',
        'slug',
        'short_description',
        'description',
        'tour_include',
        'tour_route',
    ]
    def image_preview(self, obj):
        if obj.gallery.all().filter(is_main=True):
            return mark_safe(
                '<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(obj.gallery.all().filter(is_main=True).first().image.url))
        else:
            return 'Нет изображения'

    image_preview.short_description = 'Текущее изображение'


admin.site.register(Tour, TourAdmin)
admin.site.register(TourCategory)
admin.site.register(CallbackForm)
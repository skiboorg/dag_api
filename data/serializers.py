
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction

from rest_framework import exceptions, serializers, status, generics

import settings
from .models import *

class TourGalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourGalleryImage
        fields = '__all__'

class FeedbackImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackImage
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    images = FeedbackImageSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Feedback
        fields = '__all__'

class TourDayPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourDayPlan
        fields = '__all__'


class TourFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourFeature
        fields = '__all__'

class NearestToureSerializer(serializers.ModelSerializer):
    class Meta:
        model = NearestTour
        fields = '__all__'

class TourSerializer(serializers.ModelSerializer):
    gallery = TourGalleryImageSerializer(many=True, required=False, read_only=True)
    nearest_days = NearestToureSerializer(many=True, required=False, read_only=True)
    day_plans = TourDayPlanSerializer(many=True, required=False, read_only=True)
    features = TourFeatureSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Tour
        fields = '__all__'


class TourShortSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Tour
        fields = [
            'image',
            'name',
            'slug',
            'city',
            'short_description',
            'price',
            'days'
        ]

    def get_image(self, obj):
        if obj.gallery.all().filter(is_main=True):
            return f'{settings.SITE_URL}{obj.gallery.all().filter(is_main=True).first().image.url}'
        else:
            return f'{settings.SITE_URL}{obj.gallery.all().first().image.url}'




class TourCategorySerializer(serializers.ModelSerializer):
    tours = TourShortSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = TourCategory
        fields = '__all__'


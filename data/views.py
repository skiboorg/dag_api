from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models.functions import ExtractYear
from .serializers import *
from rest_framework import generics
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404
import django_filters

import shutil
from django.conf import settings



class GetCategories(generics.ListAPIView):
    serializer_class = TourCategorySerializer
    queryset = TourCategory.objects.all()

class GetFeedbacks(generics.ListAPIView):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()


class GetTour(generics.RetrieveAPIView):
    serializer_class = TourSerializer
    queryset = Tour.objects.all()
    lookup_field = 'slug'

class CreateForm(APIView):
    def initialize_request(self, request, *args, **kwargs):
        setattr(request, 'csrf_processing_done', True)
        return super().initialize_request(request, *args, **kwargs)

    def post(self,request):
        data = request.data
        CallbackForm.objects.create(**data)
        return Response(status=200)

from django.urls import path,include
from . import views

urlpatterns = [
    path('categories', views.GetCategories.as_view()),
    path('tour/<slug>', views.GetTour.as_view()),
    path('send_form', views.CreateForm.as_view()),


]

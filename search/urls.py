from django.urls import path
from . import views


urlpatterns = [
    path('', views.FilterView, name = 'filter_search'),
   
] 
from django.contrib import admin
from django.urls import path, include
from .views import index

app_name = "inventaire"

urlpatterns = [
    path('', index, name='inventaire_index'),

]

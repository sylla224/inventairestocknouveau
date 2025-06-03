from django.contrib import admin
from django.urls import path, include
from .views import index, CreateProductView, ListProductView, EditProductview, DeleteProductview, DeleteProduct

app_name = "inventaire"

urlpatterns = [
    path('', index, name='inventaire_index'),
    path('dashboard', index, name='dashboard'),
    path('products', index, name='products'),
    path('categories', index, name='categories'),
    path('products/create', CreateProductView.as_view(), name='create_product'),
    path('products/', ListProductView.as_view(), name='products'),
    path('products/edit/<int:pk>/', EditProductview.as_view(), name='edit_product'),
    path('products/delete/<int:pk>/', DeleteProduct, name='delete_product'),
    path('products/delete/<int:pk>/confirm/', DeleteProductview.as_view(), name='confirm_delete_product'),

]

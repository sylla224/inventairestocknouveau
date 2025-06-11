from django.contrib import admin
from django.urls import path, include
from .views import (index, CreateProductView, ListProductView, EditProductview, DeleteProductview, DeleteProduct,
                    ListeEntrepotView, CreateEnterpriseView, TypeEnterpriseListView, typeenterprise_create,
                    typeenterprise_list_create)

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
    path('entreprise/listes', ListeEntrepotView.as_view(), name='liste_entreprise'),
    path('entreprise/create', CreateEnterpriseView.as_view(), name='create_entreprise'),
    path('typeenterprise/', TypeEnterpriseListView.as_view(), name='typeenterprise_list'),
    path('typeenterprise/create/', typeenterprise_create, name='typeenterprise_create'),
    path('typeenterprise/manage/', typeenterprise_list_create, name='typeenterprise_list_create'),

]

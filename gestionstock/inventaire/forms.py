from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nom du produit',
                'style': 'border: 2px solid #4caf50; padding: 10px;'
            }),
            'sku': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'ID du produit (SKU)',
                'style': 'border: 2px solid #4caf50; padding: 10px;'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Description du produit',
                'style': 'border: 2px solid #ff9800; padding: 10px;'
            }),
            'prix': forms.TextInput(attrs={
                'class': 'form-textarea',
                'placeholder': 'prix du produit',
                'style': 'border: 2px solid #4caf50; padding: 10px;'
            }),
            'seuil_alert': forms.TextInput(attrs={
                'class': 'form-textarea',
                'placeholder': 'Seuil d\'alerte',
                'style': 'border: 2px solid #f44336; padding: 10px;'
            }),
            'stock': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Stock',
                'style': 'border: 2px solid #4caf50; padding: 10px;'
            }),
        }
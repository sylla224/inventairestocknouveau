from django import forms
from .models import Product, Enterprise, TypeEnterprise


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
class EntrepriseForm(forms.ModelForm):
    class Meta:
        model = Enterprise
        fields = '__all__'
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-input block w-full px-3 py-2 border',
                'placeholder': 'Nom Entreprise',
                'style': 'border: 2px solid #4caf50; padding: 10px; <span class="text-red-500">*</span>',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Adresse de l\'entreprise',
                'style': 'border: 2px solid #4caf50; padding: 10px;'
            }),
        }
class TypeEnterpriseForm(forms.ModelForm):
    class Meta:
        model = TypeEnterprise
        fields = ['nom']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter enterprise type name',
                'required': True
            })
        }
        labels = {
            'nom': 'Enterprise Type Name'
        }

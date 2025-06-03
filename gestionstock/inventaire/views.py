from django.shortcuts import render
from  django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView

from inventaire.forms import ProductForm
from inventaire.models import Product
from django.urls import reverse_lazy


# Create your views here.
def index(request):
    """
    Render the index page of the inventory application.
    """
    return render(request, 'inventaire/index.html')
def CreateProduct(request):
    """
    Render the create product page.
    """
    return render(request, 'inventaire/create_product.html')

class CreateProductView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('inventaire:products')
    template_name = 'inventaire/create_product.html'
    pagination_by = 20

class ListProductView(ListView):
    model = Product
    template_name = 'inventaire/list_product.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()

class EditProductview(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventaire/edit_product.html'
    success_url = reverse_lazy('inventaire:products')

def DeleteProduct(request, pk):
    """
    Render the delete product page.
    """
    product = Product.objects.get(pk=pk)
    return render(request, 'inventaire/delete_product.html', {'product': product})

class DeleteProductview(DeleteView):
    model = Product
    template_name = 'inventaire/delete_product.html'
    success_url = reverse_lazy('inventaire:products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object
        return context



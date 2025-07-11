from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView, DetailView

from inventaire.forms import ProductForm, EntrepriseForm, TypeEnterpriseForm
from inventaire.models import Product, Enterprise, TypeEnterprise
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q


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
    #success_url = reverse_lazy('inventaire:products')
    template_name = 'inventaire/create_product.html'
    pagination_by = 20

    def get_template_names(self):
        user = self.request.user
        if user.is_authenticated and user.groups.filter(name='gestionnaire').exists():
            return ['inventaire/create_product_gestionnaire.html']
        elif user.is_authenticated and user.groups.filter(name='admin').exists():
            return ['inventaire/list_product.html']
        else:
            messages.error(self.request, 'You do not have permission to view this page.')
            return ['inventaire/index.html']
      

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated and user.groups.filter(name='gestionnaire').exists():
            messages.success(self.request, 'Product created successfully!')
            return reverse_lazy('inventaire:products')
        elif user.is_authenticated and user.groups.filter(name='admin').exists():
            messages.success(self.request, 'Product created successfully!')
            return reverse_lazy('inventaire:products')
        else:            messages.error(self.request, 'You do not have permission to create a product.')
        return super().get_success_url()
        




class ListProductView(ListView):
    model = Product
    #template_name = 'inventaire/list_product.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()
    def get_template_names(self):
        user = self.request.user
        if user.is_authenticated and user.groups.filter(name='gestionnaire').exists():
            return ['inventaire/list_product_gestionnaire.html']
        elif user.is_authenticated and user.groups.filter(name='admin').exists():
            return ['inventaire/list_product.html']
        else:
            messages.error(self.request, 'You do not have permission to view this page.')
            return ['inventaire/index.html']
    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated and user.groups.filter(name='gestionnaire').exists():
            messages.success(self.request, 'Product created successfully!')
            return reverse_lazy('inventaire:gestionnaire_products')
        elif user.is_authenticated and user.groups.filter(name='admin').exists():
            messages.success(self.request, 'Product created successfully!')
            return reverse_lazy('inventaire:products')
        else:            messages.error(self.request, 'You do not have permission to create a product.')
        return super().get_success_url()


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


##View pour les entreprises (entrepôts)
class ListeEntrepotView(ListView):
    model = Enterprise
    success_url = reverse_lazy('inventaire:liste_entreprise')
    template_name = 'inventaire/entreprise/listes.html'
    pagination_by = 20
    context_object_name = 'enterprises'


class CreateEnterpriseView(CreateView):
    model = Enterprise
    form_class = EntrepriseForm
    success_url = reverse_lazy('inventaire:liste_entreprise')
    template_name = 'inventaire/entreprise/add.html'


class EditEnterpriseView(UpdateView):
    model = Enterprise
    form_class = EntrepriseForm
    template_name = 'inventaire/entreprise/edit.html'
    success_url = reverse_lazy('inventaire:liste_entreprise')


class EnterpriseDetailView(DeleteView):
    model = Enterprise
    template_name = 'inventaire/entreprise/detail.html'
    fields = '__all__'
    context_object_name = 'enterprise'


class TypeEnterpriseListView(ListView):
    model = TypeEnterprise
    template_name = 'inventaire/typeenterprise/listes.html'
    context_object_name = 'typeenterprises'
    paginate_by = 10


def typeenterprise_create(request):
    if request.method == 'POST':
        form = TypeEnterpriseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Type Enterprise created successfully!')
            return redirect('inventaire:typeenterprise_list')
    else:
        form = TypeEnterpriseForm()

    return render(request, 'inventaire/typeenterprise/create.html', {'form': form})


def typeenterprise_list_create(request):
    """Combined view for listing and creating"""
    typeenterprises = TypeEnterprise.objects.all().order_by('-id')

    if request.method == 'POST':
        form = TypeEnterpriseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Type Enterprise created successfully!')
            return redirect('typeenterprise_list_create')
    else:
        form = TypeEnterpriseForm()

    context = {
        'typeenterprises': typeenterprises,
        'form': form
    }
    return render(request, 'typeenterprise/list_create.html', context)


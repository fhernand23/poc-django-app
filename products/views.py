import datetime
from math import prod
import django_filters
import qrcode
import uuid
from io import BytesIO
from PIL import Image, ImageDraw

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files import File
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from products.models import Provider, Product, ProductUnit, WhLocation, Client, LogisticUnitCode
from products.forms import AddProductUnitForm
from products.util import LOG_UNIT_TYPE_PRODUCT, generate_rfid_code
from pages.util import user_notifications


class BaseView(View):
     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # set user notifications
        if self.request.user.is_authenticated:
            context['user_notifications'] = user_notifications(self.request.user)
        return context


class FilteredListView(ListView):
    filterset_class = None

    def get_queryset(self):
        # Get the queryset however you usually would.  For example:
        queryset = super().get_queryset()
        # Then use the query parameters and the queryset to
        # instantiate a filterset and save it as an attribute
        # on the view instance for later.
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        # Return the filtered queryset
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the filterset to the template - it provides the form.
        context['filterset'] = self.filterset
        return context
        
        
# product section
class ProductFilterset(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = Product
        fields = ['price', 'date_created']


class ProductListView(BaseView, FilteredListView):
    model = Product
    paginate_by = 9
    template_name = "products/product_list.html"
    context_object_name = "products"
    filterset_class = ProductFilterset

    # def get_queryset(self, *args, **kwargs):
    #     user = self.request.user
    #     return Product.objects.filter(user__exact=user) # Get 50 notifications

class ProductDetailView(BaseView, DetailView):
    model = Product
    template_name = "products/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = kwargs.get("object")
        if object is not None:
            logisticunitcode = LogisticUnitCode.objects.filter(entity=LOG_UNIT_TYPE_PRODUCT, entity_id=object.id)
            if len(logisticunitcode) != 0:
                context['logisticunitcode'] = logisticunitcode[0]

        return context

class ProductCreate(PermissionRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'short_description', 'description', 'price', 'image', 'provider', 'archived']
    permission_required = 'product.can_add_product'


class ProductUpdate(PermissionRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'short_description', 'description', 'price', 'image', 'provider', 'archived']
    permission_required = 'product.can_change_product'


class ProductDelete(PermissionRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('products')
    permission_required = 'product.can_delete_product'


@login_required
def product_add_qr(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # check if exists previous code and delete
    LogisticUnitCode.objects.filter(entity=LOG_UNIT_TYPE_PRODUCT, entity_id=product.id).delete()
    # create base object
    log_unit_code = LogisticUnitCode(
        entity=LOG_UNIT_TYPE_PRODUCT, entity_id=product.id,
        description=f"Product {product.id}: {product.name}",
        rfid_code=generate_rfid_code(),
        entity_url=product.get_absolute_url(), entity_api_url=product.get_api_url()
    )
    full_url = request.build_absolute_uri(product.get_absolute_url())
    qr_image = qrcode.make(full_url)
    canvas = Image.new('RGB', (410, 410), "white")
    draw = ImageDraw.Draw(canvas)
    canvas.paste(qr_image)
    file_name = f'qr_{product.id}_{str(uuid.uuid4())}.png'
    stream = BytesIO()
    canvas.save(stream, 'PNG')
    log_unit_code.qr_code.save(file_name, File(stream), save=False)
    canvas.close()
    log_unit_code.save()
    # redirect to a new URL:
    return HttpResponseRedirect(product.get_absolute_url())


@login_required
def product_add_stock(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = AddProductUnitForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            product_unit = ProductUnit(
                product = product,
                action = 'buy',
                quantity = form.cleaned_data['quantity'],
                user = request.user,
                move_date = form.cleaned_data['move_date'],
                move_description = form.cleaned_data['description'],
                lot = form.cleaned_data['lot'],
            )
            product_unit.save()
            if form.cleaned_data['add_qr']:
                qr_image = qrcode.make(product_unit.get_absolute_url())
                qr_offset = Image.new('RGB', (310, 310), "white")
                qr_offset.paste(qr_image)
                files_name = f'Product{product.id}qr.png'
                stream = BytesIO()
                qr_offset.save(stream, 'PNG')
                product_unit.qrcode.save(files_name, File(stream), save=False)
                qr_offset.close()
                product_unit.save()
            # redirect to a new URL:
            return HttpResponseRedirect(product.get_absolute_url())

    default_date = datetime.date.today()
    form = AddProductUnitForm(initial={'move_date': default_date, 'quantity': 0, 'add_qr': False, 'description': '', 'lot': ''})

    context = {
        'form': form,
        'product': product,
    }

    return render(request, 'products/product_add_stock.html', context)


# providers section
class ProviderFilterset(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Provider
        fields = ['name', 'cuit', 'date_created']


class ProviderListView(BaseView, FilteredListView):
    model = Provider
    paginate_by = 9
    template_name = "products/provider_list.html"
    context_object_name = "providers"
    filterset_class = ProviderFilterset

    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(ProviderListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context


class ProviderDetailView(BaseView, DetailView):
    model = Provider
    template_name = "products/provider_detail.html"  


class ProviderCreate(PermissionRequiredMixin, CreateView):
    model = Provider
    fields = ['name', 'cuit', 'contact', 'documentation', 'avatar', 'archived']
    permission_required = 'provider.can_add_provider'


class ProviderUpdate(PermissionRequiredMixin, UpdateView):
    model = Provider
    fields = ['name', 'cuit', 'contact', 'documentation', 'avatar', 'archived']
    permission_required = 'provider.can_change_provider'


class ProviderDelete(PermissionRequiredMixin, DeleteView):
    model = Provider
    success_url = reverse_lazy('providers')
    permission_required = 'provider.can_delete_provider'


# wh location sectors
class WhLocationFilterset(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = WhLocation
        fields = ['name']


class WhLocationListView(BaseView, FilteredListView):
    model = WhLocation
    paginate_by = 10
    template_name = "products/whlocation_list.html"
    context_object_name = "whlocations"
    filterset_class = WhLocationFilterset


class WhLocationDetailView(BaseView, DetailView):
    model = WhLocation
    template_name = "products/whlocation_detail.html"


class WhLocationCreate(PermissionRequiredMixin, CreateView):
    model = WhLocation
    fields = ['name', 'description', 'archived']
    permission_required = 'wh_location.can_add_wh_location'


class WhLocationUpdate(PermissionRequiredMixin, UpdateView):
    model = WhLocation
    fields = ['name', 'description', 'archived']
    permission_required = 'wh_location.can_change_wh_location'


class WhLocationDelete(PermissionRequiredMixin, DeleteView):
    model = WhLocation
    success_url = reverse_lazy('providers')
    permission_required = 'wh_location.can_delete_wh_location'


# clients
class ClientFilterset(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Client
        fields = ['name', 'cuit', 'date_created']


class ClientListView(BaseView, FilteredListView):
    model = Client
    paginate_by = 9
    template_name = "products/client_list.html"
    context_object_name = "clients"
    filterset_class = ClientFilterset

class ClientDetailView(BaseView, DetailView):
    model = Client
    template_name = "products/client_detail.html"  


class ClientCreate(PermissionRequiredMixin, CreateView):
    model = Client
    fields = ['name', 'cuit', 'contact', 'documentation', 'archived']
    permission_required = 'client.can_add_client'


class ClientUpdate(PermissionRequiredMixin, UpdateView):
    model = Client
    fields = ['name', 'cuit', 'contact', 'documentation', 'archived']
    permission_required = 'client.can_change_client'


class ClientDelete(PermissionRequiredMixin, DeleteView):
    model = Provider
    success_url = reverse_lazy('clients')
    permission_required = 'client.can_delete_client'

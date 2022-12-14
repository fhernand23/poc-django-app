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

from products.models import ProductMoveType, Provider, Product, ProductUnit, WhLocation, Client, LogisticUnitCode, ProductMove
from products.forms import (InProductUnitForm, OutProductUnitForm, QualityProductUnitForm,
                            LocationProductUnitForm, GroupingProductUnitForm)
from products.util import (LOG_UNIT_TYPE_PRODUCT, generate_rfid_code, MOVE_IN, MOVE_IN_RFID, MOVE_OUT, MOVE_OUT_USE,
                           MOVE_CHANGE, MOVE_CHANGE_ERROR, MOVE_QUALITY, MOVE_CHANGE_VALUATION, MOVE_CHANGE_GROUPING,
                           MOVE_CHANGE_LOCATION, MOVE_RFID_FIND_ONE, MOVE_RFID_FIND_ALL, MOVE_RFID_LECTURE,
                           proccess_product_move)
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
def product_in_stock(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = InProductUnitForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            move_type = ProductMoveType.objects.filter(name__exact=MOVE_IN)[0]
            if form.cleaned_data['rfid_code']:
                move_type = ProductMoveType.objects.filter(name__exact=MOVE_IN_RFID)[0]
            product_move = ProductMove(
                product = product,
                move_type = move_type,
                provider = form.cleaned_data['provider'],
                wh_location_to = form.cleaned_data['wh_location'],
                product_packaging = form.cleaned_data['packaging'],
                move_date = form.cleaned_data['move_date'],
                lot = form.cleaned_data['lot'],
                quantity = form.cleaned_data['quantity'],
                unit_price = form.cleaned_data['unit_price'],
                unit_taxes = form.cleaned_data['unit_taxes'],
                total_price = form.cleaned_data['total_price'],
                user = request.user,
                expiration_date = form.cleaned_data['expiration_date'],
                add_qr = form.cleaned_data['add_qr'],
                rfid_code = form.cleaned_data['rfid_code'],
                description = form.cleaned_data['description'],
            )
            product_move.save()
            proccess_product_move(
                product_move=product_move
            )
            # redirect to a new URL:
            return HttpResponseRedirect(product.get_absolute_url())

    default_date = datetime.date.today()
    form = InProductUnitForm(
        initial={
            'move_date': default_date, 'quantity': 0, 'add_qr': False, 
            'description': '', 'lot': '',
            'unit_price': 0.0, 'unit_taxes': 0.0, 'total_price': 0.0
        }
    )

    context = {
        'form': form,
        'product': product,
    }

    return render(request, 'products/product_in_stock.html', context)


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


class ProductMoveDetailView(BaseView, DetailView):
    model = ProductMove
    template_name = "products/productmove_detail.html"


class ProductUnitDetailView(BaseView, DetailView):
    model = ProductUnit
    template_name = "products/productunit_detail.html"


class ProductMoveFilterset(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ProductMove
        fields = ['name']


class ProductMoveListView(BaseView, FilteredListView):
    model = ProductMove
    paginate_by = 10
    template_name = "products/productmove_list.html"
    context_object_name = "productmoves"
    filterset_class = ProductMoveFilterset


class ProductUnitFilterset(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ProductUnit
        fields = ['name']


class ProductUnitListView(BaseView, FilteredListView):
    model = ProductUnit
    paginate_by = 10
    template_name = "products/productunit_list.html"
    context_object_name = "productunits"
    filterset_class = ProductUnitFilterset


@login_required
def product_out_stock(request, pk):
    productunit = get_object_or_404(ProductUnit, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = OutProductUnitForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            move_type = ProductMoveType.objects.filter(name__exact=MOVE_OUT)[0]
            if form.cleaned_data['internal_usage']:
                move_type = ProductMoveType.objects.filter(name__exact=MOVE_OUT_USE)[0]
            product_move = ProductMove(
                product = productunit.product,
                product_unit = productunit,
                move_type = move_type,
                move_date = form.cleaned_data['move_date'],
                quantity = form.cleaned_data['quantity'],
                user = request.user,
                description = form.cleaned_data['description'],
            )
            if move_type.name == MOVE_OUT:
                product_move.client = form.cleaned_data['client']
                product_move.unit_price = form.cleaned_data['unit_price']
                product_move.unit_taxes = form.cleaned_data['unit_taxes']
                product_move.total_price = form.cleaned_data['total_price']

            product_move.save()
            proccess_product_move(
                product_move=product_move
            )
            # redirect to a new URL:
            return HttpResponseRedirect(productunit.product.get_absolute_url())

    default_date = datetime.date.today()
    form = OutProductUnitForm(
        initial={
            'move_date': default_date, 'quantity': 0,
            'description': '',
            'unit_price': 0.0, 'unit_taxes': 0.0, 'total_price': 0.0
        }
    )

    context = {
        'form': form,
        'productunit': productunit,
    }

    return render(request, 'products/product_out_stock.html', context)


@login_required
def product_quality_check(request, pk):
    productunit = get_object_or_404(ProductUnit, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = QualityProductUnitForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            move_type = ProductMoveType.objects.filter(name__exact=MOVE_QUALITY)[0]
            product_move = ProductMove(
                product = productunit.product,
                product_unit = productunit,
                move_type = move_type,
                move_date = form.cleaned_data['move_date'],
                quantity = form.cleaned_data['quantity'],
                user = request.user,
                description = form.cleaned_data['description'],
            )
            product_move.save()
            proccess_product_move(
                product_move=product_move
            )
            # redirect to a new URL:
            return HttpResponseRedirect(productunit.product.get_absolute_url())

    default_date = datetime.date.today()
    form = QualityProductUnitForm(
        initial={
            'move_date': default_date, 'quantity': 0,
            'description': '',
        }
    )

    context = {
        'form': form,
        'productunit': productunit,
    }

    return render(request, 'products/product_quality_check.html', context)


@login_required
def product_change_location(request, pk):
    productunit = get_object_or_404(ProductUnit, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = LocationProductUnitForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            move_type = ProductMoveType.objects.filter(name__exact=MOVE_CHANGE_LOCATION)[0]
            product_move = ProductMove(
                product = productunit.product,
                product_unit = productunit,
                move_type = move_type,
                move_date = form.cleaned_data['move_date'],
                user = request.user,
                description = form.cleaned_data['description'],
                quantity = productunit.quantity,
                wh_location_to = form.cleaned_data['wh_location_to'],
            )

            product_move.save()
            proccess_product_move(
                product_move=product_move
            )
            # redirect to a new URL:
            return HttpResponseRedirect(productunit.product.get_absolute_url())

    default_date = datetime.date.today()
    form = LocationProductUnitForm(
        initial={
            'move_date': default_date,
            'description': ''
        }
    )

    context = {
        'form': form,
        'productunit': productunit,
    }

    return render(request, 'products/product_change_location.html', context)


@login_required
def product_change_grouping(request, pk):
    productunit = get_object_or_404(ProductUnit, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = GroupingProductUnitForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            move_type = ProductMoveType.objects.filter(name__exact=MOVE_CHANGE_GROUPING)[0]
            product_move = ProductMove(
                product = productunit.product,
                product_unit = productunit,
                move_type = move_type,
                move_date = form.cleaned_data['move_date'],
                user = request.user,
                description = form.cleaned_data['description'],
                quantity = productunit.quantity,
                product_packaging = form.cleaned_data['packaging_to'],
            )

            product_move.save()
            proccess_product_move(
                product_move=product_move
            )
            # redirect to a new URL:
            return HttpResponseRedirect(productunit.product.get_absolute_url())

    default_date = datetime.date.today()
    form = GroupingProductUnitForm(
        initial={
            'move_date': default_date,
            'description': ''
        }
    )

    context = {
        'form': form,
        'productunit': productunit,
    }

    return render(request, 'products/product_change_grouping.html', context)

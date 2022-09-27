from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from .models import Provider, Product, ProductUnit, WhLocation
from django.urls import reverse_lazy
from pages.util import user_notifications
import django_filters


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

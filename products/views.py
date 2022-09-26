from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from .models import Provider, Product, ProductUnit, WhLocation
from django.urls import reverse_lazy
from pages.util import user_notifications


class BaseView(View):
     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # set user notifications
        if self.request.user.is_authenticated:
            context['user_notifications'] = user_notifications(self.request.user)
        return context


class ProductListView(BaseView, ListView):
    model = Product
    paginate_by = 9
    template_name = "products/product_list.html"
    context_object_name = "products"

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


class ProviderListView(BaseView, ListView):
    model = Provider
    paginate_by = 9
    template_name = "products/provider_list.html"
    context_object_name = "providers"

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


class WhLocationListView(BaseView, ListView):
    model = WhLocation
    paginate_by = 10
    template_name = "products/whlocation_list.html"
    context_object_name = "wh_locations"


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

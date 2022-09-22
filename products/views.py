from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, View
from django.contrib.messages.views import SuccessMessageMixin
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from .models import Provider, Product, ProductUnit

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

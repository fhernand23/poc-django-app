from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from .models import Notification, Provider, Product, ProductUnit


class BaseView(View):
     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO set user notifications
        return context


class ProductListView(LoginRequiredMixin, SuccessMessageMixin, BaseView, ListView):
    queryset = Product.objects.all()
    template_name = "products/product_list.html"
    context_object_name = "products"


class ProductDetailView(LoginRequiredMixin, BaseView, DetailView):
    model = Product 
    template_name = "products/product_detail.html"


class ProviderListView(LoginRequiredMixin, SuccessMessageMixin, BaseView, ListView):
    queryset = Provider.objects.all()
    # paginate_by:
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


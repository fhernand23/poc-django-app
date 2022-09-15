from django.views.generic import TemplateView
from products.models import Product, Provider
from django.views.generic import ListView, DetailView, TemplateView, View

class BaseView(View):
     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['catalog'] = Catalog.objects.order_by('-date_updated').first()
        # if self.request.user.is_authenticated:
        #     if Publisher.objects.filter(user_id=self.request.user.id).count() > 0:
        #         context['publisher'] = Publisher.objects.get(user_id=self.request.user.id)
        return context


class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"


class PubProductDetailView(BaseView, DetailView):
    model = Product
    template_name = "pages/product_detail.html"  


class PubProductList(BaseView,ListView):
    model = Product
    template_name = "pages/product_list.html"
    context_object_name = "products"


class PubProviderList(BaseView,ListView):
    model = Provider
    template_name = "pages/provider_list.html"
    context_object_name = "providers"

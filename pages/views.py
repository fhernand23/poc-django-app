from django import template
from django.views.generic import TemplateView
from products.models import Product, Provider
from django.views.generic import ListView, DetailView, TemplateView, View
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

class BaseView(View):
     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"


@login_required(login_url="/login/")
def homedev(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('pages/homedev.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def devpages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('pages/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('pages/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('pages/page-500.html')
        return HttpResponse(html_template.render(context, request))


class PubProductListView(BaseView,ListView):
    model = Product
    template_name = "pages/product_list.html"
    context_object_name = "products"


class PubProductDetailView(BaseView, DetailView):
    model = Product
    template_name = "pages/product_detail.html"  


class PubProviderListView(BaseView,ListView):
    model = Provider
    template_name = "pages/provider_list.html"
    context_object_name = "providers"

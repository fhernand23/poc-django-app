from django.shortcuts import render
from django import template
from django.views.generic import TemplateView
from products.models import Product, Provider, Notification
from django.views.generic import ListView, DetailView, TemplateView, View
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from pages.util import create_demo_data, user_notifications

class BaseView(View):
     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # set user notifications
        if self.request.user.is_authenticated:
            context['user_notifications'] = user_notifications(self.request.user)
        return context


def home(request):
    msg = ""
    if request.method == "POST":
        data = request.POST
        action = data.get("admin_action")
        if action == "demodata":
            # create sample data
            msg = create_demo_data()
            # msg = f"Requested action: {action}"
        else:
            msg = f"Unknown requested action: {action}"
    context = {
        'msg_success': msg,
        'user_notifications': user_notifications(request.user),
    }
    return render(request, "pages/home.html", context=context)


class AboutPageView(BaseView, TemplateView):
    template_name = "pages/about.html"


@login_required(login_url="/accounts/login/")
def homedev(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('pages/homedev.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/accounts/login/")
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


class NotificationsListView(BaseView, ListView):
    model = Notification
    paginate_by = 10
    template_name = "pages/notifications.html"
    context_object_name = "notifications"

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        return Notification.objects.filter(user__exact=user)[:50] # Get 50 notifications

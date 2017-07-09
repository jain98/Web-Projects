from django.conf.urls import include, url
from django.views.generic import TemplateView
from drchrono import views as mv
from django.contrib import admin

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^complete/drchrono/$', mv.auth),
    url(r'^options$', mv.options),
    url(r'^birthdays$', mv.birthdays),
    url(r'^send_message$', mv.send_message),
    url(r'^admin/', admin.site.urls),
    url(r'', include('social.apps.django_app.urls', namespace='social'))
]

from django.conf.urls import include, url
from django.views.generic import TemplateView
from drchrono import views as mv
from django.contrib import admin

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^complete/drchrono/$', mv.auth),
    url(r'^check-in', mv.check_in),
    url(r'^demographics/(?P<pid>\w+)/', mv.demographics),
    url(r'^update_info/(?P<pid>\w+)', mv.update_info),
    url(r'^start/', mv.start_appointment),
    url(r'^end/', mv.end_appointment),
    url(r'^options$', mv.options),
    url(r'^status$', mv.status),
    url(r'^update/$', mv.update),
    url(r'^welcome/$', mv.welcome),
    url(r'^error/$', mv.error),
    url(r'^success/$', mv.success),
    url(r'^admin/', admin.site.urls),
    url(r'', include('social.apps.django_app.urls', namespace='social'))
]

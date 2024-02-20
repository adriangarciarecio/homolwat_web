from django.urls import path
from django.views.generic.base import RedirectView
#from home import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from modules.home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('manual', views.manual, name='manual'),
    path('contact', views.contact, name='contact'),
]

if settings.DEBUG:
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
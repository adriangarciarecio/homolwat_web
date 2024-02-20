from django.urls import path
from django.views.generic.base import RedirectView
#from home import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from modules.crystal import views

urlpatterns = [
    path('', views.crystal, name='crystal'),
    path('graphic_crystal', views.graphic_crystal, name='graphic_crystal'),
    path('structure_crystal', views.structure_crystal, name='structure_crystal'),
]

if settings.DEBUG:
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
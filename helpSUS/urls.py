
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('recepcao/', include('recepcao.urls')),
    path('triagem/', include('triagem.urls')),
    path('consultorio/', include('consultorio.urls')),
    path('farmacia/', include('farmacia.urls')),
    path('laboratorio/', include('laboratorio.urls')),
    path("favicon.ico",  RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")))
]

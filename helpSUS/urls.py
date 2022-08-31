
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('recepcao/', include('recepcao.urls')),
    path('triagem/', include('triagem.urls')),
    path('consultorio/', include('consultorio.urls')),
    path('farmacia/', include('farmacia.urls'))
]

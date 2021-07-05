from django.urls import path

from .views import mainRecepcao

urlpatterns = [
    path('', mainRecepcao, name='mainRecepcao'),
]
from django.urls import path

from .views import IndexView, signUp

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('sign-up', signUp, name='signUp')
]
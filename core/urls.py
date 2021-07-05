from django.urls import path

from .views import IndexView, signUpView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('sign-up', signUpView.as_view(), name='signUp')
]
from django.urls import path

from .views import IndexView, signUpView, ReqNewPasswordView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('sign-up', signUpView.as_view(), name='signUp'),
    path('new-req-password', ReqNewPasswordView.as_view(), name='reqNewPassword')
]
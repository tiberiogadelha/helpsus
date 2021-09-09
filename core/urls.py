from django.urls import path

from .views import IndexView, signUpView, ReqNewPasswordView, logout_view

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('sign-up', signUpView.as_view(), name='signUp'),
    path('new-req-password', ReqNewPasswordView.as_view(), name='reqNewPassword'),
    path('logout', logout_view.as_view(), name='logout')
]
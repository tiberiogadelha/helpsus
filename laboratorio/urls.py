from django.urls import path

from .views import CreateExamView, HandleExamView

urlpatterns = [
    path('criar-exame', CreateExamView.as_view(), name='criarExame'),
    path('view-exames', HandleExamView.as_view(), name='viewExames'),
]
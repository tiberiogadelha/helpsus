from django.urls import path

from .views import CreateExamView, HandleExamView, PendingExamView, ConfirmExamView, IndexLaboratorio

urlpatterns = [
    path('', IndexLaboratorio.as_view(), name='indexLaboratorio'),
    path('criar-exame', CreateExamView.as_view(), name='criarExame'),
    path('view-exames', HandleExamView.as_view(), name='viewExames'),
    path('exames-pendentes', PendingExamView.as_view(), name='examesPendentes'),
    path('liberar-exame', ConfirmExamView.as_view(), name='liberarExame'),
]
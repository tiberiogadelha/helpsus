from django.conf.urls import url
from django.urls import path

from .views import RequireExamView, IndexConsultorioView, RequireMedView, IssueSickNoteView

urlpatterns = [
    path('solicitar-exame', RequireExamView.as_view(), name='solicitarExameConsultorio'),
    path('', IndexConsultorioView.as_view(), name='indexConsultorio'),
    path('solicitar-medicamentos', RequireMedView.as_view(), name='solicitarMedicamentoConsultorio'),
    path('emitir-atestado', IssueSickNoteView.as_view(), name='emitirAtestado')
]
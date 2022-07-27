from django.conf.urls import url
from django.urls import path

from .views import RequireExamView, IndexConsultorioView, RequireMedView, IssueSickNoteView, PendingPacientsMedView, \
    UpdateAttendanceMedView

urlpatterns = [
    path('solicitar-exame', RequireExamView.as_view(), name='solicitarExameConsultorio'),
    path('', IndexConsultorioView.as_view(), name='indexClinic'),
    path('solicitar-medicamentos', RequireMedView.as_view(), name='solicitarMedicamentoConsultorio'),
    path('emitir-atestado', IssueSickNoteView.as_view(), name='emitirAtestado'),
    path('visualizar-pacientes-pendentes', PendingPacientsMedView.as_view(), name='visualizarPacientesPendentesConsultorio'),
    path('atualizar-atendimento', UpdateAttendanceMedView.as_view(), name='updateAttendanceConsultorio'),
]
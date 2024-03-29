from django.conf.urls import url
from django.urls import path, re_path

from .views import RequireExamView, IndexConsultorioView, RequireMedView, IssueSickNoteView, PendingPacientsMedView, \
    UpdateAttendanceMedView, RequireMedListView, get_med_order_details, PatientHistoryView, ViewAttendanceDetails, \
    ViewFinishAttendance, RequireExamsListView, download_sick_note

urlpatterns = [
    path('solicitar-exame', RequireExamView.as_view(), name='solicitarExameConsultorio'),
    path('', IndexConsultorioView.as_view(), name='indexClinic'),
    path('solicitar-medicamentos', RequireMedView.as_view(), name='solicitarMedicamentoConsultorio'),
    path('emitir-atestado', IssueSickNoteView.as_view(), name='emitirAtestado'),
    path('visualizar-pacientes-pendentes', PendingPacientsMedView.as_view(), name='visualizarPacientesPendentesConsultorio'),
    path('atualizar-atendimento', UpdateAttendanceMedView.as_view(), name='updateAttendanceConsultorio'),
    path('visualizar-medicamentos-solicitados', RequireMedListView.as_view(), name='visualizarMedicamentosSolicitados'),
    path('visualizar-exames-solicitados', RequireExamsListView.as_view(), name='visualizarExamesSolicitadosConsultorio'),
    re_path('get-med-order/(?P<order_id>.+)', get_med_order_details),
    re_path('download-sick-note/(?P<pk>.+)', download_sick_note, name='downloadSickNote'),
    path('visualizar-historico-paciente', PatientHistoryView.as_view(), name='visualizarHistoricoPaciente'),
    path('atender-paciente/', ViewAttendanceDetails.as_view(), name='atenderPacienteConsultorio'),
    path('finalizar-atendimento', ViewFinishAttendance.as_view(), name='finalizarAtendimento')
]

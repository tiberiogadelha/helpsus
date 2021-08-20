from django.conf.urls import url
from django.urls import path

from .views import PatientView, IndexReception, CreateAttendanceView, ConfirmAttendanceView, ViewAttendancesView, RemoveAttendanceView, EditPatientView

urlpatterns = [
    path('paciente', PatientView.as_view(), name='newPatient'),
    path('', IndexReception.as_view(), name='indexReception'),
    path('atendimento', CreateAttendanceView.as_view(), name='newAttendance'),
    path('editar-paciente', EditPatientView.as_view(), name='editPatient'),
    path('confirmadoAtendimento', ConfirmAttendanceView.as_view(), name='confirmAttendance'),
    path('visualizarAtendimentos', ViewAttendancesView.as_view(), name='viewAttendances'),
    path('atendimento/deletar', RemoveAttendanceView.as_view(), name='removeAttendance'),

]
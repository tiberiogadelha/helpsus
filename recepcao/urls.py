from django.urls import path

from .views import PatientView, IndexReception, CreateAttendanceView, ConfirmAttendanceView, ViewAttendancesView

urlpatterns = [
    path('paciente', PatientView.as_view(), name='newPatient'),
    path('', IndexReception.as_view(), name='indexReception'),
    path('atendimento', CreateAttendanceView.as_view(), name='newAttendance'),
    path('confirmadoAtendimento', ConfirmAttendanceView.as_view(), name='confirmAttendance'),
    path('visualizarAtendimentos', ViewAttendancesView.as_view(), name='viewAttendances')

]
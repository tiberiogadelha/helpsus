from django.conf.urls import url
from django.urls import path

from .views import IndexPharmacy

urlpatterns = [
    path('', IndexPharmacy.as_view(), name='indexPharmacy'),
    # path('atendimento', CreateAttendanceView.as_view(), name='newAttendance'),
    # path('editar-paciente', EditPatientView.as_view(), name='editPatient'),
    # path('confirmadoAtendimento', ConfirmAttendanceView.as_view(), name='confirmAttendance'),
    # path('visualizarAtendimentos', ViewAttendancesView.as_view(), name='viewAttendances'),
    # path('atendimento/deletar', RemoveAttendanceView.as_view(), name='removeAttendance'),

]
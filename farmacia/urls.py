from django.conf.urls import url
from django.urls import path, re_path

from .views import IndexPharmacy, HandleMedicationOrderPharmacy

urlpatterns = [
    path('', IndexPharmacy.as_view(), name='indexPharmacy'),
    re_path(r'detalhes-requisicao/((?P<order>.+))?', HandleMedicationOrderPharmacy.as_view(), name='handleMedicationOrder'),
    # path('editar-paciente', EditPatientView.as_view(), name='editPatient'),
    # path('confirmadoAtendimento', ConfirmAttendanceView.as_view(), name='confirmAttendance'),
    # path('visualizarAtendimentos', ViewAttendancesView.as_view(), name='viewAttendances'),
    # path('atendimento/deletar', RemoveAttendanceView.as_view(), name='removeAttendance'),

]
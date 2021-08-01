from django.urls import path

from .views import PatientView, IndexReception, CreateAttendanceView

urlpatterns = [
    path('testando', PatientView.as_view(), name='newPatient'),
    path('', IndexReception.as_view(), name='indexReception'),
    path('atendimento', CreateAttendanceView.as_view(), name='newAttendance')

]
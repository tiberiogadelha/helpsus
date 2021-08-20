from django.conf.urls import url
from django.urls import path

from .views import IndexView, GetAttendancesView, UpdateAttendanceView

urlpatterns = [
    path('', IndexView.as_view(), name='indexTriagem'),
    path('getAttendances', GetAttendancesView.as_view(), name='getAttendancesTriagem'),
    path('updateAttendance', UpdateAttendanceView.as_view(), name='updateAttendanceTriagem')

]
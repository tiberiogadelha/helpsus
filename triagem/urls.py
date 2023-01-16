from django.conf.urls import url
from django.urls import path

from .views import IndexView, GetAttendancesView, UpdateAttendanceView, EditLastAttendanceView

urlpatterns = [
    path('', IndexView.as_view(), name='indexTriagem'),
    path('getAttendances', GetAttendancesView.as_view(), name='getAttendancesTriagem'),
    path('updateAttendance', UpdateAttendanceView.as_view(), name='updateAttendanceTriagem'),
    path('editLastAttendance', EditLastAttendanceView.as_view(), name='editLastAttendanceTriagem')

]
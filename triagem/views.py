from django.db.models.query_utils import Q
from django.shortcuts import render

from django.http import request
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView 
from core.models import Attendance, Patient
from datetime import date
from .forms import TriagemForm
from .util import calculate_age

class IndexView(TemplateView):
    template_name = 'indexTriagem.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class GetAttendancesView(TemplateView):
    template_name = 'getAttendancesTriagem.html'

    def get_context_data(self, **kwargs):
        context = super(GetAttendancesView, self).get_context_data(**kwargs)
        try:
            sql = "SELECT * FROM core_attendance WHERE STATUS = 'aguardando' ORDER BY created_at, creation_hour"
            attendances = Attendance.objects.raw(sql)
            context['attendances'] = attendances
            return context
        except Exception as e:
            print(e.__str__())
            return super().get_context_data(**kwargs)

        return super().get_context_data(**kwargs)

class UpdateAttendanceView(TemplateView):
    template_name = 'updateAttendance.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateAttendanceView, self).get_context_data(**kwargs)
        try:
            id = self.request.GET['id']
            attendance = Attendance.objects.filter(id = id).first()
            birth_date = attendance.patient.birth_date
            age = f'{calculate_age(birth_date)} anos'
            formated_date = attendance.patient.birth_date.strftime("%d/%m/%Y")
            attendance.patient.formated_date = f'{formated_date} - Idade: {age} anos'
            entrada = attendance.created_at.strftime("%d/%m/%Y")
            if (attendance.status == 'aguardando'):
               context["attendance"] = attendance 
               entrance = f'{entrada} às {str(attendance.creation_hour)[:5]}'
               meta_data = { 'age': age, 'entrance': entrance }
               context['meta'] = meta_data
        except Exception as e:
            print(e.__str__())
            return context
        form = TriagemForm()
        context['form'] = form
        
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)

        except Exception as e:
            return super().get(request, *args, **kwargs)

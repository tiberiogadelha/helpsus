from django.shortcuts import render
import pytz
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView 
from core.models import Attendance, Patient, Triagem, VitalData
from datetime import date, datetime, timedelta
from .forms import TriagemForm
from .util import alocate_patient, calculate_age, extract_vital_data, extract_triagem_data

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'indexTriagem.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class GetAttendancesView(LoginRequiredMixin, TemplateView):
    template_name = 'getAttendancesTriagem.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(GetAttendancesView, self).get_context_data(**kwargs)
        try:
            if ('filter' in self.request.GET):
                filter = self.request.GET['filter']
                filter = filter.split('-')
                date1 = datetime(int(filter[0]), int(filter[1]), int(filter[2]), 0, 0, 0)
                date2 = datetime(int(filter[0]), int(filter[1]), int(filter[2]), 23, 59, 59)
                sql = f"SELECT * FROM core_attendance WHERE STATUS = 'aguardando' AND (created_at between '{date1.__str__()}' AND '{date2.__str__()}')  ORDER  BY created_at, creation_hour"
                attendances = Attendance.objects.raw(sql)

            else: 
                sql = "SELECT * FROM core_attendance WHERE STATUS = 'aguardando' ORDER BY created_at, creation_hour"
                attendances = Attendance.objects.raw(sql)
            context['attendances'] = attendances
            return context
        except Exception as e:
            print(e)
            return super().get_context_data(**kwargs)

class UpdateAttendanceView(LoginRequiredMixin, TemplateView):
    template_name = 'updateAttendance.html'
    login_url = '/'

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
            
            form = TriagemForm() if (self.request.method == 'GET') else TriagemForm(self.request.POST)
        except Exception as e:
            if (self.request.method == 'POST'):
                form = TriagemForm(self.request.POST)
            else:  
                form = TriagemForm()

            context['form'] = form
            return context
        context['form'] = form
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            attendance_id = request.POST['id']
            form = TriagemForm(request.POST)
            if (form.is_valid()):
                try:
                    attendance = Attendance.objects.get(id = attendance_id)
                    if (attendance.status != 'aguardando'):
                        messages.error(request, 'Status do atendimento inválido')
                        return super().get(request, *args, **kwargs)

                except Attendance.DoesNotExist:
                    messages.error(request, 'Atendimento não encontrado')
                    return super().get(request, *args, **kwargs)
                attendance.moment_triagem = datetime.now(pytz.utc)
                attendance.save()
                vital_data = extract_vital_data(form)
                
                created_vital = VitalData.objects.create(temperature=vital_data.temperature, pad=vital_data.pad, pas=vital_data.pas, saturation=vital_data.saturation, heart_beats=vital_data.heart_beats)
                created_vital.save()
                triagem = extract_triagem_data(form)
                attendance.status = 'triagem'
                attendance.priority = triagem.priority
                attendance.save()
                triagem.attendance = attendance
                triagem.responsible = request.user
                triagem.vital_data = created_vital
                triagem.save()
                
                alocate_patient(attendance)
                messages.success(request, 'Triagem do paciente finalizada!')
                
                return redirect('getAttendancesTriagem')
            print(form.errors)
            id = request.POST.id
            query = f'?id={id}'
            return redirect(reverse('updateAttendanceTriagem') + query)

        except Exception as e:
            print(e)
            return super().get(request, *args, **kwargs)

class EditLastAttendanceView(LoginRequiredMixin, TemplateView):
    template_name = 'editLastAttendanceTriagem.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(EditLastAttendanceView, self).get_context_data(**kwargs)
        try:
            id = 13
            attendance = Attendance.objects.filter(id = id).first()
            birth_date = attendance.patient.birth_date
            age = f'{calculate_age(birth_date)} anos'
            formated_date = attendance.patient.birth_date.strftime("%d/%m/%Y")
            attendance.patient.formated_date = f'{formated_date} - Idade: {age} anos'
            entrada = attendance.created_at.strftime("%d/%m/%Y")
            
            context["attendance"] = attendance 
            entrance = f'{entrada} às {str(attendance.creation_hour)[:5]}'
            meta_data = { 'age': age, 'entrance': entrance }
            context['meta'] = meta_data
            sql_triagem = "SELECT * FROM core_triagem WHERE attendance_id=" + str(id)
            triagem = Triagem.objects.raw(sql_triagem)
            form = TriagemForm() if (self.request.method == 'GET') else TriagemForm(self.request.POST)
            context['triagem'] = triagem[0]
        except Exception as e:
            print(e.__str__())
            if (self.request.method == 'POST'):
                form = TriagemForm(self.request.POST)
            else:  
                form = TriagemForm()

            context['form'] = form
            return context
        context['form'] = form
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)



import datetime

import pytz
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
from django.shortcuts import render
from django.views.generic.base import View

from helpSUS.settings import TIME_ZONE
from .forms import PatientForm, PatientUpdate
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView 
from core.models import Attendance, Patient
from .util import Util
from datetime import date as dateClass


class PatientView(TemplateView):
    template_name = 'newPatient.html'

    def get_context_data(self, **kwargs):
        context = super(PatientView, self).get_context_data(**kwargs)
        try:
            if(self.request.method != 'GET'):
                context['form'] = PatientForm(self.request.POST)
            else:
                context['form'] = PatientForm()
        except: 
            context['form'] = PatientForm()
        return context
        
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            patient = PatientForm(request.POST)
            if (not(patient.is_valid())):
                messages.error(request, 'Preencha os dados do paciente corretamente!')
                
            patient.save()
            messages.success(request, 'Paciente cadastrado com sucesso!')
            return super().get(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, e.__str__())
            return super().get(request, *args, **kwargs)


class IndexReception(TemplateView):
    template_name = 'indexReception.html'

    def get_context_data(self, **kwargs):
        context = super(IndexReception, self).get_context_data(**kwargs)
        context['att'] = '23232'
        return context


class CreateAttendanceView(LoginRequiredMixin, TemplateView):
    template_name = 'newAttendance.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(CreateAttendanceView, self).get_context_data(**kwargs)
        try:
            if self.request.POST:
                return
            if self.request.GET.__contains__('patient_data'):
                if self.request.GET['patient_data'] != 'patient_data':
                    patient_id = self.request.GET['patient_data']
                    try:
                        patient = Patient.objects.filter(id=patient_id).first()
                        if patient is None:
                            messages.error(self.request, "Paciente não encontrado. Faça o cadastro")
                            return redirect('newPatient')
                        context['userData'] = patient
                    except Patient.DoesNotExist:
                            messages.error(self.request, "Paciente não encontrado. Faça o cadastro!")
        except Exception as e:
            messages.error(request, e.__str__())

        context['patients'] = Patient.objects.all()
        return context
        
    def get(self, request, *args, **kwargs):
        try:
            if (self.request.GET.__contains__('patient_data')):
                patient_id = request.GET['patient_data']
                try: 
                    patient = Patient.objects.filter(id=patient_id).first()
                    if(not(patient)):
                        messages.error(request, "Paciente não encontrado. Faça o cadastro")
                        return redirect('newPatient')
                except Patient.DoesNotExist:
                    messages.error(request, "Paciente não encontrado. Faça o cadastro!")
        except Exception as e:
            messages.error(request, e.__str__())

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            patient_id = request.POST['patient_id']
            patient = Patient.objects.filter(id=patient_id).first()

            if not patient:
                messages.error(request, 'Paciente não encontrado')

            attendance = Attendance()
            util = Util()
            ficha = util.getFicha()
            attendance.num = ficha
            attendance.patient = patient
            attendance.status = 'aguardando'
            attendance.save()
            query = f'?nome={patient.name}&ficha={attendance.num}'
            return redirect(reverse('confirmAttendance') + query)
        
            
        except Patient.DoesNotExist:
            messages.error(request, 'Paciente não encontrado')
        except Exception as e:
            messages.error(request, e.__str__())
    
        return super().get(request, *args, **kwargs)

class ConfirmAttendanceView(TemplateView):
    template_name = 'confirmAttendance.html'

    def get_context_data(self, **kwargs):
        context = super(ConfirmAttendanceView, self).get_context_data(**kwargs)
        try:
            context['nome'] = self.request.GET['nome']
            context['ficha'] = self.request.GET['ficha']
            return context
        except Exception as e:
            messages.error(self.request, 'Dados inválidos')
        return super().get_context_data(**kwargs)

class ViewAttendancesView(TemplateView):
    template_name = 'viewAttendances.html'

    def get_context_data(self, **kwargs):
        context = super(ViewAttendancesView, self).get_context_data(**kwargs)
        if 'filter' in self.request.GET and self.request.GET['filter']:
            date = self.request.GET['filter'].split('-')
            date1 = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), 0, 0, 0)
            date1 = pytz.timezone(TIME_ZONE).localize(date1)
            date2 = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), 23, 59, 59)
            date2 = pytz.timezone(TIME_ZONE).localize(date2)

            attendances = Attendance.objects.filter(
                created_at__gte=date1,
                created_at__lte=date2

            )

            context['attendances'] = attendances
        else:
            today_start = Util.agora().replace(hour=0, minute=0, second=0)
            today_end = Util.agora().replace(hour=23, minute=59, second=59)

            attendances = Attendance.objects.filter(
                created_at__gte=today_start,
                created_at__lte=today_end
            )
            context['attendances'] = attendances

        return context

class RemoveAttendanceView(TemplateView):
    template_name = 'removeAttendance.html'

    def get_context_data(self, **kwargs):
        context = super(RemoveAttendanceView, self).get_context_data(**kwargs)
        try:
            id = self.request.GET['id']
            attendance = Attendance.objects.filter(id=id).first()
            context['attendance'] = attendance
            try:
                context['deleted'] = self.request.GET['success']
            except:
                None
            return context
        except Exception as e:
            return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs): 
        try:
            id = request.POST['attendance_id']
            attendance = Attendance.objects.get(id=int(id))
            attendance.delete()
            messages.success(request, 'Atendimento removido com sucesso!')
            return redirect('viewAttendances')
        except Exception as e:
            messages.error(request, e.__str__()) 

        return super().get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class EditPatientView(TemplateView):
    template_name = 'viewPatients.html'

    def format_date(self, date):
        splited = date.split('-')
        new_date = f'{splited[2]}/{splited[1]}/{splited[0]}'
        return new_date

    def get_context_data(self, **kwargs):
        context = super(EditPatientView, self).get_context_data(**kwargs)
        try:
            if self.request.POST:
                return

            patient_data = self.request.GET.get('patient_data')
            if patient_data != 'patient_data' and patient_data is not None:
                if self.request.method == 'GET':
                    patient_id = self.request.GET['patient_data']
                else:
                    patient_id = self.request.POST['id_patient']
                try:
                    patient = Patient.objects.filter(id=patient_id).first()
                    if patient is None:
                        messages.error(self.request, "Paciente não encontrado. Faça o cadastro")
                        return redirect('editPatient')

                    context['userData'] = patient
                    if self.request.method != 'GET':
                        context['form'] = PatientUpdate(self.request.POST)
                    else:
                        context['form'] = PatientUpdate(instance=patient)
                except Patient.DoesNotExist:
                        messages.error(self.request, "Paciente não encontrado. Faça o cadastro!")
        except Exception as e:
            messages.error(request, e.__str__())

        context['patients'] = Patient.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        try:
            form = PatientForm(request.POST)
            id = request.POST['id_patient']
           
            if (form.is_valid()):
                patient = Patient.objects.filter(id=id).update(
                    name = form.cleaned_data['name'],
                    birth_date = form.cleaned_data['birth_date'],
                    gender = form.cleaned_data['gender'],
                    cns = form.cleaned_data['cns'],
                    uf = form.cleaned_data['uf'],
                    city = form.cleaned_data['city'],
                    neighborhood = form.cleaned_data['neighborhood'],
                    street = form.cleaned_data['street'],
                    num = form.cleaned_data['num']


                )
                messages.success(request, 'Dados atualizados com sucesso!')
                query = f'?patient_data={id}'
                return redirect(reverse('editPatient') + query)
            else:
                query = f'?patient_data={id}'
                messages.error(request, 'Preencha os dados do paciente corretamente!')
                return redirect(reverse('editPatient') + query)

        except Exception as e:
            messages.error(request, e.__str__())

        return super().get(request, *args, **kwargs)

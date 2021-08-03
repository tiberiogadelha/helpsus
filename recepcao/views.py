import datetime
from django.http import request
from django.shortcuts import render
from django.views.generic.base import View
from .forms import PatientForm
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

class CreateAttendanceView(TemplateView):
    template_name = 'newAttendance.html'

    def get_context_data(self, **kwargs):
        context = super(CreateAttendanceView, self).get_context_data(**kwargs)
        try:
            if (self.request.POST):
                return
            if (self.request.GET.__contains__('patient_data')):
                if (self.request.GET['patient_data'] != 'patient_data'):
                    patient_id = self.request.GET['patient_data']
                    try:
                        patient = Patient.objects.filter(id=patient_id).first()
                        if (not(patient)):
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
            patient = Patient.objects.filter(id = patient_id).first()

            if (not(patient)):
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
            print(context)
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
        if (self.request.GET.__contains__('filter')):
            date = self.request.GET['filter']
            print(date)
            sql = f"SELECT * FROM core_attendance a WHERE a.created_at = '{date}'"
            attendances = Attendance.objects.raw(sql)
            context['attendances'] = attendances
        else:
            today = dateClass.today()
            sql = f"SELECT * FROM core_attendance WHERE created_at='{today}'"
            attendances = Attendance.objects.raw(sql)
            context['attendances'] = attendances

        return context
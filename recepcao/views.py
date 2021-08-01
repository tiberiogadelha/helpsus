from django.db.models.fields import DateTimeField
from django.http import request
from django.shortcuts import render
from .forms import PatientForm
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView 
from core.models import Attendance, Patient, FichaHandler


class PatientView(TemplateView):
    template_name = 'newPatient.html'

    def get_context_data(self, **kwargs):
        context = super(PatientView, self).get_context_data(**kwargs)
        context['form'] = PatientForm()
        return context
        
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        patient = PatientForm(request.POST)
        if (not(patient.is_valid())):
            messages.error(request, 'Preencha os dados do paciente corretamente!')
            
        
        patient.save()
        
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
            print('nesse')
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
            ##attendance = Attendance()
            ficha = FichaHandler()
            ficha.num = 0
            ficha.save()
            

            ##attendance.num = FichaHandler.numero_ficha
            ##print(FichaHandler.numero_ficha)
            
        except Patient.DoesNotExist:
            messages.error(request, 'Paciente não encontrado')
        except Exception as e:
            messages.error(request, e.__str__())
    
        return super().get(request, *args, **kwargs)
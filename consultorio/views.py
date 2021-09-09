from core.models import Attendance
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.

class IndexConsultorioView(LoginRequiredMixin, TemplateView):
    template_name = 'indexConsultorio.html'
    login_url = '/'
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class RequireExamView(LoginRequiredMixin, TemplateView):
    template_name = 'solicitarExameConsultorio.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(RequireExamView, self).get_context_data(**kwargs)
        
            
        sql = "SELECT * FROM core_attendance WHERE status ='consultorio' ORDER BY moment_consultorio"
        atendimentos = Attendance.objects.raw(sql)
        context['atendimentos'] = atendimentos

        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class RequireMedView(LoginRequiredMixin, TemplateView):
    template_name = 'solicitarMedicamentosConsultorio.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(RequireMedView, self).get_context_data(**kwargs)
        
            
        sql = "SELECT * FROM core_attendance WHERE status ='consultorio' ORDER BY moment_consultorio"
        atendimentos = Attendance.objects.raw(sql)
        context['atendimentos'] = atendimentos

        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class IssueSickNoteView(LoginRequiredMixin, TemplateView):
    template_name = 'emitirAtestado.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(IssueSickNoteView, self).get_context_data(**kwargs)
        
            
        sql = "SELECT * FROM core_attendance WHERE status ='consultorio' ORDER BY moment_consultorio"
        atendimentos = Attendance.objects.raw(sql)
        context['atendimentos'] = atendimentos

        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)



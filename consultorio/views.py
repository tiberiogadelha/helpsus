import json
from datetime import datetime

import pytz
from django.core.checks import messages

from core.models import Attendance, AttendanceQueue
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import TemplateView

from helpSUS.settings import TIME_ZONE
from triagem.util import calculate_age


class IndexConsultorioView(LoginRequiredMixin, TemplateView):
    template_name = 'indexConsultorio.html'
    login_url = '/'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PendingPacientsMedView(LoginRequiredMixin, TemplateView):
    template_name = 'visualizarAtendimentosConsultorio.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(PendingPacientsMedView, self).get_context_data(**kwargs)
        try:
            attendances_queue = AttendanceQueue.objects.first()
            attendances = []

            for pending_attendance in json.loads(attendances_queue.attendances):
                attendances.append(pending_attendance['id'])

            # if self.request.GET.get('filter'):
            #     date = self.request.GET['filter'].split('-')
            #     date1 = datetime(int(date[0]), int(date[1]), int(date[2]), 0, 0, 0)
            #     date1 = pytz.timezone(TIME_ZONE).localize(date1)
            #     date2 = datetime(int(date[0]), int(date[1]), int(date[2]), 23, 59, 59)
            #     date2 = pytz.timezone(TIME_ZONE).localize(date2)
            #
            #     attendances = attendances.objects.filter(
            #         created_at__gte=date1,
            #         created_at__lte=date2
            #     ).order_by('tria')

            context['attendances'] = Attendance.objects.filter(id__in=attendances).all()

            return context
        except Exception as e:
            print(e)
            return super().get_context_data(**kwargs)


class UpdateAttendanceMedView(LoginRequiredMixin, TemplateView):
    template_name = 'atualizarAtendimentoConsultorio.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(UpdateAttendanceMedView, self).get_context_data(**kwargs)
        try:
            id = self.request.GET.get('id')
            attendance = Attendance.objects.get(id=id)
            birth_date = attendance.patient.birth_date
            age = f'{calculate_age(birth_date)} anos'
            formated_date = attendance.patient.birth_date.strftime("%d/%m/%Y")
            attendance.patient.formated_date = f'{formated_date} - Idade: {age} anos'
            entrance = attendance.created_at.strftime("%d/%m/%Y")

            if attendance.status == 'aguardando':
                context["attendance"] = attendance
                entrance = f'{entrance} às {str(attendance.creation_hour)[:5]}'
                meta_data = {'age': age, 'entrance': entrance}
                context['meta'] = meta_data

           # form = TriagemForm() if (self.request.method == 'GET') else TriagemForm(self.request.POST)

        except Attendance.DoesNotExist:
            messages.error(request, 'Atendimento já realizado ou não encontrado.')
            return super().get(request, **kwargs)
        except Exception as e:
            if self.request.method == 'POST':
                form = TriagemForm(self.request.POST)
            else:
                form = TriagemForm()

            context['form'] = form
            return context
        context['form'] = form
        return context

class RequireExamView(LoginRequiredMixin, TemplateView):
    template_name = 'solicitarExameConsultorio.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(RequireExamView, self).get_context_data(**kwargs)

        attendances = Attendance.objects.filter(
            status='consultorio',
        ).order_by('-moment_consultorio')

        context['atendimentos'] = attendances

        return context


    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class RequireMedView(LoginRequiredMixin, TemplateView):
    template_name = 'solicitarMedicamentosConsultorio.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(RequireMedView, self).get_context_data(**kwargs)

        attendances = Attendance.objects.filter(
            status='consultorio',
        ).order_by('-moment_consultorio')

        context['atendimentos'] = attendances

        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class IssueSickNoteView(LoginRequiredMixin, TemplateView):
    template_name = 'emitirAtestado.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(IssueSickNoteView, self).get_context_data(**kwargs)

        attendances = Attendance.objects.filter(
            status='consultorio',
        ).order_by('-moment_consultorio')

        context['atendimentos'] = attendances

        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)



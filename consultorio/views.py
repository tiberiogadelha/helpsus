import json
import uuid
from datetime import datetime

import pytz
from dateutil.relativedelta import relativedelta
from django.core.files.base import ContentFile
from django.db import transaction
from django.db.models import Count
from django.http import request
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response

from consultorio.serializers import MedicationOrderSerializer, AttendanceHistorySerializer, PatientBasicSerializer, \
    TriagemSerializer
from consultorio.services import getAllPendingAttendances
from consultorio.util import mount_sick_note_pdf
from core.models import Attendance, AttendanceQueue, Patient, MedicationOrder, SickNote
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
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
        # try:
        #     id = self.request.GET.get('id')
        #     attendance = Attendance.objects.get(id=id)
        #     birth_date = attendance.patient.birth_date
        #     age = f'{calculate_age(birth_date)} anos'
        #     formated_date = attendance.patient.birth_date.strftime("%d/%m/%Y")
        #     attendance.patient.formated_date = f'{formated_date} - Idade: {age} anos'
        #     entrance = attendance.created_at.strftime("%d/%m/%Y")
        #
        #     if attendance.status == 'aguardando':
        #         context["attendance"] = attendance
        #         entrance = f'{entrance} às {str(attendance.creation_hour)[:5]}'
        #         meta_data = {'age': age, 'entrance': entrance}
        #         context['meta'] = meta_data

           # form = TriagemForm() if (self.request.method == 'GET') else TriagemForm(self.request.POST)

        # except Attendance.DoesNotExist:
        #     messages.error(request, 'Atendimento já realizado ou não encontrado.')
        #     return super().get(request, **kwargs)
        # except Exception as e:
        #     if self.request.method == 'POST':
        #         form = TriagemForm(self.request.POST)
        #     else:
        #         form = TriagemForm()
        #
        #     context['form'] = form
        #     return context
        # context['form'] = form
        return context



class ViewAttendanceDetails(LoginRequiredMixin, TemplateView):
    template_name = 'analisarAtendimentoConsultorio.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ViewAttendanceDetails, self).get_context_data(**kwargs)
        try:
            id = self.request.GET.get('id')
            attendance = Attendance.objects.get(pk=id)

            context['patient'] = PatientBasicSerializer(attendance.patient).data
            context['attendance'] = attendance
            context['triagem'] = TriagemSerializer(attendance.triage_reference).data
        except Attendance.DoesNotExist:
            messages.error(self.request, 'Atendimento já realizado ou não encontrado.')
            return context

        return context


class RequireExamView(LoginRequiredMixin, TemplateView):
    template_name = 'solicitarExameConsultorio.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(RequireExamView, self).get_context_data(**kwargs)
        try:
            if self.request.POST:
                return
            attendance_data = self.request.GET.get('attendance_data')
            if attendance_data and attendance_data != 'data':
                attendance = Attendance.objects.filter(
                    id=attendance_data, status='triagem'
                ).first()

                if attendance is None:
                    messages.error(self.request, "Atendimento finalizado ou inexistente!")
                    return

                context['attendanceData'] = attendance

        except Exception as e:
            messages.error(request, e.__str__())

        context['attendances'] = getAllPendingAttendances()
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class RequireMedView(LoginRequiredMixin, TemplateView):
    template_name = 'solicitarMedicamentosConsultorio.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(RequireMedView, self).get_context_data(**kwargs)
        try:
            if self.request.POST:
                return
            attendance_data = self.request.GET.get('attendance_data')
            if attendance_data and attendance_data != 'data':
                attendance = Attendance.objects.filter(
                    id=attendance_data, status='triagem'
                ).first()

                if attendance is None:
                    messages.error(self.request, "Atendimento finalizado ou inexistente!")
                    return

                context['attendanceData'] = attendance

        except Exception as e:
            messages.error(request, e.__str__())

        context['attendances'] = getAllPendingAttendances()
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        attendance_id = request.POST['attendance_id']
        attendance = Attendance.objects.filter(id=attendance_id).first()

        if attendance is None:
            messages.error(request, 'Atendimento não encontrado')
            return super().get(request, *args, **kwargs)

        order = MedicationOrder(
            order=request.POST['reqMed'],
            requested_by=request.user
        )

        order.save()

        attendance.medication_orders.add(order)

        messages.success(request, 'Medicação solicitada com sucesso!')
        return super().get(request, *args, **kwargs)


class RequireMedListView(LoginRequiredMixin, TemplateView):
    template_name = 'visualizarMedicamentosSolicitadosConsultorio.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(RequireMedListView, self).get_context_data(**kwargs)

        user = self.request.user

        medications_orders = MedicationOrder.objects.filter(
            requested_by=user.id
        ).order_by('-created_at')

        context['orders'] = MedicationOrderSerializer(medications_orders, many=True).data
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PatientHistoryView(LoginRequiredMixin, TemplateView):
    template_name = 'visualizarHistoricoPaciente.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(PatientHistoryView, self).get_context_data(**kwargs)
        patient_pk = self.request.GET.get('patient')
        try:
            patient = Patient.objects.get(pk=patient_pk)
        except:
            messages.error(self.request, "Paciente não encontrado!")
            return

        attendances = Attendance.objects.filter(patient=patient.pk).order_by('-created_at')

        context['attendances'] = AttendanceHistorySerializer(attendances, many=True).data
        context['patient'] = PatientBasicSerializer(patient).data

        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class IssueSickNoteView(LoginRequiredMixin, TemplateView):
    template_name = 'emitirAtestado.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(IssueSickNoteView, self).get_context_data(**kwargs)
        attendance_id = self.request.GET.get('attendance_id')

        attendances = Attendance.objects.alias(qty_notes=Count('sick_notes')).filter(
            status='triagem',
            qty_notes=0
        ).order_by('-moment_consultorio')

        context['attendances'] = attendances

        if attendance_id is not None:
            try:
                attendance = Attendance.objects.get(pk=attendance_id, status='triagem')
                context['attendance'] = attendance
                context['patient'] = attendance.patient
            except Attendance.DoesNotExist:
                pass

        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = request.POST
        user = request.user
        attendance = data['attendance_id']

        try:
            attendance = Attendance.objects.select_for_update(skip_locked=True).get(pk=attendance, status='triagem')
        except:
            messages.error(request, "Atendimento não encontrado!")
            return

        if attendance.sick_notes.count() > 1:
            messages.error(request, "Atendimento já possui atestado emitido!")
            return

        days = int(data['days'])
        if days < 1:
            messages.error(request, "Quantidade de dias inválida!")
            return

        sick_note = SickNote(
            quantity_days=int(days),
            requested_by=user
        )
        sick_note.save()

        attendance_date = attendance.created_at.strftime('%d/%m/%Y às %H:%M')
        util = (attendance.created_at + relativedelta(days=days-1)).strftime('%d/%m/%Y às %H:%M')
        pdf_data = mount_sick_note_pdf(
            sick_note.id, attendance, user, days, data['days_text'], data['cid'], attendance_date, util
        )
        sick_note.document.save(str(uuid.uuid4()) + '.pdf', ContentFile(pdf_data))
        sick_note.save()

        attendance.sick_notes.add(sick_note)

        messages.success(request, 'Atestado emitido com sucesso!')
        return redirect('viewAttendances')



@api_view(['GET'])
def get_med_order_details(_, order_id):
    try:
        med_order = MedicationOrder.objects.get(pk=order_id)

        data = {
            'order': med_order.order
        }

        return Response(data, status=200)
    except:
        return Response(data={}, status=404)


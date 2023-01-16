import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render
from django.views.generic import TemplateView

from consultorio.serializers import ExamOrderSerializer
from core.models import ExamInstance, ExamOrder, Attendance
from helpSUS.settings import TIME_ZONE


class IndexLaboratorio(LoginRequiredMixin, TemplateView):
    template_name = 'indexLaboratorio.html'
    login_url = '/'



class CreateExamView(LoginRequiredMixin, TemplateView):
    template_name = 'cadastrarExameLab.html'
    login_url = '/'

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        label = request.POST['label']
        description = request.POST['description']

        exam = ExamInstance(
            label=label,
            description=description
        )

        try:
            exam.save()
        except:
            messages.error(request, 'Erro ao salvar o exame. Verifique se não existe outro cadastrado!')
            return super().get(request, *args, **kwargs)

        messages.success(request, 'Exame cadastrado com sucesso!')
        return super().get(request, *args, **kwargs)


class HandleExamView(LoginRequiredMixin, TemplateView):
    template_name = 'viewExamesLab.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(HandleExamView, self).get_context_data(**kwargs)

        exams = ExamInstance.objects.all().order_by('label')
        context['exams'] = exams
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        exam_id = request.POST['examId']

        try:
            exam = ExamInstance.objects.select_for_update(skip_locked=True).get(pk=exam_id)
            exam.active = not exam.active
            exam.save()
        except ExamInstance.DoesNotExist:
            messages.error(request, 'Exame não encontrado!')
            return

        messages.success(request, 'Exame atualizado com sucesso!')
        return super().get(request, *args, **kwargs)


class PendingExamView(LoginRequiredMixin, TemplateView):
    template_name = 'ordensExamesPendentes.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(PendingExamView, self).get_context_data(**kwargs)

        exams = ExamOrder.objects.filter(status='0').order_by('created_at')
        context['exams'] = ExamOrderSerializer(exams, many=True).data
        return context


class ConfirmExamView(LoginRequiredMixin, TemplateView):
    template_name = 'updateExamOrder.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ConfirmExamView, self).get_context_data(**kwargs)

        if self.request.method == 'GET':
            id = self.request.GET.get('id')
        else:
            id = self.request.POST['id']

        try:
            exam = ExamOrder.objects.get(pk=id)
            context['exam'] = ExamOrderSerializer(exam).data
        except:
            messages.error(self.request, 'Ordem não encontrada!')
            return context

        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        exam_id = request.POST['id']

        try:
            exam = ExamOrder.objects.select_for_update(skip_locked=True).get(pk=exam_id, status=0)
            exam.status = 1
            exam.was_released = True
            exam.released_by = request.user
            exam.released_at = datetime.datetime.now()
            exam.save()
        except Exception as e:
            print(e)
            messages.error(request, 'Ordem exame não encontrada ou já finalizada!')
            return super().get(request, *args, **kwargs)

        messages.success(request, 'Ordem exame atualizada com sucesso!')
        return super().get(request, *args, **kwargs)


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from core.models import ExamInstance


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


import datetime

import pytz
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
from django.shortcuts import render
from django.views.generic.base import View

from consultorio.serializers import MedicationOrderSerializer
from helpSUS.settings import TIME_ZONE

from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView
from core.models import Attendance, Patient, MedicationOrder

from datetime import date as dateClass


class IndexPharmacy(LoginRequiredMixin, TemplateView):
    template_name = 'indexPharmacy.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(IndexPharmacy, self).get_context_data(**kwargs)
        context['user_name'] = self.request.user.first_name
        return context


class GetPendingOrdersPharmacy(LoginRequiredMixin, TemplateView):
    template_name = 'indexPharmacy.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(GetPendingOrdersPharmacy, self).get_context_data(**kwargs)
        pending_orders = MedicationOrder.objects.filter(status=0).order_by('created_at')

        context['orders_data'] = MedicationOrderSerializer(pending_orders, many=True).data
        return context


class GetFinishedOrdersPharmacy(LoginRequiredMixin, TemplateView):
    template_name = 'indexPharmacy.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(GetFinishedOrdersPharmacy, self).get_context_data(**kwargs)
        finished_orders = MedicationOrder.objects.filter(status__in=[1, 2]).order_by('-created_at')

        context['orders_data'] = MedicationOrderSerializer(finished_orders, many=True).data
        return context


class HandleMedicationOrderPharmacy(LoginRequiredMixin, TemplateView):
    template_name = 'updateMedicationOrder.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(HandleMedicationOrderPharmacy, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            order_id = self.request.POST.get('order_id')
        else:
            order_id = context.get('order')

        try:
            order = MedicationOrder.objects.get(pk=order_id)
        except MedicationOrder.DoesNotExist:
            messages.error(self.request, 'Requisição não encontrada ou já finalizada')
            return

        context['order'] = MedicationOrderSerializer(order).data
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        order_id = request.POST.get('order_id')

        try:
            order = MedicationOrder.objects.select_for_update(skip_locked=True).get(pk=order_id, status=0)
        except MedicationOrder.DoesNotExist:
            messages.error(request, 'Requisição não encontrada ou já finalizada')
            return super().get(request, **kwargs)

        if action not in ['liberar', 'rejeitar']:
            messages.error(request, 'Ação inválida!')
            return super().get(request, **kwargs)

        user = request.user

        if action == 'liberar':
            status = 1
        else:
            status = 2

        order.released_by = user
        order.status = status
        order.released_at = datetime.datetime.now()
        order.save()

        messages.success(request, 'O status da medicação foi atualizado!')
        return super().get(request, *args, **kwargs)





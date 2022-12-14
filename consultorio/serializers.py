from datetime import datetime

from rest_framework import serializers

from core.models import MedicationOrder, Attendance
from dateutil.relativedelta import relativedelta

class MedicationOrderSerializer(serializers.ModelSerializer):
    attendance = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)
    released_at = serializers.SerializerMethodField(read_only=True)

    def get_attendance(self, instance):
        attendance = Attendance.objects.get(medication_orders=instance.pk)

        return {
            'num': attendance.num,
            'status': attendance.status,
            'patient': {
                'name': attendance.patient.name,
                'birth_date': attendance.patient.birth_date.strftime('%d/%m/%Y'),
                'age': relativedelta(datetime.now(), attendance.patient.birth_date).years,
                'gender': attendance.patient.gender
            }
        }

    def get_status(self, instance):
        if instance.status == 0:
            return 'Pendente'
        elif instance.status == 1:
            return 'Liberada'
        return 'Recusada'

    def get_created_at(self, instance):
        return instance.created_at.strftime('%d/%m/%Y às %H:%m')

    def get_released_at(self, instance):
        if instance.released_at is None:
            return None
        return instance.released_at.strftime('%d/%m/%Y às %H:%m')

    class Meta:
        model = MedicationOrder
        fields = ['id', 'order', 'attendance', 'status', 'created_at', 'released_at']
from datetime import datetime

from rest_framework import serializers

from core.models import MedicationOrder, Attendance, Triagem, VitalData, ExamOrder, Patient, ExamInstance
from dateutil.relativedelta import relativedelta

from triagem.util import calculate_age


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


class MedicationOrderBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicationOrder
        fields = ['order']


class ExamOrderBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamOrder
        fields = ['order']


class VitalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalData
        fields = ['temperature', 'pas', 'pad', 'saturation', 'heart_beats']


class TriagemSerializer(serializers.ModelSerializer):
    vital_data = VitalDataSerializer(read_only=True)
    priority = serializers.SerializerMethodField(read_only=True)

    def get_priority(self, obj):
        priority = str(obj.priority)
        if priority == '0':
            return 'Normal'
        elif priority == '1':
            return 'Moderada'
        return 'Alta'

    class Meta:
        model = Triagem
        fields = ['vital_data', 'priority', 'description']


class AttendanceHistorySerializer(serializers.ModelSerializer):
    triage_reference = TriagemSerializer(read_only=True)
    medication_orders = MedicationOrderBasicSerializer(many=True, read_only=True)
    exams_orders = ExamOrderBasicSerializer(many=True, read_only=True)
    had_sick_note = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField(read_only=True)

    def get_had_sick_note(self, obj):
        return 'Sim' if obj.sick_notes.count() > 0 else 'Não'

    def get_created_at(self, obj):
        return obj.created_at.strftime('%d/%m/%Y às %H:%M')

    class Meta:
        model = Attendance
        fields = [
            'num', 'status', 'triage_reference', 'created_at', 'had_sick_note', 'medication_orders', 'exams_orders',
            'medication_orders'
        ]


class PatientBasicSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField(read_only=True)
    birth_date = serializers.SerializerMethodField(read_only=True)

    def get_age(self, obj):
        return calculate_age(obj.birth_date)

    def get_birth_date(self, obj):
        return obj.birth_date.strftime('%d/%m/%Y')

    class Meta:
        model = Patient
        fields = ['name', 'gender', 'age', 'cns', 'id', 'birth_date']


class ExamInstanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExamInstance
        fields = ['label', 'description']


class ExamOrderSerializer(serializers.ModelSerializer):
    attendance = serializers.SerializerMethodField(read_only=True)
    patient = serializers.SerializerMethodField(read_only=True)
    exams = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)
    order_details = serializers.SerializerMethodField(read_only=True)
    order_details_req = serializers.SerializerMethodField(read_only=True)
    released_at = serializers.SerializerMethodField(read_only=True)

    def get_attendance(self, obj):
        attendance = Attendance.objects.get(exams_orders=obj.pk)
        return AttendanceHistorySerializer(attendance).data

    def get_patient(self, obj):
        attendance = Attendance.objects.get(exams_orders=obj.pk)
        return PatientBasicSerializer(attendance.patient).data

    def get_status(self, obj):
        if str(obj.status) == '0':
            return 'Pendente'
        return 'Liberado'

    def get_created_at(self, obj):
        return obj.created_at.strftime('%d/%m/%Y às %H:%M')

    def get_released_at(self, obj):
        return '--' if obj.released_at is None else obj.released_at.strftime('%d/%m/%Y às %H:%M')

    def get_exams(self, obj):
        return ExamInstanceSerializer(obj.exams, many=True).data

    def get_order_details(self, obj):
        order_details = ''
        for index, exam in enumerate(obj.exams.all()):
            if index != obj.exams.count() - 1:
                order_details = order_details + f'{exam.label}, '
            else:
                order_details = order_details + f'{exam.label}'
        return order_details

    def get_order_details_req(self, obj):
        order_details = ''
        for index, exam in enumerate(obj.exams.all()):
            if index != obj.exams.count() - 1:
                order_details = order_details + f'{exam.label}, \n'
            else:
                order_details = order_details + f'{exam.label}'
        return order_details

    class Meta:
        model = ExamOrder
        fields = [
            'id', 'created_at', 'attendance', 'patient', 'order', 'status', 'exams', 'order_details',
            'order_details_req', 'released_at'
        ]

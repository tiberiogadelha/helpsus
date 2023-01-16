from rest_framework import serializers

from core.models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = '__all__'

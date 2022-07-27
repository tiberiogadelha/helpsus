import json

from core.models import AttendanceQueue, Attendance


def getAllPendingAttendances():
    raw_attendandes = AttendanceQueue.objects.first().attendances
    attendances_id = [int(entity['id']) for entity in json.loads(raw_attendandes)]

    attendances = Attendance.objects.filter(
        pk__in=attendances_id
    )

    return attendances
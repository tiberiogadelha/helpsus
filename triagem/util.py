from datetime import datetime

from dateutil.relativedelta import relativedelta

from core.models import AttendanceQueue, Triagem, VitalData, Attendance
import json

from recepcao.util import Util
from triagem.serializers import AttendanceSerializer


def calculate_age(birth_date):
    return int(relativedelta(datetime.now(), birth_date).years)


def insert_attendance(new_attendance, queue):


    index = 0
    inserted = False
    serialized = AttendanceSerializer(new_attendance).data
    actual_queue = queue

    while not inserted and index < len(actual_queue):
        attendance = actual_queue[index]
        attendance = Attendance.objects.get(pk=attendance['id'])
        triagem = attendance

        if int(new_attendance.priority) > int(triagem.priority):
            WAITING_LIMIT = 0 if triagem.priority == 2 else (1 if (triagem.priority == 1) else 3)
            diff_time = Util.agora() - triagem.created_at
            converted_to_hour = (diff_time.days * 24) + (diff_time.seconds/60)
            if converted_to_hour < WAITING_LIMIT:
                inserted = True
                actual_queue.insert(index, serialized)
        index += 1
    
    if not inserted:
        actual_queue.append(serialized)

    return json.dumps(actual_queue)


def allocate_patient(attendance):
    try:
        attendance_queue = AttendanceQueue.objects.select_for_update().first()
        queue = json.loads(attendance_queue.attendances)
        new_queue = insert_attendance(attendance, queue)
        attendance_queue.attendances = new_queue
        attendance_queue.save()
        return "Ok"
    except Exception as e:
        raise Exception(e.__str__())

def extract_vital_data(form): 
    vital_data = VitalData()
    vital_data.temperature = form.cleaned_data['temperature']
    vital_data.pas = form.cleaned_data['pas']
    vital_data.pad = form.cleaned_data['pad']
    vital_data.saturation = form.cleaned_data['saturation']
    vital_data.heart_beats = form.cleaned_data['heart_beats']

    return vital_data


def extract_triagem_data(form):
    triagem = Triagem()
    triagem.description = form.cleaned_data['description']
    triagem.priority = form.cleaned_data['priority']

    return triagem
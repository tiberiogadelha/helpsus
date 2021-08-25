from datetime import date
from core.models import AttendanceQueue, Triagem, VitalData
import json
import datetime

def calculate_age(birth_date):
    today = date.today()
    diff_in_days = today - birth_date
    DAYS_IN_YEAR = 365
    age = diff_in_days.days/DAYS_IN_YEAR
    return int(age)

def insert_attendance(new_attendance, queue):
    MAX_PRIORITY = 2
    MEDIUM_PRIORITY = 1
    NORMAL_PRIORITY = 0
    MIN_WAITING = 0
    MEDIUM_WAITING = 1
    MAX_WAITING = 3

    WAITING_LIMIT = MIN_WAITING if (new_attendance.priority == MAX_PRIORITY) else (MEDIUM_WAITING if (new_attendance.priority == MEDIUM_PRIORITY) else MAX_WAITING)
    index = 0
    inserted = False
    serialized = json.dumps(new_attendance)
    while (not(inserted) and index < len(queue)):
        attendance = json.loads(queue[index])
        if (new_attendance.priority > attendance['priority']):
            attendance_time = attendance['created_at']
            WAITING_LIMIT = 0 if (attendance['priority'] == 2) else (1 if (attendance['priority'] == 1) else 3)
            diff_time = datetime.datetime.now() - attendance_time
            converted_to_hour = (diff_time.days * 24) + (diff_time.seconds/60)
            if (converted_to_hour < WAITING_LIMIT):
                inserted = True
                queue.insert(index, serialized)
        index += 1
    
    if (not(inserted)):
        queue.append(serialized)

    return queue


def alocate_patient(attendance):
    try:
        data = AttendanceQueue.objects.first()
        queue = json.loads(data.attendances)
        new_queue = insert_attendance(attendance, queue)
        serialized = json.dumps(new_queue)
        data.attendances = serialized
        data.save()
        return "Ok"
    except Exception as e:
        return e.__str__()

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
from datetime import date
from core.models import AttendanceQueue, Triagem, VitalData
import json
import datetime
from django.forms.models import model_to_dict

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
    print(new_attendance)
    WAITING_LIMIT = MIN_WAITING if (int(new_attendance.priority) == MAX_PRIORITY) else (MEDIUM_WAITING if (int(new_attendance.priority) == MEDIUM_PRIORITY) else MAX_WAITING)
    index = 0
    inserted = False
    serialized = model_to_dict(new_attendance)
    testing = json.loads(queue["pacientes"])
    actual_queue = json.loads(testing)
    print(len(actual_queue))
    while (not(inserted) and index < len(actual_queue)):
        attendance = json.loads(actual_queue[index])
        if (new_attendance.priority > int(attendance['priority'])):
            attendance_time = attendance['created_at']
            print(attendance_time)
            WAITING_LIMIT = 0 if (attendance['priority'] == 2) else (1 if (attendance['priority'] == 1) else 3)
            diff_time = datetime.datetime.now() - attendance_time
            converted_to_hour = (diff_time.days * 24) + (diff_time.seconds/60)
            if (converted_to_hour < WAITING_LIMIT):
                inserted = True
                actual_queue.insert(index, serialized)
        index += 1
    
    if (not(inserted)):
        actual_queue.append(serialized)
    queue['pacientes'] = json.dumps(str(actual_queue))
    return json.dumps(queue)


def alocate_patient(attendance):
    try:
        data = AttendanceQueue.objects.first()
        print(data)
        queue = json.loads(data.attendances)
        print(queue)
        new_queue = insert_attendance(attendance, queue)
        print(new_queue)
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
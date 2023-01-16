from core.models import Patient, Attendance, ExamOrder, MedicationOrder, SickNote, Employee

roles_department = {
    'biom': ['laboratorio'],
    'bioq': ['laboratorio'],
    'enf': ['triagem'],
    'med': ['consultorio'],
    'dig': ['recepcao', 'laboratorio'],
    'rec': ['recepcao'],
    'tec': ['laboratorio'],
    'coord': ['all'],
    'dir': ['all'] 
}

class Validate:
    def validateUserDepartment(self, user, department):
        try:
            if user.role.cod == 'coord' or user.role.cod == 'dir':
                return True
            return department in roles_department[user.role.cod]
        except:
            return False


def mount_default_dashboard_info():
    qty_patients = Patient.objects.only('pk').count()
    qty_finished_attendance = Attendance.objects.only('pk', 'status').filter(status='encerrado').count()
    qty_exams_orders = ExamOrder.objects.only('pk').count()
    qty_medications_orders = MedicationOrder.objects.only('pk').count()
    qty_sick_notes = SickNote.objects.only('pk').count()
    qty_employees = Employee.objects.only('pk', 'is_enabled').filter(is_enabled=True).count()

    return {
        'qty_total_patients': qty_patients,
        'qty_total_finished_attendance': qty_finished_attendance,
        'qty_total_exams_orders': qty_exams_orders,
        'qty_total_medications_orders': qty_medications_orders,
        'qty_total_sick_notes': qty_sick_notes,
        'qty_total_employees': qty_employees
    }



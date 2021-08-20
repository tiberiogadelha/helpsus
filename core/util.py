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
            if(user.role.cod == 'coord' or user.role.cod == 'dir'):
                return True
            return department in roles_department[user.role.cod]
        except:
            return False

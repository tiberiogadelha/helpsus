import enum
import uuid
from datetime import datetime

import jsonfield
from dateutil.relativedelta import relativedelta
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.forms import JSONField
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db.models import signals
from queue import PriorityQueue
import json


GENDER_CHOICES = (
        ('f', 'Feminino'),
        ('m', 'Masculino'),
        ('o', 'Outro')
    )

class Base(models.Model):
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        abstract = True


class FichaHandler(models.Model):
    num = models.IntegerField('Nº Ficha')
    

class User(Base):
    GENDER_CHOICES = (
        ('f', 'Feminino'),
        ('m', 'Masculino'),
        ('o', 'Outro')
    )
    name = models.CharField('Nome', max_length=140)
    email = models.EmailField('Email', max_length=120)
    password = models.CharField('Senha', max_length=300, default='23232')
    re_password = models.CharField('Confirmação da senha', max_length=300, default='')
    birth_date = models.DateField('Birth Date')
    gender = models.CharField('Sexo', max_length=1, choices=GENDER_CHOICES)
    is_enabled = models.BooleanField('Está habilitado', default=False)
    role = models.ForeignKey('core.Role', verbose_name='Cargo', on_delete=models.CASCADE)
    conselho = models.CharField('Conselho', max_length=120, default=0)
    #slug = models.SlugField('Slug', max_length=100, blank=True, editable=False)

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
    
    def __str__(self):
        return f'{self.name} - {self.role}'


'''
Realiza função antes de inserir
'''
#def user_pre_save(signal, instance, sender, **kwargs):
#    instance.slug = slugify(instance.name)
#signals.pre_save.connect(user_pre_save, sender=User)

class Patient(Base):
    name = models.CharField('Nome', max_length=140)
    birth_date = models.DateField('Data de nascimento')
    gender = models.CharField('Sexo', max_length=1, choices=GENDER_CHOICES)
    cns = models.CharField('CNS', max_length=20, blank=True)
    cpf = models.CharField('CPF', max_length=11, blank=True)
    uf_select = (("AC","Acre"), ("AL", "Alagoas"), ("AM", "Amazonas"), ("AP", "Amapá"), ("BA", "Bahia"), ("CE", "Ceará"), ("DF", "Distrito Federal"), ("ES", "Espirito Santo"), ("GO", "Goiás"), ("MA", "Maranhão"), ("MT", "Mato Grosso"), ("MS", "Mato Grosso do Sul"), ("MG", "Minas Gerais"), ("PA", "Pará"), ("PB", "Paraíba"), ("PR", "Paraná"), ("PE", "Pernambuco"), ("PI", "Piauí"), ("RJ", "Rio de Janeiro"), ("RN", "Rio Grande do Norte"), ("RO", "Roraima"), ("RS", "Rio Grande do Sul"), ("RR", "Roraima"), ("SC", "Santa Catarina"), ("SE", "Sergipe"), ("SP", "São Paulo"), ("TO", "Tocantins"))
    city = models.CharField('Cidade', max_length=60, default='Campina Grande')
    uf = models.CharField('Estado', max_length=2, choices=uf_select, default='PB')
    street = models.CharField('Rua', max_length=150)
    neighborhood = models.CharField('Bairro', max_length=70)
    num = models.CharField('Número', max_length=10)
 
    class Meta:
        verbose_name = 'paciente'
        verbose_name_plural = 'Pacientes'
    
    def __str__(self):
        date = self.birth_date.strftime('%d/%m/%Y')
        return f'{self.name} - CNS: {self.cns} - Data de nascimento: {date}'

    
class Role(models.Model):
    ROLES = (
        ('biom', 'Biomédico/Biomédica'),
        ('bioq', 'Bioquímico/Bioquímica'),
        ('enf', 'Enfermeiro/Enfermeira'),
        ('med', 'Médico/Médica'),
        ('dig', 'Digitador/Digitadora'),
        ('rec', 'Recepcionista'),
        ('farm', 'Farmacêutico/Farmacêutica'),
        ('tec', 'Técnico'),
        ('coord', 'Coordenador/Coordenadora'),
        ('dir', 'Diretor/Diretora')
    )
    cod = models.CharField('Código', max_length=20, choices=ROLES)
    name = models.CharField('Masculino', max_length=150)
    f_name = models.CharField('Feminino', max_length=150)
    
    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
    
    def __str__(self):
        if (self.name == self.f_name):
            return self.name
        return f'{self.name}/{self.f_name}'


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if (not email):
            raise ValueError('Invalid email')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_enabled', True)

        return self._create_user(email, password, **extra_fields)


class Employee(AbstractUser):
    email = models.EmailField('Email', unique=True)
    first_name = models.CharField('Primeiro nome', max_length=50)
    last_name = models.CharField('Sobrenomes', max_length=250)
    birth_date = models.DateField('Data de nascimento')
    gender = models.CharField('Sexo', max_length=1, choices=GENDER_CHOICES, default='o')
    is_enabled = models.BooleanField('Está habilitado', default=False)
    role = models.ForeignKey(
        Role, 
        verbose_name='Cargo', 
        null=True, 
        on_delete=models.CASCADE
    )
    conselho = models.CharField('Conselho', max_length=120, null=True, blank=True)
    created_at = models.DateField('Created at', auto_now_add=True)
    updated_at = models.DateField('Updated at', auto_now=True)
    reqPwd = models.DateField('Solicitação recuperação de senha', auto_now_add=True)
    pwdTries = models.IntegerField('Tentativas de senha', default=0)
    pwdUrl = models.CharField('URL senha', default='none', max_length=150)
    code = models.IntegerField('Código', default=0)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birth_date', 'gender']
    objects = UserManager()

    def __str__(self) -> str:
        string = f'{self.first_name} {self.last_name} - {self.role}:{self.conselho}'
        return string

    def getCarimbo(self, employee):
        if employee.gender == 'm':
            string = f'{employee.first_name} {employee.last_name} - {employee.role.name}/{employee.conselho}'
        else:
            string = f'{employee.first_name} {employee.last_name} - {employee.role.f_name}/{employee.conselho}'
        return string

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'

class VitalData(Base):
    temperature = models.FloatField('Temperatura corporal', null=False, blank=False)
    pas = models.IntegerField('Pressão sistólica', null=False, blank=False)
    pad = models.IntegerField('Pressão diástolica', null=False, blank=False)
    saturation = models.IntegerField('Saturação', null=False, blank=False)
    heart_beats = models.IntegerField('Batimentos', null=False, blank=False)

    def __str__(self) -> str:
        string = f'Dados vitais({self.id}) - Temperatura: {self.temperature}°C, Pressão: sistólica {self.pas} mmHg, diastólica {self.pad} mmHg, Saturação: {self.saturation}%, Batimentos: {self.heart_beats}'
        return string

    class Meta:
        verbose_name = 'Dados vitais'
        verbose_name_plural = 'Dados vitais'

    
class Triagem(Base):
    priority_enum = (
        (0, 'Normal'),
        (1, 'Moderada'),
        (2, 'Alta')
    )
    responsible = models.ForeignKey(
        Employee,
        on_delete=models.deletion.PROTECT,
        blank=False,
        null=False,
        related_name='responsavem_triagem'
    )
    vital_data = models.ForeignKey(
        VitalData,
        on_delete=models.deletion.PROTECT,
        blank=False,
        null=False,
        related_name="Vitais",
    )
    priority = models.IntegerField('Prioridade', default=1, blank=False, null=False, choices=priority_enum)
    description = models.TextField('Descrição dos sintomas', blank=False, null=False, max_length=800, default="")

    def __str__(self):
        employee = Employee()
        carimbo = employee.getCarimbo(self.responsible)
        string = f'Triagem({self.id}) - Prioridade: {self.priority}, Responsável:{carimbo}'
        return string

    class Meta:
        verbose_name = 'Triagem'
        verbose_name_plural = 'Triagens'


def get_default_queue():
    return {"attendances": []}


class AttendanceQueue(models.Model):
    attendances = jsonfield.JSONField(blank=True, default=json.dumps([]))

    def __str__(self) -> str:
        attendances = json.loads(self.attendances)
        result = []
        for attendance in attendances:
            result.append(f'Atendimento {attendance["num"]}')

        return ' '.join(result)


class MedicationOrder(Base):
    status_enum = (
        (0, 'Pendente'),
        (1, 'Liberado'),
        (2, 'Recusado')
    )

    id = models.CharField('Identificador', max_length=100, primary_key=True,  default=uuid.uuid4)
    requested_by = models.ForeignKey(Employee, blank=False, null=False, on_delete=models.deletion.PROTECT,
                                     related_name='solicitante_medicacao')
    released_by = models.ForeignKey(Employee, blank=True, null=True, on_delete=models.deletion.PROTECT,
                                    related_name='responsavel_medicacao')
    order = models.TextField('Solicitação', max_length=5000, null=False, blank=False)
    was_released = models.BooleanField(default=False)
    status = models.IntegerField('Status', default=0, choices=status_enum)
    released_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Solicitação de medicamento'
        verbose_name_plural = 'Solicitações de medicamento'


class ExamInstance(Base):
    label = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    active = models.BooleanField(default=True)


class ExamOrder(Base):
    status_enum = (
        (0, 'Pendente'),
        (1, 'Liberado')
    )

    id = models.CharField('Identificador', max_length=100, primary_key=True, default=uuid.uuid4)
    requested_by = models.ForeignKey(Employee, blank=False, null=False, on_delete=models.deletion.PROTECT,
                                     related_name='solicitante_exame')
    released_by = models.ForeignKey(Employee, blank=True, null=True, on_delete=models.deletion.PROTECT,
                                    related_name='responsavel_exame')
    order = models.TextField('Solicitação', max_length=5000, null=False, blank=False)
    was_released = models.BooleanField(default=False)
    status = models.IntegerField('Status', default=0, choices=status_enum)
    exams = models.ManyToManyField(ExamInstance)
    released_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Solicitação de exame'
        verbose_name_plural = 'Solicitações de exames'


class SickNote(Base):
    id = models.CharField('Identificador', max_length=100, primary_key=True, default=uuid.uuid4)
    requested_by = models.ForeignKey(Employee, on_delete=models.deletion.PROTECT, related_name='requisitante_atestado')
    document = models.FileField('Atestado', null=True, blank=True)
    quantity_days = models.IntegerField()

    def get_expiration(self):
        return self.created_at + relativedelta(days=self.quantity_days-1)

    class Meta:
        verbose_name = 'Atestado'
        verbose_name_plural = 'Atestados'


class Attendance(Base):
    enum_status = (
        ('aguardando', 'Aguardando atendimento'),
        ('triagem', 'Triado'),
        ('consultorio', 'Consultado'),
        ('encerrado', 'Encerrado')

    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='Paciente'
    )
    num = models.IntegerField('Número atendimento', default=0, blank=False, null=False)
    status = models.CharField('Status', default='aguardando', choices=enum_status, max_length=30)
    moment_triagem = models.DateTimeField('Momento da triagem', blank=True, null=True)
    sign_attendance = models.TextField('Assinatura atendimento', max_length=900, default='')
    moment_consultorio = models.DateTimeField('Momento da consulta', blank=True, null=True)
    moment_encerramento = models.DateTimeField('Momento do encerramento', blank=True, null=True)
    attended_by = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.PROTECT, related_name='MedicoResponsavel')
    creation_hour = models.TimeField('Hora da criação', blank=False, default=datetime.time(datetime.now()))
    priority = models.IntegerField('Prioridade', default=0)

    triage_reference = models.ForeignKey(
        Triagem,
        on_delete=models.deletion.PROTECT,
        blank=True,
        null=True,
        related_name='Triagem'
    )

    medication_orders = models.ManyToManyField(
        MedicationOrder, related_name='medicamentos', blank=True
    )

    exams_orders = models.ManyToManyField(
        ExamOrder, related_name='exames', blank=True
    )

    sick_notes = models.ManyToManyField(
        SickNote, related_name='atestados', blank=True
    )

    def __str__(self):
        formated_date = self.created_at.strftime('%d/%m/%Y')
        return f'Atendimento ({self.num}): Paciente {self.patient} - Status {self.status} - Data {formated_date} às {str(self.creation_hour)[:5]}'
    
    def __lt__(self, other):
        if isinstance(other, Attendance):
            if self.created_at < other.created_at:
                return True
            elif self.created_at == other.created_at:
                return self.creation_hour <= other.creation_hour
            return False
        else:
            raise('invalid comparation')

    def finish_attendance(self, sign_attendance, attended_by):
        self.moment_encerramento = datetime.now()
        self.sign_attendance = sign_attendance
        self.attended_by = attended_by
        self.status = 'encerrado'
        self.save()


    class Meta:
        verbose_name = 'Atendimento'
        verbose_name_plural = 'Atendimentos'




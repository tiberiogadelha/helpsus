from datetime import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db.models import signals
from queue import PriorityQueue


# Create your models here.

GENDER_CHOICES = (
        ('f', 'Feminino'),
        ('m', 'Masculino'),
        ('o', 'Outro')
    )

class Base(models.Model):
    created_at = models.DateField('Created at', auto_now_add=True)
    updated_at = models.DateField('Updated at', auto_now=True)

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

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'

    
        

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
    moment_consultorio = models.DateTimeField('Momento da consulta', blank=True, null=True)
    moment_encerramento = models.DateTimeField('Momento do encerramento', blank=True, null=True)
    creation_hour = models.TimeField('Hora da criação', blank=False, default=datetime.time(datetime.now()))
    def __str__(self):
        formated_date = self.created_at.strftime('%d/%m/%Y')
        return f'Atendimento ({self.num}): Paciente {self.patient} - Status {self.status} - Data {formated_date} às {str(self.creation_hour)[:5]}'
    
    def __lt__(self, other):
        if isinstance(other, Attendance):
            if (self.created_at < other.created_at):
                return True
            elif (self.created_at == other.created_at):
                return self.creation_hour <= other.creation_hour
            return False
        else:
            raise('invalid comparation')

    class Meta:
        verbose_name = 'Atendimento'
        verbose_name_plural = 'Atendimentos'

        
class VitalData(Base):
    temperature = models.FloatField('Temperatura corporal', null=False, blank=False)
    pas = models.IntegerField('Pressão sistólica', null=False, blank=False)
    pad = models.IntegerField('Pressão diástolica', null=False, blank=False)
    saturation = models.IntegerField('Saturação', null=False, blank=False)
    heart_beats = models.IntegerField('Batimentos', null=False, blank=False)

class Triagem(Base):
    setor_enum = (
        ('azul', 'Ala Azul'),
        ('verde', 'Ala Verde'),
        ('amarela', 'Ala Amarela'),
        ('vermelha', 'Ala Vermelha')
    )
    attendance = models.ForeignKey(
        Attendance,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='Atendimento'
    )
    responsible = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='Responsável'
    )
    vital_data = models.ForeignKey(
        VitalData,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name= "Vitais",
    )
    department = models.CharField('Ala', default= 'azul', blank=False, null=False, max_length=30) 
    description = models.TextField('Descrição dos sintomas', blank=False, null=False, max_length=800)

    

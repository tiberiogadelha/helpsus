#from typing_extensions import Required
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
#from django.db.models import signals
#from django.template.defaultfilters import date, slugify

# Create your models here.

class Base(models.Model):
    created_at = models.DateField('Created at', auto_now_add=True)
    updated_at = models.DateField('Updated at', auto_now=True)

    class Meta:
        abstract = True

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
    GENDER_CHOICES = (
        ('f', 'Feminino'),
        ('m', 'Masculino'),
        ('o', 'Outro')
    )
    name = models.CharField('Nome', max_length=140)
    birth_date = models.DateField('Data de nascimento')
    gender = models.CharField('Sexo', max_length=1, choices=GENDER_CHOICES)
    cns = models.CharField('CNS', max_length=20)
    cpf = models.CharField('CPF', max_length=11)
    adress = models.CharField('Endereço', max_length=200, default='')

    class Meta:
        verbose_name = 'Paciente',
        verbose_name_plural = 'Pacientes'
    
    def __str__(self):
        return f'{self.name} - {self.birth_date}'


    
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
        verbose_name = 'Cargo',
        verbose_name_plural = 'Cargos'
    
    def __str__(self):
        if (self.name == self.f_name):
            return self.name
        return f'{self.name}/{self.f_name}'

class UsuarioManager(BaseUserManager):
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
        return self.cre

class UsuarioCustom(AbstractUser):
    email = models.EmailField('Email', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']
    objects = UsuarioManager()
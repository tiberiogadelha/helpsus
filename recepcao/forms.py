from django import forms
from django.db.models import fields
from core.models import Patient
from django.core.mail.message import EmailMessage
from django.forms import ModelForm

class PatientForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('f', 'Feminino'),
        ('m', 'Masculino'),
        ('o', 'Outro')
    )


    class Meta:
        model = Patient
        fields = ('name', 'birth_date', 'cns', 'gender', 'city', 'uf', 'street', 'neighborhood', 'num')

    def save(self):
        return super().save(commit=True)
        

    
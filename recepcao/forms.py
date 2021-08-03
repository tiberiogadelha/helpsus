from django import forms
from django.db.models import fields
from core.models import Patient
from django.core.mail.message import EmailMessage
from django.forms import ModelForm

class DateInput(forms.DateInput):
    input_type = 'date'
    
class PatientForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('f', 'Feminino'),
        ('m', 'Masculino'),
        ('o', 'Outro')
    )

    uf_select = (("AC","Acre"), ("AL", "Alagoas"), ("AM", "Amazonas"), ("AP", "Amapá"), ("BA", "Bahia"), ("CE", "Ceará"), ("DF", "Distrito Federal"), ("ES", "Espirito Santo"), ("GO", "Goiás"), ("MA", "Maranhão"), ("MT", "Mato Grosso"), ("MS", "Mato Grosso do Sul"), ("MG", "Minas Gerais"), ("PA", "Pará"), ("PB", "Paraíba"), ("PR", "Paraná"), ("PE", "Pernambuco"), ("PI", "Piauí"), ("RJ", "Rio de Janeiro"), ("RN", "Rio Grande do Norte"), ("RO", "Roraima"), ("RS", "Rio Grande do Sul"), ("RR", "Roraima"), ("SC", "Santa Catarina"), ("SE", "Sergipe"), ("SP", "São Paulo"), ("TO", "Tocantins"))
    name = forms.CharField(label='Nome completo', max_length=250, min_length=10)
    birth_date = forms.DateField(label='Data de nascimento', widget=DateInput)
    gender = forms.ChoiceField(label='Sexo', choices=GENDER_CHOICES)
    cns = forms.CharField(label='Número do cartão do SUS', max_length=30)
    uf = forms.ChoiceField(choices=uf_select, label='Estado')
    city = forms.CharField(label='Cidade', max_length=100)
    neighborhood = forms.CharField(label='Bairro', max_length=100)
    street = forms.CharField(label='Rua', max_length=300)
    num = forms.CharField(label='Número', max_length=10)


    class Meta:
        model = Patient
        fields = ('name', 'birth_date', 'gender', 'cns', 'uf', 'city', 'neighborhood', 'street', 'num')

    def save(self):
        return super().save(commit=True)
        

    
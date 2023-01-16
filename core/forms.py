from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.db.models import fields
from .models import Employee, GENDER_CHOICES, Role, User
from django.core.mail.message import EmailMessage

class LoginForm(forms.Form):
    departments = (
        (' ', '--------------'),
        ('consultorio', 'Consultório'),
        ('farmacia', 'Farmácia'),
        ('laboratorio', 'Laboratório'),
        ('recepcao', 'Recepção'),
        ('triagem', 'Triagem')
    )
    email = forms.CharField(label='Email', max_length=150)
    password = forms.CharField(label='Senha', max_length=24, min_length=6)
    department = forms.ChoiceField(label='Setor', choices=departments)

class ReqNewPassword(forms.Form):
    email = forms.CharField(label='Email', max_length=200)

    def send_email(self, code, url):
        email = self.cleaned_data['email']
        mail = EmailMessage(
            subject= f"HelpSUS!: Recuperação de senha. Código: {code}  | Url: {url}",
            body = 'abc',
            from_email= 'email@gmail.com',
            to= [email]
        )
        mail.send()


'''
class UserModelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    re_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 're_password', 'gender', 'birth_date', 'conselho', 'role']

'''
class DateInput(forms.DateInput):
    input_type = 'date'

class UserModelForm(UserCreationForm):
    first_name = forms.CharField(label='Primeiro nome', max_length=150)
    last_name = forms.CharField(label='Sobrenomes', max_length=200)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    birth_date = forms.DateField(label='Data de nascimento', widget=DateInput)
    email = forms.EmailField(label='Email', max_length=200)
    gender = forms.ChoiceField(label='Sexo', choices=GENDER_CHOICES)
    conselho = forms.CharField(label='Conselho', max_length=200, required=False)


    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'gender', 'birth_date', 'email', 'username','gender', 'birth_date', 'password1', 'password2', 'role', 'conselho' )

        def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data['password1'])
            user.email = self.cleaned_data['username']
    
            if commit:
                user.save()
            return user

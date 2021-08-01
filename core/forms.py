from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.db.models import fields
from .models import Employee, User
from django.core.mail.message import EmailMessage

class LoginForm(forms.Form):
    email = forms.CharField(label='Email', max_length=150)
    password = forms.CharField(label='Password', max_length=24, min_length=6)
    department = forms.CharField(label='Department', max_length=100, min_length=4)
    #grande = forms.Charfield(label, widget=Textarea())

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

class UserModelForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'gender', 'birth_date', 'role', 'conselho')
        #labels = {'username': 'Email'}

        def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data['password1'])
            user.email = self.cleaned_data['username']
            if commit:
                user.save()
            return user

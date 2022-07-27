from django import http
from django.forms.utils import to_current_timezone
from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView, FormView 
from django.contrib.auth import authenticate, login
from .util import Validate
from uuid import uuid4
import random as random
from datetime import datetime
from .forms import LoginForm, ReqNewPassword, UserModelForm
from .models import Employee


ROUTER_TABLE = {
    'recepcao': 'indexReception',
    'laboratorio': 'indexLaboratory',
    'triagem': 'indexTriagem',
    'consultorio': 'indexClinic',
    'farmacia': 'indexPharmacy'
}

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['form'] = LoginForm()
        return context
        
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            form = LoginForm(request.POST)
            email = request.POST['email']
            password = request.POST['password']
            department = request.POST['department_select']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                if not user.is_enabled:
                    messages.error(request, 'Sua conta ainda não foi aceita. Aguarde aprovação!')
                    return super().get(request, *args, **kwargs)
                
                validator = Validate()
                is_valid = validator.validateUserDepartment(user, department)
                if not is_valid:
                    messages.error(request, f'Você não tem acesso a este setor: {department}')
                    return super().get(request, *args, **kwargs)

                login(request, user)
                route = f'{ROUTER_TABLE[department]}'
                return redirect(route)
                
            else:
                messages.error(request, 'Email e/ou senha inválidos')
            return super().get(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, e.__str__())
            return super().get(request, *args, **kwargs)

class signUpView(FormView):
    template_name = 'sign-up.html'
    form_class = UserModelForm

    def get_context_data(self, **kwargs):
        context = super(signUpView, self).get_context_data(**kwargs)
        try:
            if(self.request.method != 'GET'):
                context['form'] = UserModelForm(self.request.POST)
        except:
            context['form'] = UserModelForm()
        return context
        
    def form_valid(self, form):
        messages.success(self.request, 'Conta criada com sucesso! Aguarde avaliação do administrador.')
        form.save()
        form = UserModelForm()
        return redirect('index')

    def form_invalid(self, form):
        messages.error(self.request, 'Preencha os campos corretamente!')
        return super(signUpView, self).form_invalid(form)

    def get(self, request, *args, **kwargs):
        return super(signUpView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        try:
            form = UserModelForm(request.POST)
            if (form.is_valid()):
                form.save()
                messages.success(request, 'Usuário registrado com sucesso! Aguarde avaliação!')
                form = UserModelForm()
                return redirect('index')
            else:
                messages.error(request, form.errors)
                return super().get(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, e.__str__())
            return super().get(request, *args, **kwargs)
        
class ReqNewPasswordView(TemplateView):
    template_name = 'req-new-password.html'

    def get_context_data(self, **kwargs):
        context = super(ReqNewPasswordView, self).get_context_data(**kwargs)
        context['form'] = ReqNewPassword()
        return context       
    
    def post(self, request, *args, **kwargs):
        form = ReqNewPassword(request.POST)
        if (form.is_valid()):
            email = str(form.cleaned_data['email']).lower().strip()
            try:
                user = Employee.objects.get(email=email)
                code = random.randint(10000, 99999)
                url = uuid4()
                user.code = code
                user.reqPwd = datetime.now()
                user.pwdTries = 0
                user.pwdUrl = url
                user.save()
                form.send_email(code, url)
                messages.success(request, 'Confira no email as instruções para recuperação de senha!')
                form = ReqNewPassword()
                return redirect('index')
            except Employee.DoesNotExist:
                messages.error(request, 'Este email não está associado a nenhuma conta!')
        return super().get(request, *args, **kwargs)

from django.contrib.auth import logout

class logout_view(TemplateView):
    template_name = 'logout.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
    def get(self, request: http.HttpRequest, *args, **kwargs) -> http.HttpResponse:
        logout(request)
        return redirect('index')
    
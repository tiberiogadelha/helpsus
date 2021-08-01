from django import http
from django.forms.utils import to_current_timezone
from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView 
from uuid import uuid4
import random as random
from datetime import datetime
import asyncio

from .forms import LoginForm, ReqNewPassword, UserModelForm
from .models import Employee


class IndexView(TemplateView):
    template_name = 'index.html'
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['form'] = LoginForm()
        return context
        
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class signUpView(FormView):
    template_name = 'sign-up.html'
    form_class = UserModelForm

    def get_context_data(self, **kwargs):
        context = super(signUpView, self).get_context_data(**kwargs)
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
        form = UserModelForm(request.POST)
        if (form.is_valid()):
            form.save()
            messages.success(request, 'Usuário registrado com sucesso! Aguarde avaliação!')
            form = UserModelForm()
            return redirect('index')
        else:
            messages.error(request, 'Problemas no formulário!')
            return redirect('signUp')
    
    

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
            #print(email)
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
'''
def index(request):
    form = LoginForm(request.POST or None)
    if (str(request.method) == 'POST'):
        form = LoginForm(request.POST)
        if (form.is_valid()):
            # faço coisas de login
            messages.success(request, 'Sucesso no login')
            form = LoginForm()
        else:
            messages.error(request, 'Falha no login')



    
    pwdForm = RecoverPassword(request.POST or None)
    print(dir(pwdForm))
    if (str(request.method) == 'POST'):
        if (pwdForm.is_valid()):
            #send email
            messages.success(request, 'Um email foi enviado para recuperação de senha!')
            pwdForm = RecoverPassword()
        else:
            messages.error(request, 'Email inválido')

    if (pwdForm == RecoverPassword()):
        form = LoginForm(request.POST or None)
        if (str(request.method) == 'POST'):
            if (form.is_valid()):
                email = form.cleaned_data['email']
                form = LoginForm()
            else:
                messages.error(request, 'Problemas no login')
    else:
        form = LoginForm()



    context = {
        'form': form,
        'passwordForm': pwdForm
    }

    return render(request, 'index.html', context)

'''
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView
import asyncio

from .forms import LoginForm, RecoverPassword, UserModelForm

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['loginForm'] = LoginForm()
        context['pwdForm'] = RecoverPassword()
        return context

    def get(self, request, *args, **kwargs):
        
        
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
    if (str(request.method) == 'PUT'):
        pwdForm = RecoverPassword(request.POST)
        if (pwdForm.is_valid()):
            # faço coisas de login
            messages.success(request, 'Sucesso na recuperação')
            pwdForm = RecoverPassword()
        else:
            messages.error(request, 'Falha na recuperação')


    
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
def recoverPassword(request):
    form = RecoverPassword(request.POST or None)
    if (str(request.method) == 'POST'):
        if (form.is_valid()):
            form.send_email()
            messages.success('Sucesso! Confira seu email para atualizar a senha.')
        else:
            messages.error(request, 'Email inválido!')

    context = {
        'form': form
    }

    return render(request, 'index.html', context)


def signUp(request):
    if (str(request.method) == 'POST'):
        form = UserModelForm(request.POST)
        if (form.is_valid):
            print('AQUI')
            user = form.save(commit=False)
            print(f'{user.name} {user.email} {user.password}')
            messages.success(request, 'Usuário registrado com sucesso! Aguarde avaliação!')
            form = UserModelForm()

            return redirect('index')
        else:
            messages.error(request, 'Problemas no cadastro!')
    else:
        form = UserModelForm()

    context = {
        'form': form
    }

    return render(request, 'sign-up.html', context)

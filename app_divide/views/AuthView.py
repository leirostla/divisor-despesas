from app_divide.forms.auth_form import LoginForm, RegistroForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST

def login_view(request):
    
    message = None

    if request.user.is_authenticated:
        return redirect('sumario')

    if request.method == 'POST':

        loginForm = LoginForm(request.POST)

        if loginForm.is_valid():
            usuario = loginForm.cleaned_data["usuario"]
            password = loginForm.cleaned_data["password"]
            user = authenticate(username=usuario, password=password)
            if user is not None:
                login(request, user)
                return redirect('sumario')
            else:
                message = {'type':'danger',
                           'text':'Dados de usuário incorretos' }
    else:
        loginForm = LoginForm()

    context = {
        'form': loginForm,
        'message': message,
        'title': 'login',
        'button_text': 'Entrar'
    }

    return render(request, template_name='auth/auth.html',context=context)


@require_POST
def logout_view(request):
    logout(request)
    return redirect("login")


def registro_view(request):

    message = None
    if request.user.is_authenticated:
        return redirect('sumario')

    if request.method == 'POST':
        registro_form = RegistroForm(request.POST)

        if registro_form.is_valid():
            usuario = registro_form.cleaned_data['usuario']
            mail_usuario = registro_form.cleaned_data['email']
            password_usuario = registro_form.cleaned_data['password']

            verifica_usuario = User.objects.filter(username=usuario).first()
            verifica_mail = User.objects.filter(email=mail_usuario).first()

            if verifica_usuario is not None:
                message = {'type':'danger',
                           'text':'Já existe um usuário com esse username'}
            elif verifica_mail is not None:
                message = {'type':'danger',
                           'text':'Já existe um usuário com esse email'}
            else:
                user = User.objects.create_user(usuario, mail_usuario, password_usuario)
                if user is not None:
                    message = {'type':'sucess',
                                'text':'usuário criado com sucesso'}
                else:
                    message = {'type':'danger',
                                'text':'Erro ao criar usuário'}
    else:
        registro_form = RegistroForm()

    context = {
        'registro_form': registro_form,
        'message': message,
        'title': 'Registrar',
        'button_text': 'Registrar',
        'link_text' : 'Login'
    }

    return render(request, template_name='auth/auth.html', context=context)



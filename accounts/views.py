from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages

def cadastro(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        # Validações
        if password != password2:
            messages.error(request, 'As senhas não coincidem!')
            return render(request, 'accounts/cadastro.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este usuário já existe!')
            return render(request, 'accounts/cadastro.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado!')
            return render(request, 'accounts/cadastro.html')
        
        # Cria o usuário
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        messages.success(request, 'Cadastro realizado com sucesso! Faça login.')
        return redirect('login')
    
    return render(request, 'accounts/cadastro.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('pagina_inicial')
        else:
            messages.error(request, 'Usuário ou senha incorretos!')
    
    return render(request, 'accounts/login.html')  # CORRIGIDO: adicionei 'accounts/'

def logout_view(request):
    logout(request)
    return redirect('login')

def teste(request):
    return render(request, 'accounts/teste.html')
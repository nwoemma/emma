from django.shortcuts import render, redirect
from .form import RegisterForm 
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('loginUser')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def loginUser(request):
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            message = f'Hello {user.username}! You have been logged in.'
            return redirect('pages:home')  
        message = 'Login failed. Please check your username and password.'
    return render(request, 'users/login.html', {'message': message})

def logoutUser(request):
    logout(request)
    return redirect("users:loginUser")


# class CustomLoginView(LoginView):
#     template_name = 'users/login.html'  # Update this to your login template
#     success_url = reverse_lazy('home') 





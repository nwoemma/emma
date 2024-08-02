from django.shortcuts import render, redirect
from .form import RegisterForm 
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import serializers
from rest_framework.permissions import AllowAny


def page_view(request, page_name):
    titles = {
        'home': 'Home',
        'about': 'About Us',
        'register': 'Register',
        'login': 'Login',
        'profile': 'Your Profile',
        'menu': 'Menu',
        'booking': 'Booking',
    }
    title = titles.get(page_name, 'Default Title')
    return render(request, f'{page_name}.html', {'page_title': title})

def register(request):
    context = {}  # Initialize context variable
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:loginUser')
    else:
        form = RegisterForm()
    
    context['form'] = form
    context['page_title'] = 'Register'
    
    return render(request, 'users/register.html', context)

def loginUser(request):
    message = ''
    context = {
        'page_title': 'Login',
    }
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            message = f'Hello {user.username}! You have been logged in.'
            return redirect('pages:home')  
        message = 'Login failed. Please check your username and password.'
    
    context['message'] = message
    return render(request, 'users/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect("users:loginUser")


# class CustomLoginView(LoginView):
#     template_name = 'users/login.html'  # Update this to your login template
#     success_url = reverse_lazy('home') 

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'user': RegisterSerializer(user).data,
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({'message': 'User logged in successfully'}, status=status.HTTP_200_OK)
    
class LogoutAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)

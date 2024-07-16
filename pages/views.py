from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'pages/index.html')
def about(request):
    return render(request, "pages/about.html")
def book(request):
    return render(request, 'pages/book.html')
def menu(request):
    return render(request, 'pages/menu.html')
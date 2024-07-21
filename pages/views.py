from django.shortcuts import render

# Create your views here.
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

def home(request):
    return render(request, 'pages/index.html', {'page_title': 'Home'})

def about(request):
    return render(request, 'pages/about.html', {'page_title': 'About Us'})

def menu(request):
    return render(request, 'pages/menu.html', {'page_title': 'Menu'})
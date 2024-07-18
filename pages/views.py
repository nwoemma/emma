from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'pages/index.html')
def about(request):
    return render(request, "pages/about.html")
# def book(request):
#     return render(request, 'pages/book.html')
def menu(request):
    return render(request, 'pages/menu.html')

def page_title(request, page_name):
    # Logic to determine title based on page_name
    titles = {
        'home': 'Home',
        'about': 'About Us',
        'register':'Register',
        'login':'Login',
        'profile':'Your Profile',
        'profile_edit':'Edit your Profile',
        'menu':'Menu',
        'booking':'Booking',
    }
    title = titles.get(page_name, titles['register'])
    return render(request, 'base.html', {'page_title': title})
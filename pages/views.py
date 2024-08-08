from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
def page_view(request, page_name):
    titles = {
        "home": "Ivory Hospital - Home",
        "about": "Ivory Hospital - About Us",
        "contact": "Ivory Hospital - Contact Us",
        "services": "Ivory Hospital - Our Services",
        "register": "Register",
        "login": "Login",
        "profile": "Your Profile",
        "menu": "Menu",
        "booking": "Booking",
        "authenticated_home": "Ivory Hospital - Authenticated Home",
    }
    title = titles.get(page_name, "Default Title")
    return render(request, f"{page_name}.html", {"page_title": title})


def custom_404(request, exception):
    return render(request, "404.html", status=404)


@login_required
def authenticated_home(request):
    return render(
        request,
        "pages/authenticated_home.html",
        {"page_title": "Ivory Hospital - Home"},
    )


def home(request):
    if request.user.is_authenticated:
        return redirect("pages:authenticated_home")
    return render(request, "pages/index.html", {"page_title": "Ivory Hospital - Home"})


@login_required
def about(request):
    return render(
        request, "pages/about.html", {"page_title": "Ivory Hospital - About Us"}
    )


@login_required
def services(request):
    return render(
        request, "pages/services.html", {"page_title": "Ivory Hospital - Our Services"}
    )


@login_required
def contact(request):
    return render(
        request, "pages/contact.html", {"page_title": "Ivory Hospital - Contact Us"}
    )

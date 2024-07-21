from django.shortcuts import render, get_object_or_404,redirect
from django.contrib import messages
from .models import Product
from .form import TableForm
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.

def page_view(request, page_name):
    titles = {
        'product_list': 'Products',
        'product_details': 'Product details',
        'book_table': 'Booking',
    }
    title = titles.get(page_name, 'Default Title')
    return render(request, f'{page_name}.html', {'page_title': title})

def product_list(request):
    product = Product.objects.all()
    context = {
        'product': product,
        'page_title': 'Booking',
    }
    return render(request, 'shop/product_list.html',context)

def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product':product,
        'page_title': 'Booking',
    }
    return render(request, 'shop/product_detail.html',context)
    
def book_table(request):
    if request.method == 'POST':
        form = TableForm(request.POST)  # This should be your Django form
        if form.is_valid():  # Check if the form is valid
            form.save()
            messages.success(request, "Your table has been booked successfully!")
            return redirect('pages:home')
        else:
            messages.error(request, "There was an error with your booking.")
            # Optional: log form errors for debugging
            print(form.errors)  # This will print any form errors to the console for debugging
    else:
        form = TableForm()  # Instantiate an empty form for GET requests

    context = {
        'form': form,
        'page_title': 'Booking',
    }
    return render(request, 'shop/book_table.html', context)


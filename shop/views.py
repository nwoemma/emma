from django.shortcuts import render, get_object_or_404,redirect
from django.contrib import messages
from .models import Product,Booking
from .form import TableForm
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
def product_list(request):
    product = Product.objects.all()
    return render(request, 'shop/product_list.html', {'product':product})
    
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

def book_table(request):
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your table has been booked successfully!")
            return redirect('pages:home')  
            
        else:
            messages.error(request, "shop/book_table.html")
    else:
        form = TableForm()  # Instantiate an empty form for GET requests
    
    return render(request, 'shop/book_table.html', {'form': form})

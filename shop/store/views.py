from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order

# Главная страница с выводом всех товаров
def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

# Детальная страница товара
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

# Оформление заказа
def order(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        quantity = request.POST.get('quantity')

        product = get_object_or_404(Product, id=product_id)
        Order.objects.create(
            product=product,
            customer_name=customer_name,
            customer_email=customer_email,
            quantity=quantity,
        )
        return redirect('home')

    return render(request, 'store/order.html')

# Create your views here.

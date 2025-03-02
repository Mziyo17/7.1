from django.shortcuts import render, get_object_or_404, redirect
from .models import Car, Color, Brand, Comment
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Главная страница
def home(request):
    cars = Car.objects.all()
    return render(request, "home.html", {"cars": cars})

# Фильтр по цвету
def cars_by_color(request, color_id):
    color = get_object_or_404(Color, id=color_id)
    cars = Car.objects.filter(color=color)
    return render(request, "cars_by_color.html", {"cars": cars, "color": color})

# Фильтр по бренду
def cars_by_brand(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    cars = Car.objects.filter(brand=brand)
    return render(request, "cars_by_brand.html", {"cars": cars, "brand": brand})

# Детальная страница машины
def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    comments = Comment.objects.filter(car=car)
    return render(request, "car_detail.html", {"car": car, "comments": comments})

# Добавление комментариев
@login_required
def add_comment(request, car_id):
    if request.method == "POST":
        text = request.POST.get("text")
        car = get_object_or_404(Car, id=car_id)
        Comment.objects.create(car=car, user=request.user, text=text)
        return redirect("car_detail", car_id=car.id)
    return redirect("home")

# Регистрация
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

# Авторизация
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
    return render(request, "login.html")

# Выход из аккаунта
def user_logout(request):
    logout(request)
    return redirect("home")


# Create your views here.

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


from .models import Car, Brand, Color


def car_list(request):
    brand_id = request.GET.get('brand')
    color_id = request.GET.get('color')

    cars = Car.objects.all()

    if brand_id:
        cars = cars.filter(brand_id=brand_id)
    if color_id:
        cars = cars.filter(color_id=color_id)

    brands = Brand.objects.all()
    colors = Color.objects.all()

    return render(request, 'car_list.html', {'cars': cars, 'brands': brands, 'colors': colors})


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Car, Like


def toggle_like(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.user.is_authenticated:
        like, created = Like.objects.get_or_create(car=car, user=request.user)
        if not created:
            like.delete()
            return JsonResponse({'liked': False, 'likes_count': car.likes.count()})
        return JsonResponse({'liked': True, 'likes_count': car.likes.count()})

    return JsonResponse({'error': 'Not authenticated'}, status=403)


from django.shortcuts import redirect
from .forms import CarForm


def add_car(request):
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('car_list')
    else:
        form = CarForm()

    return render(request, 'add_car.html', {'form': form})

from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.urls import reverse_lazy
from .models import Lesson

class LessonListView(ListView):
    model = Lesson
    template_name = 'lesson_list.html'  # Sahifa shabloni
    context_object_name = 'lessons'  # Template-da foydalaniladigan o'zgaruvchi nomi
class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'lesson_detail.html'
    context_object_name = 'lesson'
class LessonCreateView(CreateView):
    model = Lesson
    template_name = 'lesson_form.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('lesson_list')  # Qo'shgandan keyin qaytish sahifasi
class LessonDeleteView(DeleteView):
    model = Lesson
    template_name = 'lesson_confirm_delete.html'
    success_url = reverse_lazy('lesson_list')
from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

class LessonUpdateView(View):
    def post(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        lesson.title = request.POST.get('title', lesson.title)
        lesson.description = request.POST.get('description', lesson.description)
        lesson.save()
        return JsonResponse({'message': 'Lesson updated successfully'})
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .models import Car

class CarUpdateView(UpdateView):
    model = Car
    fields = ['name', 'brand', 'color']
    template_name = 'car_update.html'
    success_url = reverse_lazy('car_list')
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']
    template_name = 'category_form.html'
    success_url = reverse_lazy('category_list')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']
    template_name = 'category_form.html'
    success_url = reverse_lazy('category_list')
class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category_confirm_delete.html'
    success_url = reverse_lazy('category_list')


from django.db.models import Q


class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Car.objects.filter(Q(name__icontains=query) | Q(brand__name__icontains=query))
        return Car.objects.all()
from django.core.paginator import Paginator

class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'
    paginate_by = 5  # 5 машин на страницу

# Create your views here.

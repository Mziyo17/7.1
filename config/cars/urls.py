from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("cars/color/<int:color_id>/", views.cars_by_color, name="cars_by_color"),
    path("cars/brand/<int:brand_id>/", views.cars_by_brand, name="cars_by_brand"),
    path("car/<int:car_id>/", views.car_detail, name="car_detail"),
    path("car/<int:car_id>/comment/", views.add_comment, name="add_comment"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
]

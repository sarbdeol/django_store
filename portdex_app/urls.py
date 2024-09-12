from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('products/', views.index, name='products'),
    path('product/<slug:slug>/', views.product_page, name='product_page'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('product-add/', views.admin_page, name='admin_page'),
    path('logout/', views.user_logout, name='logout'),
]


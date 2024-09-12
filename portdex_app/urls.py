from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.main, name='main'),
    path('products/', views.index, name='products'),
    path('product/<slug:slug>/', views.product_page, name='product_page'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('product-add/', views.add_product, name='add_product'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
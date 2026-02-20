"""
URL configuration for petmart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # ADMIN
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('adminpage/', views.adminpage, name='adminpage'),
    path('manage/', views.manageproduct, name='manage'),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('viewproduct/', views.viewproduct, name='viewproduct'),
    path('update/<int:pk>/', views.viewproductupdate, name='update'),
    path('delete/<int:pk>/', views.viewproductdelet, name='delete'),

    # AUTH
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),

    # STORE
    path('store/', views.userpage, name='userpage'),
    path('store/<str:category>/', views.userpage, name='filter_category'),

    # GAME DETAIL
    path('game/<int:id>/', views.game_detail, name='game_detail'),

    # CART
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:game_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:game_id>/', views.remove_from_cart, name='remove_from_cart'),

    # WISHLIST
    path('wishlist/', views.view_wishlist, name='view_wishlist'),
    path('wishlist/add/<int:game_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:game_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    # LIBRARY
    path('library/', views.library, name='library'),

    # PROFILE
    path('profile/', views.user_profile, name='user_profile'),

    # BUY NOW
    path('buy/<int:game_id>/', views.buy_now, name='buy_now'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
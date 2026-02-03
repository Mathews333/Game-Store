from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # admin
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('adminpage/', views.adminpage, name='adminpage'),

    # products
    path('manageproduct/', views.manageproduct, name='manageproduct'),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('view/', views.viewproduct, name='viewproduct'),
    path('update/<int:pk>/', views.viewproductupdate, name='updategames'),
    path('delete/<int:pk>/', views.viewproductdelet, name='deletegames'),

    # auth
    path('register/', views.register, name='register'),
    path('', views.user_login, name='login'),          # 👈 homepage login
    path('userpage/', views.userpage, name='userpage'), # 👈 THIS FIXES ERROR
    
    path('games/', views.view_game, name='view_game'),
    path('games/<int:id>/', views.game_detail, name='game_detail'),
    
    path('cart/add/<int:game_id>/', views.add_to_cart, name='add_to_cart'),
    path('wishlist/add/<int:game_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:game_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('wishlist/', views.view_wishlist, name='view_wishlist'),
    
    path('profile/', views.user_profile, name='user_profile'),
    
    path('wishlist/', views.view_wishlist, name='view_wishlist'),
    path('wishlist/add/<int:game_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:game_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    path('store/', views.userpage, name='userpage'),
    path('store/category/<str:category>/', views.userpage, name='filter_category'),
    
    path('buy/<int:game_id>/', views.buy_now, name='buy_now'),
  path('checkout/<int:game_id>/', views.checkout, name='checkout'),





]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

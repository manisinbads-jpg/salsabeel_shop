from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('', views.product_list, name='product_list'),  # shop listing page
    path('category/<slug:slug>/', views.product_list_by_category, name='product_list_by_category'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('new-arrivals/', views.new_arrivals, name='new_arrivals'),
    path('promotions/', views.promotions, name='promotions'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),

]

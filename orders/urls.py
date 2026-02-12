from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.create, name='create'),
    path('my-orders/', views.order_list, name='order_list'),
    path('<int:order_id>/', views.order_detail, name='detail'),
    path('history/', views.order_history, name='history'),
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('success/<int:order_id>/', views.success, name='success'),
    path('confirm/<int:order_id>/', views.confirm_payment, name='confirm_payment'),
    path('upload_receipt/<int:order_id>/', views.upload_receipt, name='upload_receipt'),
    path('invoice/<int:order_id>/', views.order_invoice_pdf, name='order_invoice'),

]

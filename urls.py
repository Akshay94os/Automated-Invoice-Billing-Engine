from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='billing_home'),
    path('invoice/<int:pk>/', views.invoice_detail, name='invoice_detail'),
]

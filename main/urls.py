from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_account, name='create_account'),
    path('transaction/', views.transaction, name='transaction'),
    path('security/', views.security, name='security'),
]

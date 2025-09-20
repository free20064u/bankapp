from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('account/create/', views.create_account, name='create_account'),
    path('account/<int:account_id>/transactions/', views.view_transactions, name='view_transactions'),
    path('transaction/make/', views.make_transaction, name='make_transaction'),
]

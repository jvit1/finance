from django.urls import path
from . import views

app_name = 'transaction'

urlpatterns = [
    path('', views.home, name='home'),
    path('update-category/<int:transaction_id>/', views.update_transaction_category, name='update-category'),
]
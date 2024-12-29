from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('overview/categorize/', views.categorize_spending, name='categorize-spending')
]
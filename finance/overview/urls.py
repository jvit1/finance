from django.urls import path
from . import views

app_name = 'overview'

urlpatterns = [
    path('', views.home, name='home'),
    path('overview/categorize/', views.categorize_spending, name='categorize-spending')
]
from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),                 
    path('display/', views.DisplayView.as_view(), name='display'),
    path('', views.HomeView.as_view(), name='home')
]
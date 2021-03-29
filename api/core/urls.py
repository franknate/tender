from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from . import views

router = DefaultRouter()
router.register('tenders', views.TenderViewSet)

urlpatterns = [
    path('login/', obtain_auth_token, name="login"), 
    path('bid/<int:tender_id>/', views.BidView.as_view(), name="bid"), 
    path('', include(router.urls)),
]
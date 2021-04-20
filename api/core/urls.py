from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework.authtoken.views import obtain_auth_token

from . import views

router = SimpleRouter()
router.register('tenders', views.TenderViewSet)

urlpatterns = [
    path('login/', obtain_auth_token, name="login"), 
    path('bid/<int:tender_id>/', views.BidView.as_view(), name="bid"), 
    path('', include(router.urls)),
]

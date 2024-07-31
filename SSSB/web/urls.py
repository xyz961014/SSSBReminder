from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApartmentAmountViewSet
from .views import get_status
from .views import IndexView

router = DefaultRouter()
router.register(r'apartment_amount', ApartmentAmountViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('get_status/', get_status),
    path('index', IndexView.as_view(), name='index'),
]

from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView
from .views import ApartmentAmountViewSet, ApartmentInfoViewSet, ApartmentStatusViewSet
from .views import PersonalFilterViewSet
from .views import get_regions, get_types
from .views import get_space_range, get_rent_range, get_floor_range, get_credit_range
from .views import get_filtered_apartments
from .views import get_drawing
from .views import IndexView

router = DefaultRouter()
router.register(r'apartment_amount', ApartmentAmountViewSet)
router.register(r'apartment_info', ApartmentInfoViewSet)
router.register(r'apartment_status', ApartmentStatusViewSet)
router.register(r'personal_filter', PersonalFilterViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('get_regions', get_regions, name='get_regions'),
    path('get_types', get_types, name='get_types'),
    path('get_space_range', get_space_range, name='get_space_range'),
    path('get_rent_range', get_rent_range, name='get_rent_range'),
    path('get_floor_range', get_floor_range, name='get_floor_range'),
    path('get_credit_range', get_credit_range, name='get_credit_range'),
    path('get_filtered_apartments', get_filtered_apartments, name='get_filtered_apartments'),
    path('get_drawing', get_drawing, name='get_drawing'),
]

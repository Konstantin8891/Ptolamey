from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RoomViewSet, BookAPIView, BookingViewSet


router = DefaultRouter()
router.register('rooms', RoomViewSet)
router.register('mybooking', BookingViewSet, basename='booking')

app_name = 'api'

urlpatterns = [
    path('rooms/<int:room_id>/book/', BookAPIView.as_view()),
    path('', include(router.urls)),
]

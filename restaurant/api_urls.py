from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'bookings', views.BookingViewSet, basename='booking')

urlpatterns = [
    # Menu endpoints
    path('menu/', views.MenuItemView.as_view(), name='menu-list'),
    path('menu/<int:pk>/', views.SingleMenuItemView.as_view(), name='menu-detail'),
    # Booking endpoints (router handles GET, POST, PUT, DELETE)
    path('', include(router.urls)),
    # Auth endpoints
    path('registration/', views.registration, name='registration'),
    path('login/', views.login_view, name='login'),
    path('me/', views.current_user, name='current-user'),
]

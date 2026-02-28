from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Restaurant views (HTML)
    path('', include('restaurant.urls')),
    # API endpoints
    path('api/', include('restaurant.api_urls')),
    # Authentication with Djoser
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

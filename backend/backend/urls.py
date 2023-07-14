from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api/', include('api.urls', namespace='api')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('admin/', admin.site.urls),
]

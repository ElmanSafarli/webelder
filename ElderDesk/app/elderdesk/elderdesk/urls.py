from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),
    # User management
    # path('accounts/', include('allauth.urls')),
    path('oauth2/', include('django_auth_adfs.urls')),
    path('silk/', include('silk.urls', namespace='silk')),
    # Local apps
    path('', include('pages.urls')),
    path('dashboard/', include('tickets.urls')),
]

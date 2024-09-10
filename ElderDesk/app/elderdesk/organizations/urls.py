from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:pk>/', views.OrganizationDetailView.as_view(), name='organization_detail'),
    path('api/get-organizations/', views.get_organizations, name='get_organizations'),
]

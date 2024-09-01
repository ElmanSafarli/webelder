from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.OrganizationDetailView.as_view(), name='organization_detail'),
    path('get-organizations/', views.get_organizations, name='get_organizations'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrganizationListView.as_view(), name='organization_list'),
    # path('add/', views.OrganizationCreateView.as_view(), name='organization_add'),
    path('<int:pk>/', views.OrganizationDetailView.as_view(), name='organization_detail'),
]

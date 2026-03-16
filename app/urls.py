from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/profile/', views.api_profile),
    path('api/research/', views.api_research),
    path('api/publications/', views.api_publications),
    path('api/projects/', views.api_projects),
    path('api/awards/', views.api_awards),
    path('api/cv/', views.api_cv),
    path('api/gallery/', views.api_gallery),
    path('api/stats/', views.api_stats),
    path('api/contact/', views.api_contact),
]

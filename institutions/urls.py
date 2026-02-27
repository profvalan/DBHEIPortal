from django.urls import path
from . import views

app_name = 'institutions'

urlpatterns = [
    # Public
    path('', views.institution_directory, name='directory'),
    path('<int:pk>/', views.institution_detail, name='detail'),

    # Institution self-edit
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('stats/edit/', views.edit_stats, name='edit_stats'),

    # Admin
    path('admin/list/', views.admin_institution_list, name='admin_list'),
    path('admin/edit/<int:pk>/', views.admin_edit_institution, name='admin_edit'),
]
